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


def detect_api_response_type(file: str, headers: dict = None) -> Optional[str]:
    """Detect if a file or URL is a STAC API list response.

    Args:
        file: Path or URL to the file
        headers: Optional HTTP headers for URL requests

    Returns:
        "item_collection" for a FeatureCollection with features,
        "collections" for a collections endpoint response,
        None otherwise
    """
    try:
        if is_valid_url(file):
            resp = requests.get(file, headers=headers or {})
            data = resp.json()
        else:
            with open(file) as f:
                data = json.load(f)
    except Exception:
        # If we can't determine, return None
        return None

    if not isinstance(data, dict):
        return None
    if (
        data.get("type") == "FeatureCollection"
        and isinstance(data.get("features"), list)
        and len(data["features"]) > 0
    ):
        return "item_collection"
    if isinstance(data.get("collections"), list) and len(data["collections"]) > 0:
        return "collections"
    if isinstance(data.get("catalogs"), list) and len(data["catalogs"]) > 0:
        return "catalogs"
    return None


def is_item_collection(file: str, headers: dict = None) -> bool:
    """Detect if a file is an item collection (FeatureCollection with features).

    Args:
        file: Path or URL to the file
        headers: Optional HTTP headers for URL requests

    Returns:
        True if the file is an item collection, False otherwise
    """
    return detect_api_response_type(file, headers) == "item_collection"


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
    "--catalogs",
    is_flag=True,
    help="Validate catalogs endpoint response (STAC API catalogs extension). Can be combined with --pages. Defaults to one page.",
)
@click.option(
    "--pages",
    "-p",
    type=int,
    help="Maximum number of pages to validate per paginated list — with --item-collection/--collections/--catalogs or --recursive (default: one page per list; 0 for all pages).",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Recursively validate all related stac objects. Can be combined with --fast for stac-valid FastValidator validation.",
)
@click.option(
    "--max-depth",
    "-m",
    type=int,
    help="Maximum depth to traverse when recursing. Omit this argument to get full recursion. Ignored if `recursive == False` or in fast mode.",
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
    help="Show per-asset validation details; without it only a summary is printed.",
)
@click.option(
    "--fast",
    is_flag=True,
    help="Skip linting and geometry checks for maximum validation speed. Also applies to --recursive.",
)
@click.command()
@click.argument("file")
@click.version_option(version=importlib.metadata.distribution("stac-check").version)
def main(
    file: str,
    collections: bool,
    item_collection: bool,
    catalogs: bool,
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
        catalogs: Validate a catalogs endpoint (STAC API catalogs extension)
        pages: Number of pages to validate (for API endpoints)
        recursive: Recursively validate linked STAC objects
        max_depth: Maximum depth for recursive validation
        assets: Validate assets
        links: Validate links
        no_assets_urls: Disable URL validation for assets
        header: Additional HTTP headers
        pydantic: Use stac-pydantic for validation
        verbose: Show verbose output
        output: Save output to file (only with --collections, --item-collection, --catalogs, or --recursive)
        fast: Skip linting and geometry checks for maximum validation speed
    """
    # Check if output is used without a multi-asset mode
    if output and not any([collections, item_collection, catalogs, recursive]):
        click.echo(
            "Error: --output can only be used with --collections, --item-collection, --catalogs, or --recursive",
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

    # Auto-detect API list responses if no explicit flag is set
    if not collections and not item_collection and not catalogs and not recursive:
        detected = detect_api_response_type(file, headers=dict(header))
        if detected == "item_collection":
            item_collection = True
        elif detected == "collections":
            collections = True
        elif detected == "catalogs":
            catalogs = True

    if collections or item_collection or catalogs:
        # Handle API-based validation (collections, item collections, catalogs)
        object_list_key = (
            "collections" if collections else "catalogs" if catalogs else "features"
        )
        api_linter = ApiLinter(
            source=file,
            object_list_key=object_list_key,
            pages=pages if pages is not None else 1,
            headers=dict(header),
            verbose=verbose,
            fast=fast,
        )
        try:
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
        except (OSError, ValueError, requests.exceptions.RequestException) as e:
            click.secho(f"Error: {e}", fg="red", err=True)
            sys.exit(1)

        if not results:
            if api_linter.mismatched_list_key:
                suggested = {
                    "features": "--item-collection",
                    "collections": "--collections",
                    "catalogs": "--catalogs",
                }[api_linter.mismatched_list_key]
                click.secho(
                    f"Error: no '{api_linter.object_list_key}' objects found in "
                    f"{file}; the response contains "
                    f"'{api_linter.mismatched_list_key}' — did you mean {suggested}?",
                    fg="red",
                    err=True,
                )
                sys.exit(1)
            click.secho(
                f"Warning: no '{api_linter.object_list_key}' objects found in "
                f"{file}; nothing was validated.",
                fg="yellow",
                err=True,
            )
            sys.exit(0)

        # Show intro message in the terminal
        intro_message(display_linter)

        # Define output generation function (without intro message since we already showed it)
        def generate_output():
            if collections or catalogs:
                collections_message(
                    api_linter,
                    results=results,
                    cli_message_func=cli_message,
                    verbose=verbose,
                    title=(
                        "Catalogs: Validate all catalogs in a STAC API"
                        if catalogs
                        else "Collections: Validate all collections in a STAC API"
                    ),
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
        try:
            linter = Linter(
                file,
                assets=assets,
                links=links,
                recursive=recursive,
                max_depth=max_depth,
                pages=pages,
                assets_open_urls=not no_assets_urls,
                headers=dict(header),
                pydantic=pydantic,
                verbose=verbose,
                fast=fast,
            )
        except FileNotFoundError:
            click.secho(f"Error: file not found: {file}", fg="red", err=True)
            sys.exit(1)
        except json.JSONDecodeError as e:
            click.secho(f"Error: invalid JSON in {file}: {e}", fg="red", err=True)
            sys.exit(1)
        except (OSError, ValueError, requests.exceptions.RequestException) as e:
            click.secho(f"Error: {e}", fg="red", err=True)
            sys.exit(1)

        intro_message(linter)

        # Define output generation function (without intro message since we already showed it)
        def generate_output():
            if recursive:
                recursive_message(linter, cli_message_func=cli_message, verbose=verbose)
            elif fast:
                # For fast mode, use item_collection_message to show compact summary
                # even for single items
                from stac_check.display_messages import _display_fast_validation_summary

                result = {
                    "path": file,
                    "valid_stac": linter.valid_stac,
                    "asset_type": linter.asset_type,
                    "version": linter.version,
                    "validation_method": "stac-valid FastValidator",
                    "error_type": linter.error_type,
                    "error_message": linter.error_msg,
                    "best_practices": linter.best_practices_msg,
                    "geometry_errors": linter.geometry_errors_msg,
                    "schema": linter.schema,
                    "original_object": linter.data,
                }
                results = [result]
                _display_fast_validation_summary(
                    results,
                    total_time=(
                        linter.total_time if hasattr(linter, "total_time") else 0
                    ),
                    schemas=(
                        linter.schemas_checked
                        if hasattr(linter, "schemas_checked")
                        else None
                    ),
                )
            else:
                cli_message(linter)

        # Handle output (without duplicating the intro message)
        handle_output(output if recursive else None, generate_output)

        valid = linter.valid_stac
        if recursive:
            valid = valid and all(
                msg.get("valid_stac") is True for msg in linter.validate_all
            )
        sys.exit(0 if valid else 1)
