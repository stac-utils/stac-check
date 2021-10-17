import click
import json
from .lint.lint import Linter

def load_linter(file):
    linter = Linter(file)
    return linter

def cli_message(linter):
    if linter.version == "1.0.0":
        click.secho(linter.update_msg, fg='green')
    else:
        click.secho(linter.update_msg, fg='red')
    click.secho("Validator: stac-validator 2.3.0 ", fg="blue")
    if linter.valid_stac == True:
        click.secho(f"Valid {linter.asset_type}: {linter.valid_stac}", fg='green')
    else:
        click.secho(f"Valid {linter.asset_type}: {linter.valid_stac}", fg='red')
    click.secho(f"Schemas validated: {json.dumps(linter.schema, indent=4)}", fg="blue")

    ### Stac validator response for reference
    # info = linter.parse_file()
    # click.secho(json.dumps(info, indent=4))

@click.command()
@click.argument('file')
def main(file):
    linter = load_linter(file)
    cli_message(linter)
