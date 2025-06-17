import click

from stac_check.lint import Linter
from stac_check.logo import logo
from stac_check.utilities import format_verbose_error

__all__ = [
    "cli_message",
    "intro_message",
    "recursive_message",
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
        click.secho()
        click.secho("\n " + linter.best_practices_msg[0], bg="blue")
        click.secho()
        for message in linter.best_practices_msg[1:]:
            click.secho(message, fg="black")


def _display_geometry_errors(linter: Linter) -> None:
    """Display geometry validation errors.

    Args:
        linter: The Linter object containing geometry error information
    """
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


def recursive_message(linter: Linter, cli_message_func=None) -> None:
    """Displays messages related to the recursive validation of assets in a collection or catalog.

    Args:
        linter: An instance of the Linter class.
        cli_message_func: The cli_message function to use for recursive validation.
                         If None, will use the default cli_message from this module.

    Returns:
        None.
    """
    if cli_message_func is None:
        cli_message_func = cli_message

    click.secho()
    click.secho("Recursive: Validate all assets in a collection or catalog", bold=True)
    click.secho(f"Max-depth = {linter.max_depth}")
    click.secho("-------------------------")
    for count, msg in enumerate(linter.validate_all):
        click.secho(f"Asset {count + 1}: {msg['path']}", bg="white", fg="black")
        click.secho()
        if msg["valid_stac"] == True:
            recursive_linter = Linter(msg["path"], recursive=True)
            cli_message_func(recursive_linter)
        else:
            click.secho(f"Valid: {msg['valid_stac']}", fg="red")
            click.secho("Schemas checked: ", fg="blue")
            for schema in msg["schema"]:
                click.secho(f"    {schema}")
            click.secho(f"Error Type: {msg['error_type']}", fg="red")
            click.secho(f"Error Message: {msg['error_message']}", fg="red")
        click.secho("-------------------------")


def cli_message(linter: Linter) -> None:
    """Prints various messages about the STAC object being validated.

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
    click.secho(logo, bold=True, fg="bright_green")

    click.secho("stac-check: STAC spec validation and linting tool", bold=True)

    click.secho()

    if linter.version == "1.1.0":
        click.secho(linter.set_update_message(), fg="green")
    else:
        click.secho(linter.set_update_message(), fg="red")

    click.secho(
        f"\n Validator: stac-validator {linter.validator_version}",
        bold=True,
        bg="black",
        fg="white",
    )

    # Always show validation method
    validation_method = (
        "Pydantic" if hasattr(linter, "pydantic") and linter.pydantic else "JSONSchema"
    )

    click.secho(f"\n Validation method: {validation_method}", bg="cyan", fg="white")

    click.secho()
