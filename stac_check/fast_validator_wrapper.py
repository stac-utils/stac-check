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
    source: str, linter_class: Any, verbose: bool = False
) -> tuple[List[Dict], float, List[str]]:
    """Validate a collection file using FastValidator with per-item results.

    Args:
        source: Path to the STAC collection file
        linter_class: The Linter class to use for validation
        verbose: Whether to show verbose output

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

    # Collect all schemas from items
    all_schemas = set()

    # Validate the entire collection with FastValidator once (for schema caching)
    # This validates all items at once and caches schemas
    linter_for_file = linter_class(source, verbose=verbose, fast=True)
    file_result = linter_for_file.message

    # Create per-item results from the collection validation
    # All items get the same validation result as the collection
    for idx, obj in enumerate(items):
        item_id = obj.get("id", f"unknown-{idx}")
        obj_url = f"{source}/{item_id}"

        # Extract schemas from item
        item_schemas = extract_schemas(obj)
        all_schemas.update(item_schemas)

        # Create result for this item
        msg = {
            "path": obj_url,
            "valid_stac": file_result.get("valid_stac", True),
            "asset_type": file_result.get("asset_type", ""),
            "version": obj.get("stac_version", ""),
            "validation_method": file_result.get("validation_method", "FastJSONSchema"),
            "error_type": file_result.get("error_type", ""),
            "error_message": file_result.get("error_message", ""),
            "best_practices": [],
            "geometry_errors": [],
            "schema": item_schemas,
            "original_object": obj,
        }
        results_by_url[obj_url] = msg

    # Calculate total validation time
    total_time = (time.time() - start_time) * 1000

    # Store schemas for display
    schemas_checked = sorted(list(all_schemas))

    return list(results_by_url.values()), total_time, schemas_checked
