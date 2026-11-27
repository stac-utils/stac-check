import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Optional, Tuple
from urllib.parse import urlparse, urlunparse

from stac_validator.utilities import fetch_and_parse_file

from stac_check.lint import Linter


def extract_schemas(obj: Dict) -> List[str]:
    """Extract schemas from a STAC object.

    Args:
        obj: A STAC object (Item, Collection, etc.)

    Returns:
        List of schema URLs
    """
    schemas = []
    if isinstance(obj, dict):
        stac_version = obj.get("stac_version", "1.0.0")
        item_type = obj.get("type", "Item")

        # Add base schema (handle both "Item" and "Feature" types for GeoJSON)
        if item_type in ("Item", "Feature"):
            schemas.append(
                f"https://schemas.stacspec.org/v{stac_version}/item-spec/json-schema/item.json"
            )
        elif item_type == "Collection":
            schemas.append(
                f"https://schemas.stacspec.org/v{stac_version}/collection-spec/json-schema/collection.json"
            )

        # Add extension schemas
        for ext in obj.get("stac_extensions", []):
            schemas.append(ext)

    return schemas


def validate_collection_fast(
    source: str,
    linter_class: Any,
    verbose: bool = False,
    lint_items: bool = False,
    headers: Optional[Dict] = None,
) -> tuple[List[Dict], float, List[str]]:
    """Validate a collection file using FastValidator.

    Uses the updated FastValidator that exposes valid/invalid counts and error details
    in the message dict, eliminating the need for temp files.

    Args:
        source: Path to the STAC collection file
        linter_class: The Linter class to use for validation
        verbose: Whether to show verbose output
        lint_items: Whether to run linting checks on each item
        headers: Optional HTTP headers forwarded to the linter instances

    Returns:
        Tuple of (results list, total_time in ms, schemas_checked list)
    """
    start_time = time.time()
    results_by_url = {}

    # Parse the source file to get items
    with open(source) as f:
        data = json.load(f)

    items = (
        data.get("features", []) if data.get("type") == "FeatureCollection" else [data]
    )

    # Validate the collection file with FastValidator
    # FastValidator now exposes valid_count, invalid_count, and error details
    linter = linter_class(source, verbose=verbose, fast=True, headers=headers or {})

    # FastValidator returns message as a list with one dict
    if isinstance(linter.message, list) and len(linter.message) > 0:
        msg = linter.message[0]
    else:
        msg = linter.message if isinstance(linter.message, dict) else {}

    # Extract validation results from FastValidator message
    schemas_checked = msg.get("schemas_checked", [])
    errors = msg.get("errors") or []

    # Build a map of failed item IDs for quick lookup
    failed_items: Dict[str, List[str]] = {}
    for error in errors:
        for item_id in error.get("affected_items", []):
            if item_id not in failed_items:
                failed_items[item_id] = []
            failed_items[item_id].append(error.get("error_message", ""))

    # Early-return failures (unsupported version, load errors) carry no
    # per-item errors; the file-level error applies to every item
    file_level_error = None
    if not msg.get("valid_stac", True) and not failed_items:
        file_level_error = msg.get("error_message") or "Validation failed"

    # Create per-item results
    for idx, obj in enumerate(items):
        item_id = obj.get("id", f"unknown-{idx}")
        obj_url = f"{source}/{item_id}"
        item_schemas = extract_schemas(obj)

        # Determine if item is valid
        is_valid = item_id not in failed_items and file_level_error is None
        error_messages = failed_items.get(item_id, [])
        if file_level_error is not None:
            error_messages = [file_level_error]

        # Get best practices and geometry errors for this item (linting checks
        # only, no re-validation)
        best_practices = []
        geometry_errors = []
        if lint_items:
            try:
                item_linter = linter_class(
                    obj,
                    verbose=verbose,
                    prevalidated=True,
                    headers=headers or {},
                )
                best_practices = item_linter.best_practices_msg
                geometry_errors = item_linter.geometry_errors_msg
            except Exception:
                best_practices = []
                geometry_errors = []

        result = {
            "path": obj_url,
            "valid_stac": is_valid,
            "asset_type": "",
            "version": obj.get("stac_version", ""),
            "validation_method": "stac-valid FastValidator",
            "error_type": "FastValidationError" if not is_valid else "",
            "error_message": error_messages[0] if error_messages else "",
            "best_practices": best_practices,
            "geometry_errors": geometry_errors,
            "schema": item_schemas,
            "original_object": obj,
        }
        results_by_url[obj_url] = result

    # Calculate total validation time
    total_time = (time.time() - start_time) * 1000

    return list(results_by_url.values()), total_time, schemas_checked


@dataclass
class ApiLinter:
    """A class for linting paginated STAC endpoints or static files.

    This linter handles item collections, collections, and other STAC endpoints,
    with support for pagination and HTTP headers.

    Args:
        source (str): URL or file path of the STAC endpoint or static file
            (e.g. /items, /collections, or local JSON).
        object_list_key (str): Key in response containing list of objects
            (e.g. "features", "collections").
        pages (int): Number of pages to fetch. Defaults to 1.
        headers (Optional[Dict], optional): Optional headers for HTTP requests. Defaults to None.

    Attributes:
        source (str): The source URL or file path.
        object_list_key (str): The key for the list of objects in the response.
        pages (int): Maximum number of pages to process (0 follows every page).
        headers (Dict): HTTP headers for requests.
        version (Optional[str]): STAC version detected from validated objects.
        validator_version (str): Version of stac-validator being used.
    """

    def __init__(
        self,
        source: str,
        object_list_key: str,
        pages: Optional[int] = 1,
        headers: Optional[Dict] = None,
        verbose: bool = False,
        fast: bool = False,
    ):
        self.source = source
        self.object_list_key = object_list_key
        self.pages = pages if pages is not None else 1
        self.headers = headers or {}
        self.verbose = verbose
        self.fast = fast
        self.version = None
        self.validator_version = self._get_validator_version()
        self.start_time = time.time()
        self.total_time = 0.0
        self.schemas_checked: List[str] = []
        # Set when the response contains a different list key than the one
        # requested (e.g. "features" seen while validating --collections)
        self.mismatched_list_key: Optional[str] = None

    def _get_validator_version(self) -> str:
        """Get the version of stac-validator being used.

        Returns:
            str: The version string of stac-validator, or "unknown" if not available.
        """
        try:
            import stac_validator

            return getattr(stac_validator, "__version__", "unknown")
        except ImportError:
            return "unknown"

    def set_update_message(self) -> str:
        """Generate a message for users about their STAC version.

        Returns:
            str: A string containing a message about the current STAC version
                and recommendation to update if needed.
        """
        if not self.version:
            return "Please upgrade to STAC version 1.1.0!"
        elif self.version != "1.1.0":
            return f"Please upgrade from version {self.version} to version 1.1.0!"
        else:
            return "Thanks for using STAC version 1.1.0!"

    def _fetch_and_parse(self, url: str) -> Dict:
        """Fetch and parse a STAC file from a URL.

        Args:
            url (str): The URL to fetch the STAC file from.

        Returns:
            Dict: The parsed STAC file as a dictionary.
        """
        return fetch_and_parse_file(url, self.headers)

    def iterate_objects(self) -> Generator[Tuple[Dict, str], None, None]:
        """Iterate through all objects in the endpoint, following pagination if necessary.

        This generator yields each object in the endpoint along with its URL.
        It handles pagination by following "next" links and prevents duplicate objects
        by tracking seen IDs.

        Yields:
            Tuple[Dict, str]: A tuple containing (object_dict, object_url) for each object.
        """
        stac_file = self.source
        page = 1
        seen_ids = set()

        def get_base_url(url: str) -> str:
            """Extract the base URL without query parameters or fragments.

            Args:
                url (str): The full URL to process.

            Returns:
                str: The base URL without query parameters or fragments.
            """
            parsed = urlparse(url)
            return urlunparse(parsed._replace(query="", fragment=""))

        while stac_file:
            response = self._fetch_and_parse(stac_file)
            objects = response.get(self.object_list_key)
            # Only list responses paginate — a bare STAC object with a
            # rel="next" link (e.g. item navigation) is not a page of results
            is_list_response = isinstance(objects, list)
            if not is_list_response:
                objects = []
                for alt in ("features", "collections", "catalogs"):
                    if alt != self.object_list_key and isinstance(
                        response.get(alt), list
                    ):
                        self.mismatched_list_key = alt
                        break
                # A bare STAC object (not a list response) is validated
                # as itself rather than silently checking nothing
                if self.mismatched_list_key is None and (
                    response.get("type") or response.get("stac_version")
                ):
                    objects = [response]
            for obj in objects:
                obj_id = obj.get("id")
                base_url = get_base_url(stac_file)
                obj_url = f"{base_url}/{obj_id}" if obj_id else base_url
                # Only yield if not seen before (protects against duplicates from bad APIs)
                if obj_id not in seen_ids:
                    seen_ids.add(obj_id)
                    yield obj, obj_url
            # Pagination: look for 'next' link
            next_link = None
            for link in response.get("links", []):
                if link.get("rel") == "next":
                    next_link = link.get("href")
                    break
            # Check if we should continue to the next page
            # (pages <= 0 means follow every page)
            if (
                next_link
                and next_link != stac_file
                and is_list_response
                and (self.pages <= 0 or page < self.pages)
            ):
                stac_file = next_link
                page += 1
            else:
                break

    def lint_all(self) -> List[Dict]:
        """Lint all objects in the endpoint, handling pagination if configured.

        This method processes all objects in the endpoint (up to the specified number of pages),
        validates each object using the Linter class, and collects the results.
        It ensures only one result per asset URL and preserves the original object
        for potential further processing.

        Returns:
            List[Dict]: A list of validation result dictionaries, one per object,
                matching the message structure of the Linter class.
        """
        results_by_url = {}

        # Local FeatureCollection files are validated in one pass; --fast only
        # controls whether per-item linting runs, not the engine. Other list
        # shapes (e.g. {"collections": [...]}) go through iterate_objects since
        # FastValidator only understands "features".
        is_local_file = (
            isinstance(self.source, str)
            and self.source.endswith((".json", ".geojson"))
            and not self.source.startswith(("http://", "https://"))
            and self.object_list_key == "features"
        )
        if is_local_file:
            try:
                with open(self.source) as f:
                    envelope = json.load(f)
                if isinstance(envelope, dict):
                    for alt in ("features", "collections", "catalogs"):
                        if alt != self.object_list_key and isinstance(
                            envelope.get(alt), list
                        ):
                            self.mismatched_list_key = alt
                            return []
            except (OSError, ValueError):
                pass
            try:
                results, total_time, schemas = validate_collection_fast(
                    self.source,
                    Linter,
                    self.verbose,
                    lint_items=not self.fast,
                    headers=self.headers,
                )

                # Store results and metadata
                self.total_time = total_time
                self.schemas_checked = schemas

                # Set version from first result
                if results and self.version is None:
                    self.version = results[0].get("version")

                return results
            except Exception:
                # Fall back to regular validation if fast validation fails
                pass

        # Regular validation path (non-fast or when FastValidator unavailable)
        for obj, obj_url in self.iterate_objects():
            try:
                linter = Linter(
                    obj,
                    verbose=self.verbose,
                    fast=self.fast,
                    headers=self.headers,
                )
                msg = dict(linter.message)
                msg["path"] = obj_url
                msg["best_practices"] = linter.best_practices_msg
                msg["geometry_errors"] = linter.geometry_errors_msg
                # Store the original object to allow recreation of Linter instance later
                msg["original_object"] = obj
                results_by_url[obj_url] = msg

                # Set the version from the first valid STAC object if not already set
                if self.version is None:
                    # Get version from the validation message
                    stac_version = msg.get("version")
                    if stac_version:
                        self.version = stac_version
            except Exception as e:
                results_by_url[obj_url] = {
                    "path": obj_url,
                    "valid_stac": False,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "best_practices": [],
                    "geometry_errors": [],
                    "version": None,
                    "schema": [],
                    "original_object": obj,  # Still include the original object even if validation failed
                }

        # Calculate total validation time
        self.total_time = (
            time.time() - self.start_time
        ) * 1000  # Convert to milliseconds

        return list(results_by_url.values())
