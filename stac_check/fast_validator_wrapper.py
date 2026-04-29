"""Fast validation wrapper for item collections using FastValidator."""

import json
import os
import tempfile
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
    """Validate a collection file using FastValidator.

    FastValidator automatically detects FeatureCollections and validates each item,
    tracking valid/invalid counts.

    Args:
        source: Path to the STAC collection file
        linter_class: The Linter class to use for validation
        verbose: Whether to show verbose output

    Returns:
        Tuple of (results list, total_time in ms, schemas_checked list)
    """
    start_time = time.time()
    results_by_url = {}

    # Parse the source file to get items and schemas
    with open(source) as f:
        data = json.load(f)

    items = (
        data.get("features", []) if data.get("type") == "FeatureCollection" else [data]
    )

    all_schemas = set()
    for obj in items:
        item_schemas = extract_schemas(obj)
        all_schemas.update(item_schemas)

    # Validate each item individually with temp files to use FastValidator
    for idx, obj in enumerate(items):
        item_id = obj.get("id", f"unknown-{idx}")
        obj_url = f"{source}/{item_id}"
        item_schemas = extract_schemas(obj)

        # Create temp file for this item and validate with FastValidator
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump(obj, tmp)
            tmp_path = tmp.name

        try:
            # Validate with Linter using fast=True (will use FastValidator on file)
            linter = linter_class(tmp_path, verbose=verbose, fast=True)
            msg = dict(linter.message)

            msg["path"] = obj_url
            msg["best_practices"] = []
            msg["geometry_errors"] = []
            msg["schema"] = item_schemas
            msg["original_object"] = obj
            results_by_url[obj_url] = msg
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    # Calculate total validation time
    total_time = (time.time() - start_time) * 1000

    # Store schemas for display
    schemas_checked = sorted(list(all_schemas))

    return list(results_by_url.values()), total_time, schemas_checked
