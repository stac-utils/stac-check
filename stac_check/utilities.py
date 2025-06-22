import contextlib
from typing import Callable

import click


def determine_asset_type(data):
    """Determine the STAC asset type from the given data dictionary.

    This function identifies the type of STAC object based on its structure and content.
    It handles all STAC object types including Item, Collection, Catalog, and FeatureCollection.

    Args:
        data (dict): The STAC data dictionary

    Returns:
        str: The asset type in uppercase (e.g., 'ITEM', 'COLLECTION', 'FEATURECOLLECTION', 'CATALOG')
             or an empty string if the type cannot be determined.
    """
    if not isinstance(data, dict):
        return ""

    # Check for STAC Item types
    if data.get("type") == "Feature":
        return "ITEM"
    elif data.get("type") == "FeatureCollection":
        return "FEATURECOLLECTION"
    elif data.get("type") == "Collection":
        return "COLLECTION"

    # For STAC Catalog/Collection without explicit type or with older STAC versions
    if "stac_version" in data and "id" in data:
        if data.get("type") == "Catalog":
            return "CATALOG"
        # If type is not explicitly set, determine based on structure
        if "extent" in data and "links" in data:
            return "COLLECTION"
        return "CATALOG"

    # If we can't determine the type
    return ""


def handle_output(
    output_file: str, callback: Callable[[], None], output_path: str = None
) -> None:
    """Helper function to handle output redirection to a file or stdout.

    Args:
        output_file: Path to the output file, or None to use stdout
        callback: Function that performs the actual output generation
        output_path: Optional path to display in the success message
    """

    if output_file:
        with open(output_file, "w") as f:
            with contextlib.redirect_stdout(f):
                callback()
        click.secho(
            f"Output written to {output_path or output_file}",
            fg="green",
            err=True,
            bold=True,
        )
        click.secho()
    else:
        callback()


def format_verbose_error(error_data):
    """Format verbose error data into a human-readable string."""
    if not error_data or not isinstance(error_data, dict):
        return str(error_data)

    output = []

    # Handle validator type
    if "validator" in error_data:
        output.append(f"Validator: {error_data['validator']}")

    # Handle schema information if available
    if "schema" in error_data and error_data["schema"]:
        output.append("\nSchema Information:")
        if isinstance(error_data["schema"], list):
            for schema in error_data["schema"]:
                if isinstance(schema, dict):
                    if "$comment" in schema:
                        output.append(f"- {schema['$comment']}")
                    if "required" in schema:
                        output.append(
                            f"  Required fields: {', '.join(schema['required'])}"
                        )
                    # Handle nested schema requirements
                    if "properties" in schema and "properties" in schema.get(
                        "properties", {}
                    ):
                        props = schema["properties"]["properties"]
                        if "allOf" in props:
                            for item in props["allOf"]:
                                if "anyOf" in item:
                                    for req in item["anyOf"]:
                                        if "required" in req:
                                            output.append(
                                                f"  One of these fields is required: {', '.join(req['required'])}"
                                            )

    # Handle path information if available
    if "path_in_schema" in error_data and error_data["path_in_schema"]:
        output.append(
            f"\nError Path: {' -> '.join(str(p) for p in error_data['path_in_schema'])}"
        )

    # Handle any other fields we haven't specifically formatted
    other_fields = set(error_data.keys()) - {
        "validator",
        "schema",
        "path_in_schema",
        "path_in_document",
    }
    for field in other_fields:
        if isinstance(error_data[field], (str, int, float, bool)):
            output.append(f"\n{field.replace('_', ' ').title()}: {error_data[field]}")

    return "\n".join(output)
