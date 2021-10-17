import click
from stac_validator import stac_validator

def parse_file(file):
    valid = validate_file(file)
    print(f"Is this a valid stac? {valid}")

def validate_file(file):
    stac = stac_validator.StacValidate(file)
    stac.run()
    return stac.message[0]["valid_stac"]

@click.command()
@click.argument('file')
def main(file):
    parse_file(file)