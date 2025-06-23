from dataclasses import dataclass
from typing import Dict, Generator, List, Optional, Tuple
from urllib.parse import urlparse, urlunparse

from stac_validator.utilities import fetch_and_parse_file

from stac_check.lint import Linter


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
        pages (int): Maximum number of pages to process.
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
    ):
        self.source = source
        self.object_list_key = object_list_key
        self.pages = pages if pages is not None else 1
        self.headers = headers or {}
        self.verbose = verbose
        self.version = None
        self.validator_version = self._get_validator_version()

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
            objects = response.get(self.object_list_key, [])
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
            if next_link and next_link != stac_file and page < self.pages:
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
        for obj, obj_url in self.iterate_objects():
            try:
                linter = Linter(obj, verbose=self.verbose)
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
                    "recommendation": None,
                    "error_verbose": None,
                    "failed_schema": None,
                    "original_object": obj,  # Still include the original object even if validation failed
                }
        return list(results_by_url.values())
