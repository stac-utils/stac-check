"""Fast validation wrapper for item collections using FastValidator."""

import json
import time
from typing import Any, Dict, List


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
    source: str, linter_class: Any, verbose: bool = False, fast_linting: bool = False
) -> tuple[List[Dict], float, List[str]]:
    """Validate a collection file using FastValidator.

    Uses the updated FastValidator that exposes valid/invalid counts and error details
    in the message dict, eliminating the need for temp files.

    Args:
        source: Path to the STAC collection file
        linter_class: The Linter class to use for validation
        verbose: Whether to show verbose output
        fast_linting: Whether to include linting checks in fast mode

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
    linter = linter_class(source, verbose=verbose, fast=True)

    # FastValidator returns message as a list with one dict
    if isinstance(linter.message, list) and len(linter.message) > 0:
        msg = linter.message[0]
    else:
        msg = linter.message if isinstance(linter.message, dict) else {}

    # Extract validation results from FastValidator message
    schemas_checked = msg.get("schemas_checked", [])
    errors = msg.get("errors", [])

    # Build a map of failed item IDs for quick lookup
    failed_items: Dict[str, List[str]] = {}
    for error in errors:
        for item_id in error.get("affected_items", []):
            if item_id not in failed_items:
                failed_items[item_id] = []
            failed_items[item_id].append(error.get("error_message", ""))

    # Create per-item results
    for idx, obj in enumerate(items):
        item_id = obj.get("id", f"unknown-{idx}")
        obj_url = f"{source}/{item_id}"
        item_schemas = extract_schemas(obj)

        # Determine if item is valid
        is_valid = item_id not in failed_items
        error_messages = failed_items.get(item_id, [])

        # Get best practices for this item (linting checks only, no re-validation)
        # Only run linting if fast_linting is enabled
        best_practices = []
        if fast_linting:
            try:
                item_linter = linter_class(
                    obj, verbose=verbose, fast=True, fast_linting=True
                )
                best_practices = item_linter.best_practices_msg
            except Exception:
                best_practices = []

        result = {
            "path": obj_url,
            "valid_stac": is_valid,
            "asset_type": "",
            "version": obj.get("stac_version", ""),
            "validation_method": "FastJSONSchema",
            "error_type": "FastValidationError" if not is_valid else "",
            "error_message": error_messages[0] if error_messages else "",
            "best_practices": best_practices,
            "geometry_errors": [],
            "schema": item_schemas,
            "original_object": obj,
        }
        results_by_url[obj_url] = result

    # Calculate total validation time
    total_time = (time.time() - start_time) * 1000

    return list(results_by_url.values()), total_time, schemas_checked
