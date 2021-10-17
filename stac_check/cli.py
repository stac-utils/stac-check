import click
import json
from .lint.lint import Linter

def load_linter(file):
    linter = Linter(file)
    linter.parse_file()
    return linter

def cli_message(linter):
    click.secho("----------<stac-check>----------", blink=True, bold=True)
    if linter.version == "1.0.0":
        click.secho(linter.update_msg, fg='green')
    else:
        click.secho(linter.update_msg, fg='red')
    click.secho(f"Validator: stac-validator {linter.validator_version} ", bg="blue", fg="white")
    click.secho(f"https://github.com/sparkgeo/stac-validator")
    if linter.valid_stac == True:
        click.secho(f"Valid {linter.asset_type}: {linter.valid_stac}", fg='green')
    else:
        click.secho(f"Valid {linter.asset_type}: {linter.valid_stac}", fg='red')
    click.secho(f"Schemas validated: {json.dumps(linter.schema, indent=4)}", fg="blue")

    ### Stac validator response for reference
    # click.secho(json.dumps(linter.message, indent=4))

@click.command()
@click.argument('file')
def main(file):
    linter = load_linter(file)
    cli_message(linter)
