import importlib.metadata
import json
import sys
from typing import Optional

import click
import requests
from stac_validator.utilities import is_valid_url

from stac_check.api_lint import ApiLinter
from stac_check.display_messages import (
    cli_message,
    collections_message,
    intro_message,
    item_collection_message,
    recursive_message,
)
from stac_check.lint import Linter
from stac_check.utilities import handle_output


def is_item_collection(file: str, headers: dict = None) -> bool:
    """Detect if a file is an item collection (FeatureCollection with features).

    Args:
        file: Path or URL to the file
        headers: Optional HTTP headers for URL requests

    Returns:
        True if the file is an item collection, False otherwise
    """
    try:
        if is_valid_url(file):
            resp = requests.get(file, headers=headers or {})
            data = resp.json()
        else:
            with open(file) as f:
                data = json.load(f)

        # Check if it's a FeatureCollection with features
        return (
            isinstance(data, dict)
            and data.get("type") == "FeatureCollection"
            and "features" in data
            and isinstance(data.get("features"), list)
            and len(data.get("features", [])) > 0
        )
    except Exception:
        # If we can't determine, return False
        return False


@click.option(
    "--collections",
    is_flag=True,
    help="Validate collections endpoint response. Can be combined with --pages. Defaults to one page.",
)
@click.option(
    "--item-collection",
    is_flag=True,
    help="Validate item collection response. Can be combined with --pages. Defaults to one page.",
)
@click.option(
    "--pages",
    "-p",
    type=int,
    help="Maximum number of pages to validate via --item-collection or --collections. Defaults to one page.",
)
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
    "--output",
    "-o",
    type=click.Path(dir_okay=False, writable=True),
    help="Save output to the specified file. Only works with --collections, --item-collection, or --recursive.",
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
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output.",
)
@click.option(
    "--fast",
    is_flag=True,
    help="Use FastJSONSchema for high-speed validation. Skips best practices and geometry checks for maximum performance.",
)
@click.command()
@click.argument("file")
@click.version_option(version=importlib.metadata.distribution("stac-check").version)
def main(
    file: str,
    collections: bool,
    item_collection: bool,
    pages: Optional[int],
    recursive: bool,
    max_depth: Optional[int],
    assets: bool,
    links: bool,
    no_assets_urls: bool,
    header: tuple[tuple[str, str], ...],
    pydantic: bool,
    verbose: bool,
    output: Optional[str],
    fast: bool,
) -> None:
    """Main entry point for the stac-check CLI.

    Args:
        file: The STAC file or URL to validate
        collections: Validate a collections endpoint
        item_collection: Validate an item collection
        pages: Number of pages to validate (for API endpoints)
        recursive: Recursively validate linked STAC objects
        max_depth: Maximum depth for recursive validation
        assets: Validate assets
        links: Validate links
        no_assets_urls: Disable URL validation for assets
        header: Additional HTTP headers
        pydantic: Use stac-pydantic for validation
        verbose: Show verbose output
        output: Save output to file (only with --collections, --item-collection, or --recursive)
        fast: Fast validation mode (skips best practices and geometry checks)
    """
    # Check if output is used without --collections, --item-collection, or --recursive
    if output and not any([collections, item_collection, recursive]):
        click.echo(
            "Error: --output can only be used with --collections, --item-collection, or --recursive",
            err=True,
        )
        sys.exit(1)
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

    # Auto-detect item collection if no explicit flag is set
    if not collections and not item_collection and not recursive:
        if is_item_collection(file, headers=dict(header)):
            item_collection = True

    if collections or item_collection:
        # Handle API-based validation (collections or item collections)
        api_linter = ApiLinter(
            source=file,
            object_list_key="collections" if collections else "features",
            pages=pages if pages else 1,
            headers=dict(header),
            verbose=verbose,
            fast=fast,
        )
        results = api_linter.lint_all()

        # Create a dummy Linter instance for display purposes
        display_linter = Linter(
            file,
            assets=assets,
            links=links,
            headers=dict(header),
            pydantic=pydantic,
            verbose=verbose,
            fast=fast,
        )

        # Show intro message in the terminal
        intro_message(display_linter)

        # Define output generation function (without intro message since we already showed it)
        def generate_output():
            if collections:
                collections_message(
                    api_linter,
                    results=results,
                    cli_message_func=cli_message,
                    verbose=verbose,
                )
            elif item_collection:
                item_collection_message(
                    api_linter,
                    results=results,
                    cli_message_func=cli_message,
                    verbose=verbose,
                )

        # Handle output (without duplicating the intro message)
        handle_output(output, generate_output)
        sys.exit(0 if all(msg.get("valid_stac") is True for msg in results) else 1)
    else:
        # Handle file-based validation (single file or recursive)
        linter = Linter(
            file,
            assets=assets,
            links=links,
            recursive=recursive,
            max_depth=max_depth,
            assets_open_urls=not no_assets_urls,
            headers=dict(header),
            pydantic=pydantic,
            verbose=verbose,
            fast=fast,
        )

        intro_message(linter)

        # Define output generation function (without intro message since we already showed it)
        def generate_output():
            if recursive:
                recursive_message(linter, cli_message_func=cli_message, verbose=verbose)
            else:
                cli_message(linter)

        # Handle output (without duplicating the intro message)
        handle_output(output if recursive else None, generate_output)

        sys.exit(0 if linter.valid_stac else 1)
