import click
import json
from .lint.lint import Linter

def cli_message(file):
    linter = Linter(file)
    info = linter.parse_file()
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
    click.secho(json.dumps(info, indent=4))

@click.command()
@click.argument('file')
def main(file):
    cli_message(file)
