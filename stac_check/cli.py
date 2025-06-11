import importlib.metadata

import click

from .lint import Linter
from .logo import logo


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


def recursive_message(linter: Linter) -> None:
    """Displays messages related to the recursive validation of assets in a collection or catalog.

    Args:
        linter: An instance of the Linter class.

    Returns:
        None.
    """
    click.secho()
    click.secho("Recursive: Validate all assets in a collection or catalog", bold=True)
    click.secho(f"Max-depth = {linter.max_depth}")
    click.secho("-------------------------")
    for count, msg in enumerate(linter.validate_all):
        click.secho(
            f"Asset {count + 1} Validated: {msg['path']}", bg="white", fg="black"
        )
        click.secho()
        if msg["valid_stac"] == True:
            recursive_linter = Linter(msg["path"], recursive=True)
            cli_message(recursive_linter)
        else:
            click.secho(f"Valid: {msg['valid_stac']}", fg="red")
            click.secho("Schemas validated: ", fg="blue")
            for schema in msg["schema"]:
                click.secho(f"    {schema}")
            click.secho(f"Error Type: {msg['error_type']}", fg="red")
            click.secho(f"Error Message: {msg['error_message']}", fg="red")
        click.secho("-------------------------")


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
    click.secho(logo)

    click.secho("stac-check: STAC spec validation and linting tool", bold=True)

    click.secho()

    if linter.version == "1.1.0":
        click.secho(linter.set_update_message(), fg="green")
    else:
        click.secho(linter.set_update_message(), fg="red")

    click.secho()

    click.secho(
        f"Validator: stac-validator {linter.validator_version}", bg="blue", fg="white"
    )

    # Always show validation method
    validation_method = (
        "Pydantic" if hasattr(linter, "pydantic") and linter.pydantic else "JSONSchema"
    )
    click.secho()
    click.secho(f"Validation method: {validation_method}", bg="yellow", fg="black")

    click.secho()


def cli_message(linter: Linter) -> None:
    """Prints various messages about the STAC object being validated.

    Args:
        linter: The `Linter` object containing information about
        the STAC object to be validated.

    Returns:
        None
    """
    if linter.valid_stac == True:
        click.secho(f"Valid {linter.asset_type}: {linter.valid_stac}", fg="green")
    else:
        click.secho(f"Valid {linter.asset_type}: {linter.valid_stac}", fg="red")

    """ schemas validated for core object """
    click.secho()

    # Determine if we're using Pydantic validation
    using_pydantic = hasattr(linter, "pydantic") and linter.pydantic

    # For Pydantic validation, always show the appropriate schema model
    if using_pydantic:
        click.secho("Schemas validated: ", fg="blue")
        asset_type = linter.asset_type.capitalize() if linter.asset_type else "Item"
        click.secho(f"    stac-pydantic {asset_type} model")
    # For JSONSchema validation or when schemas are available
    elif len(linter.schema) > 0:
        click.secho("Schemas validated: ", fg="blue")
        for schema in linter.schema:
            click.secho(f"    {schema}")

    """ best practices message"""
    click.secho()
    for message in linter.best_practices_msg:
        if message == linter.best_practices_msg[0]:
            click.secho(message, bg="blue")
        else:
            click.secho(message, fg="red")

    """ geometry validation errors """
    if linter.geometry_errors_msg:
        click.secho()
        for message in linter.geometry_errors_msg:
            if message == linter.geometry_errors_msg[0]:
                click.secho(message, bg="yellow", fg="black")
            else:
                click.secho(message, fg="red")

    if linter.validate_all == True:
        click.secho()
        click.secho("Recursive validation has passed!", fg="blue")
    elif linter.validate_all == False and linter.recursive:
        click.secho()
        click.secho("Recursive validation has failed!", fg="red")

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

    if linter.error_type != "":
        click.secho("Validation error type: ", fg="red")
        click.secho(f"    {linter.error_type}")

    if linter.error_msg != "":
        click.secho("Validation error message: ", fg="red")
        click.secho(f"    {linter.error_msg}")

    click.secho(f"This object has {len(linter.data['links'])} links")

    click.secho()

    # Stac validator response for reference
    # click.secho(json.dumps(linter.message, indent=4))


@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Recursively validate all related stac objects.",
)
@click.option(
    "--max-depth",
    "-m",
    type=int,
    help="Maximum depth to traverse when recursing. Omit this argument to get full recursion. Ignored if `recursive == False`.",
)
@click.option(
    "-a", "--assets", is_flag=True, help="Validate assets for format and response."
)
@click.option(
    "-l", "--links", is_flag=True, help="Validate links for format and response."
)
@click.option(
    "--no-assets-urls",
    is_flag=True,
    help="Disables the opening of href links when validating assets (enabled by default).",
)
@click.option(
    "--header",
    type=(str, str),
    multiple=True,
    help="HTTP header to include in the requests. Can be used multiple times.",
)
@click.option(
    "--pydantic",
    is_flag=True,
    help="Use pydantic validation (requires stac-pydantic to be installed).",
)
@click.command()
@click.argument("file")
@click.version_option(version=importlib.metadata.distribution("stac-check").version)
def main(file, recursive, max_depth, assets, links, no_assets_urls, header, pydantic):
    # Check if pydantic validation is requested but not installed
    if pydantic:
        try:
            importlib.import_module("stac_pydantic")
        except ImportError:
            click.secho(
                "Warning: stac-pydantic is not installed. Pydantic validation will be disabled.\n"
                "To enable pydantic validation, install it with: pip install stac-check[pydantic]",
                fg="yellow",
            )
            pydantic = False

    linter = Linter(
        file,
        assets=assets,
        links=links,
        recursive=recursive,
        max_depth=max_depth,
        assets_open_urls=not no_assets_urls,
        headers=dict(header),
        pydantic=pydantic,
    )
    intro_message(linter)
    if recursive > 0:
        recursive_message(linter)
    else:
        cli_message(linter)
