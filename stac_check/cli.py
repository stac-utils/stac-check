import click
import json
from .lint.lint import Linter

def cli_message(file):
    linter = Linter(file)
    info = linter.parse_file()
    return info

@click.command()
@click.argument('file')
def main(file):
    message = cli_message(file)
    click.echo(json.dumps(message, indent=3))
