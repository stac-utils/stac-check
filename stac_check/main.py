import click

@click.command()
@click.argument('name')
def main(name):
    print(f"hello {name}")