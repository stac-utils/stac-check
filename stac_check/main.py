import click

def parse_file(file):
    f = open(file, "r")
    print(f.read())

@click.command()
@click.argument('file')
def main(file):
    parse_file(file)