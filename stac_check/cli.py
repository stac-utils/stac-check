import importlib.metadata
import sys

import click

from stac_check.api_lint import ApiLinter
from stac_check.display_messages import (
    cli_message,
    collections_message,
    intro_message,
    item_collection_message,
    recursive_message,
)
from stac_check.lint import Linter


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
@click.command()
@click.argument("file")
@click.version_option(version=importlib.metadata.distribution("stac-check").version)
def main(
    file,
    collections,
    item_collection,
    pages,
    recursive,
    max_depth,
    assets,
    links,
    no_assets_urls,
    header,
    pydantic,
    verbose,
):
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

    if not collections and not item_collection:
        # Create a standard Linter for single file or recursive validation
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
        )
        intro_message(linter)
        # If recursive validation is enabled, use recursive_message
        if recursive:
            # Pass the cli_message function to avoid circular imports
            recursive_message(linter, cli_message_func=cli_message)
        else:
            # Otherwise, just display the standard CLI message
            cli_message(linter)

        sys.exit(0 if linter.valid_stac else 1)
    else:
        if item_collection:
            object_list_key = "features"
        elif collections:
            object_list_key = "collections"

        linter = ApiLinter(
            source=file,
            object_list_key=object_list_key,
            pages=pages,
            headers=dict(header),
        )
        results = linter.lint_all()
        intro_message(linter)
        if collections:
            collections_message(linter, results=results, cli_message_func=cli_message)
        elif item_collection:
            item_collection_message(
                linter, results=results, cli_message_func=cli_message
            )
        sys.exit(0 if all(msg.get("valid_stac") is True for msg in results) else 1)
