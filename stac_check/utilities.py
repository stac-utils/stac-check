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
