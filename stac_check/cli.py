import click
from .lint.lint import Linter

def cli_message(info):
    pass

@click.command()
@click.argument('file')
def main(file):
    linter = Linter(file)
    info = linter.parse_file()
    click.echo(info)
