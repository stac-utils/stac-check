import click
import json
from .lint.lint import Linter

def load_linter(file):
    linter = Linter(file)
    linter.parse_file()
    return linter

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

    if len(linter.link_format) > 0:
        click.secho("Link format error(s): ", fg="red")
        for link in linter.link_format:
            click.secho(f"    {link}")

    if linter.error_type != "":
        click.secho(f"Validation error type: {linter.error_type}", fg="red")

    if linter.error_msg != "":
        click.secho(f"Validation error message: {linter.error_msg}")

    click.secho()

    ### Stac validator response for reference
    click.secho(json.dumps(linter.message, indent=4))


@click.command()
@click.argument('file')
def main(file):
    linter = load_linter(file)
    cli_message(linter)
