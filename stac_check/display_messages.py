import re
from typing import Any, Callable, Dict, List, Optional

import click

from stac_check.api_lint import ApiLinter
from stac_check.lint import Linter
from stac_check.logo import logo
from stac_check.utilities import format_verbose_error

__all__ = [
    "cli_message",
    "intro_message",
    "recursive_message",
    "item_collection_message",
    "collections_message",
    "link_asset_message",
]


def link_asset_message(
    link_list: list, type: str, format: str, healthy_msg: bool
) -> None:
    """Prints a list of links or assets and any errors associated with them.

    Args:
        link_list (list): A list of links or assets.
        type (str): The type of link or asset being processed.
        format (str): The format or request being used.
        healthy_msg (bool): Whether to display "No TYPE errors!" or not

    Returns:
        None.
    """
    if len(link_list) > 0:
        click.secho(f"{type.upper()} {format} errors: ", fg="red")
        for asset in link_list:
            click.secho(f"    {asset}")
    elif healthy_msg:
        click.secho(f"No {type.upper()} {format} errors!", fg="green")


def _display_validation_status(linter: Linter) -> None:
    """Display the validation status of the STAC object.

    Args:
        linter: The Linter object containing validation results
    """
    status_color = "green" if linter.valid_stac else "red"
    click.secho(
        f"{linter.asset_type} Passed: {linter.valid_stac}", fg=status_color, bold=True
    )


def _display_schemas(linter: Linter) -> None:
    """Display the schemas that were validated against.

    Args:
        linter: The Linter object containing schema information
    """
    click.secho()
    if hasattr(linter, "pydantic") and linter.pydantic:
        click.secho("Schemas checked: ", fg="blue")
        asset_type = linter.asset_type.capitalize() if linter.asset_type else "Item"
        click.secho(f"    stac-pydantic {asset_type} model")
    elif len(linter.schema) > 0:
        click.secho("Schemas checked: ", fg="blue")
        for schema in linter.schema:
            click.secho(f"    {schema}")
    click.secho()


def _display_failed_schema(linter: Linter) -> None:
    """Display failed schema information if any.

    Args:
        linter: The Linter object containing schema information
    """
    if linter.failed_schema:
        click.secho("Failed Schema: ", fg="blue")
        click.secho(f"    {linter.failed_schema}")
        click.secho()


def _display_recommendation(linter: Linter) -> None:
    """Display recommendations if any.

    Args:
        linter: The Linter object containing recommendation information
    """
    if linter.recommendation:
        click.secho("Recommendation: ", fg="blue")
        click.secho(f"    {linter.recommendation}")


def _display_best_practices(linter: Linter) -> None:
    """Display best practices messages.

    Args:
        linter: The Linter object containing best practices information
    """
    if linter.best_practices_msg:
        click.secho("\n " + linter.best_practices_msg[0], bg="blue")
        click.secho()
        for message in linter.best_practices_msg[1:]:
            click.secho(message, fg="black")


def _display_geometry_errors(linter: Linter) -> None:
    """Display geometry validation errors.

    Args:
        linter: The Linter object containing geometry error information
    """
    # Skip geometry errors display in fast mode
    if hasattr(linter, "fast") and linter.fast:
        return

    if linter.geometry_errors_msg:
        click.secho("\n " + linter.geometry_errors_msg[0], bg="magenta", fg="black")
        click.secho()
        for message in linter.geometry_errors_msg[1:]:
            click.secho(message, fg="black")


def _display_recursive_validation(linter: Linter) -> None:
    """Display recursive validation status.

    Args:
        linter: The Linter object containing recursive validation information
    """
    if linter.validate_all is True:
        click.secho("\nRecursive validation has passed!", fg="blue")
    elif linter.validate_all is False and linter.recursive:
        click.secho("\nRecursive validation has failed!", fg="red")


def _display_asset_validation(linter: Linter) -> None:
    """Display asset and link validation results.

    Args:
        linter: The Linter object containing asset validation information
    """
    if linter.invalid_asset_format is not None:
        click.secho()
        link_asset_message(linter.invalid_asset_format, "asset", "format", True)

    if linter.invalid_asset_request is not None:
        click.secho()
        link_asset_message(
            linter.invalid_asset_request, "asset", "request", linter.assets_open_urls
        )

    if linter.invalid_link_format is not None:
        click.secho()
        link_asset_message(linter.invalid_link_format, "link", "format", True)

    if linter.invalid_link_request is not None:
        click.secho()
        link_asset_message(linter.invalid_link_request, "link", "request", True)
        click.secho()


def _display_errors(linter: Linter) -> None:
    """Display any validation errors.

    Args:
        linter: The Linter object containing error information
    """
    click.secho()
    if linter.error_type:
        click.secho("\n Validation Errors: ", fg="white", bold=True, bg="black")
        click.secho()
        click.secho("Validation error type: ", fg="red")
        click.secho(f"    {linter.error_type}")
        click.secho()

    if linter.error_msg:
        click.secho("Validation error message: ", fg="red")
        click.secho(f"    {linter.error_msg}")


def _display_verbose_output(linter: Linter) -> None:
    """Display verbose error output if available.

    Args:
        linter: The Linter object containing verbose error information
    """
    if linter.verbose_error_msg:
        click.secho("\n Verbose Validation Output: ", fg="white", bg="cyan")
        click.secho()
        if isinstance(linter.verbose_error_msg, dict):
            formatted_error = format_verbose_error(linter.verbose_error_msg)
        else:
            formatted_error = str(linter.verbose_error_msg)
        click.secho(formatted_error)
        click.secho()


def _display_additional_info(linter: Linter) -> None:
    """Display additional information about the STAC object.

    Args:
        linter: The Linter object containing STAC data
    """
    click.secho("\n Additional Information: ", bg="green", fg="white")
    click.secho()
    if hasattr(linter, "data") and "links" in linter.data:
        click.secho(f"This object has {len(linter.data['links'])} links", bold=True)
    else:
        click.secho("No links found in the STAC object", bold=True)


def _display_disclaimer() -> None:
    """Display the STAC validation disclaimer."""
    click.secho()
    click.secho(
        "Disclaimer: Schema-based STAC validation may be incomplete and should only be considered as a first indicator of validity.\n"
        "See: https://github.com/radiantearth/stac-spec/discussions/1242"
    )
    click.secho()


def _display_fast_validation_summary(
    results: List[Dict[str, Any]],
    total_time: float = 0.0,
    schemas: Optional[List[str]] = None,
) -> None:
    """Display a compact validation summary for fast mode with large datasets.

    Args:
        results: List of validation result dictionaries
        total_time: Total validation time in milliseconds
        schemas: List of schemas that were checked
    """
    passed = 0
    failed = []
    error_registry: Dict[str, List[str]] = {}
    best_practices_issues: List[tuple] = []

    for result in results:
        if result.get("valid_stac"):
            passed += 1
        else:
            failed.append(result)
            # Group errors by message
            error_msg = result.get("error_message", "Unknown error")
            if error_msg not in error_registry:
                error_registry[error_msg] = []
            # Extract item ID from path
            path = result.get("path", "unknown")
            item_id = path.split("/")[-1] if "/" in path else path
            error_registry[error_msg].append(item_id)

        # Collect best practices issues (filter out empty/base messages)
        best_practices = result.get("best_practices", [])
        if best_practices:
            # Filter out the base string and empty messages
            filtered_practices = [
                msg
                for msg in best_practices
                if msg and msg.strip() and msg.strip() != "STAC Best Practices:"
            ]
            if filtered_practices:
                path = result.get("path", "unknown")
                best_practices_issues.append((path, filtered_practices))

    click.secho()
    click.secho("\n Validation Summary", bold=True, bg="black", fg="white")
    click.secho()
    click.secho(f"✅ Passed: {passed}/{len(results)}")

    if len(failed) > 0:
        click.secho(f"❌ Failed: {len(failed)}/{len(results)}", fg="red")

    if total_time > 0:
        click.secho()
        click.secho("⚡ Timing Information:", bold=True, fg="cyan")
        click.secho(f"  Total Validation Time: {total_time:.2f} ms")
        if len(results) > 0:
            avg_time = total_time / len(results)
            click.secho(f"  Average per Object: {avg_time:.3f} ms")

    # Display schemas checked
    if schemas and len(schemas) > 0:
        click.secho()
        click.secho("Schemas checked:", bold=True)
        for schema in schemas:
            click.secho(f"    {schema}")

    # Display grouped errors
    if error_registry:
        click.secho()
        click.secho("\n Validation Errors", bg="red", fg="white")
        click.secho()
        for err_msg, affected_ids in error_registry.items():
            count = len(affected_ids)
            click.secho(f"❌ {err_msg}", fg="red")
            sample_ids = ", ".join(affected_ids[:3])
            if count > 3:
                sample_ids += f" ... (and {count - 3} more)"
            click.secho(
                f"   Affected Items: {count} | Examples: {sample_ids}", fg="red"
            )
            click.secho()

    # Display best practices issues (grouped by message type)
    if best_practices_issues:
        click.secho()
        click.secho("\n Best Practices Warnings", bg="blue", fg="white")
        click.secho()

        # Group best practices by message type (normalize item-specific messages)
        practices_registry: Dict[str, List[str]] = {}
        for path, messages in best_practices_issues:
            # Extract item ID from path
            item_id = path.split("/")[-1] if "/" in path else path
            for msg in messages:
                # Normalize messages that contain item IDs to group them together
                # e.g., "Item name 'S2B_1CCV_20200317_0_L2A' should only contain..."
                # becomes "Item name should only contain Searchable identifiers"
                normalized_msg = msg
                # Replace specific item names with generic placeholder
                normalized_msg = re.sub(
                    r"Item name '[^']+' should", "Item name should", normalized_msg
                )

                if normalized_msg not in practices_registry:
                    practices_registry[normalized_msg] = []
                practices_registry[normalized_msg].append(item_id)

        # Display grouped best practices
        for practice_msg, affected_ids in practices_registry.items():
            count = len(affected_ids)
            click.secho(f"⚠️  {practice_msg}", fg="blue")
            sample_ids = ", ".join(affected_ids[:3])
            if count > 3:
                sample_ids += f" ... (and {count - 3} more)"
            click.secho(
                f"   Affected Items: {count} | Examples: {sample_ids}", fg="blue"
            )
            click.secho()

    click.secho()


def _display_validation_summary(
    results: List[Dict[str, Any]],
    verbose: bool = False,
    fast: bool = False,
    total_time: float = 0.0,
) -> None:
    """Display a summary of validation results, including warnings and best practice issues.

    Args:
        results: List of validation result dictionaries
        verbose: Whether to show detailed output
        fast: Whether fast mode is enabled (for compact output and timing display)
        total_time: Total validation time in milliseconds (for fast mode)
    """
    passed = 0
    failed = []
    warnings = []
    all_paths = []
    total_setup_time = 0.0
    total_exec_time = 0.0
    error_registry: Dict[str, List[str]] = {}

    for result in results:
        path = result.get("path", "unknown")
        all_paths.append(path)

        # Check for validation status
        if result.get("valid_stac"):
            passed += 1
        else:
            failed.append(path)
            # Group errors by message for fast mode
            error_msg = result.get("error_message", "Unknown error")
            if error_msg not in error_registry:
                error_registry[error_msg] = []
            # Extract item ID from path
            item_id = path.split("/")[-1] if "/" in path else path
            error_registry[error_msg].append(item_id)

        # Check for best practice warnings in the result
        best_practices = []
        if result.get("best_practices"):
            best_practices = [
                p
                for p in result["best_practices"]
                if p and p.strip() and p != "STAC Best Practices: "
            ]
        # Also check for best practices in the message if it exists
        elif (
            result.get("message")
            and isinstance(result["message"], dict)
            and result["message"].get("best_practices")
        ):
            best_practices = [
                p
                for p in result["message"]["best_practices"]
                if p and p.strip() and p != "STAC Best Practices: "
            ]

        # Only add to warnings if there are actual messages
        if best_practices:
            warnings.append((path, best_practices))

        # Accumulate timing information if available
        if fast and result.get("fast_setup_time"):
            try:
                setup_str = result.get("fast_setup_time", "0").split()[0]
                total_setup_time += float(setup_str)
            except (ValueError, IndexError):
                pass
        if fast and result.get("fast_exec_time"):
            try:
                exec_str = result.get("fast_exec_time", "0").split()[0]
                total_exec_time += float(exec_str)
            except (ValueError, IndexError):
                pass

    # Use fast validation summary for fast mode
    if fast:
        # Collect all unique schemas from results
        all_schemas = set()
        for result in results:
            if result.get("schema"):
                all_schemas.update(result.get("schema", []))
        schemas_list = sorted(list(all_schemas)) if all_schemas else None
        _display_fast_validation_summary(results, total_time, schemas_list)
    else:
        # Standard output for non-fast mode or small datasets
        click.secho("\n Validation Summary", bold=True, bg="black", fg="white")
        click.secho()
        click.secho(f"✅ Passed: {passed}/{len(all_paths)}")

        if failed:
            click.secho(f"❌ Failed: {len(failed)}/{len(all_paths)}", fg="red")
            click.secho("\nFailed Assets:", fg="red")
            for path in failed:
                click.secho(f"  - {path}")

        if warnings:
            click.secho(
                f"\n⚠️  Best Practice Warnings ({len(warnings)} assets)", fg="yellow"
            )
            if verbose or len(warnings) <= 12:
                for path, msgs in warnings:
                    click.secho(f"\n  {path}:", fg="yellow")
                    for msg in msgs:
                        click.secho(f"    • {msg}", fg="yellow")
            else:
                click.secho("  (Use --verbose to see details)", fg="yellow")

        click.secho(f"\n🔍 All {len(all_paths)} Assets Checked")
        if verbose or len(all_paths) <= 12:
            for path in all_paths:
                click.secho(f"  - {path}")
        else:
            click.secho("  (Use --verbose to see all assets)", fg="yellow")

        # Display timing information if in fast mode
        if fast and (total_setup_time > 0 or total_exec_time > 0):
            click.secho()
            click.secho("⚡ FastValidator Timing:", bold=True, fg="cyan")
            click.secho(f"  Total Setup Time: {total_setup_time:.2f} ms")
            click.secho(f"  Total Execution Time: {total_exec_time:.2f} ms")
            if len(all_paths) > 0:
                avg_time = total_exec_time / len(all_paths)
                click.secho(f"  Average per Item: {avg_time:.3f} ms")

        click.secho()


def _display_validation_results(
    results: List[Dict[str, Any]],
    title: str,
    metadata: Optional[Dict[str, Any]] = None,
    cli_message_func: Optional[Callable[[Linter], None]] = None,
    create_linter_func: Optional[Callable[[Dict[str, Any]], Linter]] = None,
    verbose: bool = False,
    fast: bool = False,
    total_time: float = 0.0,
) -> None:
    """Shared helper function to display validation results consistently.

    This function handles the common logic for displaying validation results from
    different sources (item collections, recursive validation, collections, etc.).
    It displays a header with metadata, iterates through results, and attempts to
    create Linter instances for consistent display.

    Args:
        results: List of validation result dictionaries to display
        title: Title to display at the top of the results
        metadata: Optional dictionary of metadata to display (e.g., pages, max-depth)
        cli_message_func: Function to use for displaying validation messages
        create_linter_func: Function to create a Linter instance from a result item
                           Should take a result dict and return a Linter instance

    Returns:
        None
    """
    if cli_message_func is None:
        cli_message_func = cli_message

    # In fast mode with many items, show first 5 items then silence
    show_all_items = not (fast and len(results) > 20)
    items_shown = 0
    max_items_to_show = 5

    if show_all_items:
        click.secho()
        click.secho(title, bold=True)

        # Display any metadata provided
        if metadata:
            for key, value in metadata.items():
                click.secho(f"{key} = {value}")

        click.secho("-------------------------")

    for count, msg in enumerate(results):
        # In fast mode with many items, show only first 5 then silence
        if not show_all_items and items_shown >= max_items_to_show:
            if items_shown == max_items_to_show:
                click.secho(
                    "... silencing output for remaining items (validating at maximum speed) ...",
                    dim=True,
                )
            items_shown += 1
            continue

        if show_all_items:
            # Get the path or use a fallback
            path = msg.get("path", f"(unknown-{count + 1})")
            click.secho(f"\n Asset {count + 1}: {path}", bg="white", fg="black")
            click.secho()

            try:
                # Try to create a Linter instance using the provided function
                if create_linter_func:
                    item_linter = create_linter_func(msg)

                    # If create_linter_func returns None (for recursive validation), use fallback
                    if item_linter is None:
                        _display_fallback_message(msg)
                    else:
                        # Set validation status and error info for invalid items
                        if not msg.get("valid_stac", True):
                            item_linter.valid_stac = False
                            item_linter.error_type = msg.get("error_type")
                            item_linter.error_msg = msg.get("error_message")

                        # Ensure best practices are included in the result
                        if (
                            hasattr(item_linter, "best_practices_msg")
                            and item_linter.best_practices_msg
                        ):
                            # Skip the first line which is just the header
                            bp_msgs = [
                                msg
                                for msg in item_linter.best_practices_msg[1:]
                                if msg.strip()
                            ]
                            if bp_msgs:
                                msg["best_practices"] = bp_msgs

                        # Display using the provided message function
                        cli_message_func(item_linter)
                else:
                    # No linter creation function provided, use fallback
                    _display_fallback_message(msg)
            except Exception as e:
                # Fall back to basic display if creating the Linter fails
                _display_fallback_message(msg, e)

            click.secho("-------------------------")
        else:
            items_shown += 1

    # Display summary at the end for better visibility with many items
    _display_validation_summary(
        results, verbose=verbose, fast=fast, total_time=total_time
    )


def item_collection_message(
    linter: ApiLinter,
    results: Optional[List[Dict[str, Any]]] = None,
    cli_message_func: Optional[Callable[[Linter], None]] = None,
    verbose: bool = False,
) -> None:
    """Displays messages related to the validation of assets in a feature collection.

    This function processes validation results from an ApiLinter and displays them in a
    consistent format. For each item in the collection, it attempts to create a Linter
    instance from the original object data and use cli_message_func for display. If that
    fails, it falls back to a simpler display using _display_fallback_message.

    The function handles both valid and invalid STAC items consistently, ensuring that
    error information, best practices, and geometry errors are displayed appropriately.

    Args:
        linter: An instance of the ApiLinter class that performed the validation.
        results: Optional pre-computed lint results. If None, will call linter.lint_all().
        cli_message_func: The cli_message function to use for item validation.
                         If None, will use the default cli_message from this module.

    Returns:
        None.
    """
    if results is None:
        results = linter.lint_all()

    # In fast mode, use compact display
    if linter.fast:
        schemas = linter.schemas_checked if hasattr(linter, "schemas_checked") else None
        _display_fast_validation_summary(results, linter.total_time, schemas)
        return

    # Define a function to create Linter instances from API results
    def create_api_linter(msg):
        if msg.get("original_object"):
            return Linter(msg.get("original_object"), fast=linter.fast)
        raise ValueError("No original object available")

    # Display the results using the shared helper
    _display_validation_results(
        results=results,
        title="Item Collection: Validate all assets in a feature collection",
        metadata={"Pages": linter.pages},
        cli_message_func=cli_message_func,
        create_linter_func=create_api_linter,
        verbose=verbose,
        fast=linter.fast,
        total_time=linter.total_time,
    )


def _display_fallback_message(
    msg: Dict[str, Any], error: Optional[Exception] = None
) -> None:
    """Display a fallback message when a Linter instance cannot be created.

    This function provides a consistent way to display validation results when
    a proper Linter instance cannot be created. It shows validation status,
    schemas checked, error information, best practices, and geometry errors
    directly from the message dictionary.

    Args:
        msg: The message dictionary from ApiLinter results containing validation info
        error: Optional exception that occurred when trying to create a Linter
    """
    status_color = "green" if msg.get("valid_stac") else "red"
    click.secho(f"Valid: {msg.get('valid_stac')}", fg=status_color)

    click.secho("Schemas checked: ", fg="blue")
    for schema in msg.get("schema", []):
        click.secho(f"    {schema}")

    if not msg.get("valid_stac"):
        if msg.get("error_type"):
            click.secho("\nValidation error type: ", fg="red")
            click.secho(f"    {msg.get('error_type')}")

        if msg.get("error_message"):
            click.secho("\nValidation error message: ", fg="red")
            click.secho(f"    {msg.get('error_message')}")

    # Display error information if provided
    if error:
        click.secho(
            f"\nNote: Could not display detailed information. Error: {str(error)}",
            fg="yellow",
        )

    # Display best practices
    bp = msg.get("best_practices", [])
    # Filter out empty strings and the default "STAC Best Practices: " message
    bp = [p for p in bp if p and p.strip() and p != "STAC Best Practices: "]

    if bp:
        click.echo()
        click.secho("\nSTAC Best Practices: ", bg="blue")
        click.echo()
        for practice in bp:
            click.echo(f"    • {practice}", fg="black")
        # Update the best_practices in the message for the summary
        msg["best_practices"] = bp

    # Display geometry errors
    geo = msg.get("geometry_errors", [])
    if geo and len(geo) > 0:
        click.secho()
        click.secho("\n Geometry Validation Errors [BETA]: ", bg="magenta", fg="black")
        click.secho()
        for error in geo:
            if error:  # Skip empty strings
                click.secho(error, fg="black")

    click.secho("-------------------------")


def collections_message(
    linter: ApiLinter,
    results: Optional[List[Dict[str, Any]]] = None,
    cli_message_func: Optional[Callable[[Linter], None]] = None,
    verbose: bool = False,
) -> None:
    """Displays messages related to the validation of STAC collections from a collections endpoint.

    This function processes validation results from an ApiLinter targeting a collections endpoint
    and displays them in a consistent format. For each collection, it attempts to create a Linter
    instance from the original object data and use cli_message_func for display. If that fails, it
    falls back to a simpler display using _display_fallback_message.

    The function handles both valid and invalid STAC collections consistently, ensuring that
    error information, best practices, and other details are displayed appropriately.

    Args:
        linter: An instance of the ApiLinter class that performed the validation.
        results: Optional pre-computed lint results. If None, will call linter.lint_all().
        cli_message_func: The cli_message function to use for collection validation.
                         If None, will use the default cli_message from this module.

    Returns:
        None.
    """
    if results is None:
        results = linter.lint_all()

    # Define a function to create Linter instances from API results
    def create_collection_linter(msg):
        if msg.get("original_object"):
            return Linter(msg.get("original_object"), fast=linter.fast)
        raise ValueError("No original object available")

    # Display the results using the shared helper
    _display_validation_results(
        results=results,
        title="Collections: Validate all collections in a STAC API",
        metadata={"Pages": linter.pages},
        cli_message_func=cli_message_func,
        create_linter_func=create_collection_linter,
        verbose=verbose,
        fast=linter.fast,
        total_time=linter.total_time,
    )


def recursive_message(
    linter: Linter,
    cli_message_func: Optional[Callable[[Linter], None]] = None,
    verbose: bool = False,
) -> None:
    """Displays messages related to the recursive validation of assets in a collection or catalog.

    This function processes recursive validation results from a Linter and displays them in a
    consistent format. For each asset in the collection or catalog, it attempts to create a new
    Linter instance and use cli_message_func for display. If that fails, it falls back to a
    simpler display using _display_fallback_message.

    The function handles both valid and invalid STAC objects consistently, ensuring that
    error information is displayed appropriately for invalid items.

    Args:
        linter: An instance of the Linter class with recursive validation results.
        cli_message_func: The cli_message function to use for recursive validation.
                         If None, will use the default cli_message from this module.

    Returns:
        None.
    """

    # Define a function to create Linter instances from recursive results
    def create_recursive_linter(msg):
        return Linter(msg["path"], recursive=True)

    # Display the results using the shared helper
    _display_validation_results(
        results=linter.validate_all,
        title="Recursive: Validate all assets in a collection or catalog",
        metadata={"Max-depth": linter.max_depth},
        cli_message_func=cli_message_func,
        create_linter_func=create_recursive_linter,
        verbose=verbose,
    )


def cli_message(linter: Linter) -> None:
    """Prints various messages about the STAC object being validated.

    This function orchestrates the display of all validation information by calling
    multiple helper display functions in sequence. It shows validation status,
    schemas checked, errors, best practices, geometry errors, and other information.

    Args:
        linter: The `Linter` object containing information about
            the STAC object to be validated.
    """
    _display_validation_status(linter)
    _display_schemas(linter)
    _display_failed_schema(linter)
    _display_recommendation(linter)
    _display_errors(linter)
    _display_best_practices(linter)
    _display_geometry_errors(linter)
    _display_recursive_validation(linter)
    _display_asset_validation(linter)
    _display_verbose_output(linter)
    _display_additional_info(linter)
    _display_disclaimer()


def intro_message(linter: Linter) -> None:
    """Prints an introduction message for the stac-check tool.

    The message includes the stac-check logo, the name of the tool, the version
    of the STAC spec being validated, an update message, and the version of the
    stac-validator being used.

    Args:
        linter (object): An instance of the Linter class, which is used to
            obtain the version of the STAC spec being validated, the update
            message, and the version of the stac-validator being used.

    Returns:
        None.
    """
    click.secho(logo, fg="white")

    click.secho("stac-check: STAC spec validation and linting tool", bold=True)

    click.secho()

    if linter.version == "1.1.0":
        click.secho(linter.set_update_message(), fg="green")
    else:
        click.secho(linter.set_update_message(), fg="red")

    click.secho(
        f"\n Validator: stac-valid {linter.validator_version}",
        bold=True,
        bg="black",
        fg="white",
    )

    # Always show validation method
    if hasattr(linter, "fast") and linter.fast:
        validation_method = "FastJSONSchema"
    elif hasattr(linter, "pydantic") and linter.pydantic:
        validation_method = "Pydantic"
    else:
        validation_method = "JSONSchema"

    click.secho(f"\n Validation method: {validation_method}", bg="cyan", fg="white")

    click.secho()
