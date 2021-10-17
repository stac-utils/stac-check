import click
import json
from .lint.lint import Linter

def cli_message(file):
    linter = Linter(file)
    info = linter.parse_file()
    if info["stac_validator"]["version"] == "1.0.0":
        click.echo(click.style(info["update"], fg='green'))
    else:
        click.echo(click.style(info["update"], fg='red'))
    click.echo(info["stac_validator"])

@click.command()
@click.argument('file')
def main(file):
    cli_message(file)
