import click
import json
from .lint.lint import Linter

def link_asset_message(link_list:list, type: str, format: str):
    if len(link_list) > 0:
        click.secho(f"{type.upper()} {format} errors: ", fg="red")
        for asset in link_list:
            click.secho(f"    {asset}")
    else:
        click.secho(f"No {type.upper()} {format} errors!", fg="green")

def cli_message(linter):
    click.secho()
    click.secho("stac-check: STAC spec validaton and linting tool", bold=True)
    if linter.version == "1.0.0":
        click.secho(linter.update_msg, fg='green')
    else:
        click.secho(linter.update_msg, fg='red')
    click.secho(f"Validator: stac-validator {linter.validator_version}", bg="blue", fg="white")
    if linter.valid_stac == True:
        click.secho(f"Valid {linter.asset_type}: {linter.valid_stac}", fg='green')
    else:
        click.secho(f"Valid {linter.asset_type}: {linter.valid_stac}", fg='red')

    if len(linter.schema) > 0:
        click.secho("Schemas validated: ", fg="blue")
        for schema in linter.schema:
            click.secho(f"    {schema}")

    if linter.invalid_asset_format is not None:
        link_asset_message(linter.invalid_asset_format, "asset", "format")

    if linter.invalid_asset_request is not None:
        link_asset_message(linter.invalid_asset_request, "asset", "request")

    if linter.invalid_link_format is not None:
        link_asset_message(linter.invalid_link_format, "link", "format")

    if linter.invalid_link_request is not None:
        link_asset_message(linter.invalid_link_request, "link", "request")

    if linter.error_type != "":
        click.secho(f"Validation error type: ", fg="red")
        click.secho(f"    {linter.error_type}")

    if linter.error_msg != "":
        click.secho(f"Validation error message: ", fg='red')
        click.secho(f"    {linter.error_msg}")

    click.secho()

    if linter.asset_type == "COLLECTION" and linter.summaries == False:
        click.secho(f"WARNING: STAC Best Practices asks for a summaries field in a STAC collection", fg="red")
        click.secho(f"    https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md")
        click.secho()

    if linter.num_links >= 20:
        click.secho(f"WARNING: You have {linter.num_links} links. Please consider using sub-collections", fg="red")
        click.secho(f"    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#catalog--collection-practices")
    else:
        click.secho(f"This object has {linter.num_links} links", fg="green")

    click.secho()
    ### Stac validator response for reference
    # click.secho(json.dumps(linter.message, indent=4))

@click.option(
    "-a", "--assets", is_flag=True, help="Validate assets for format and response."
)
@click.option(
    "-l", "--links", is_flag=True, help="Validate links for format and response."
)
@click.command()
@click.argument('file')
def main(file, assets, links):
    linter = Linter(file, assets, links)
    cli_message(linter)
