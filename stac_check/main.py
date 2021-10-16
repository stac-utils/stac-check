import click
import json
import jsonschema
from jsonschema import validate

def parse_file(file):
    f = open(file, "r")
    valid = validate_file(f)
    print(valid)

def validate_file(file):
    try:
        json.load(file)
    except ValueError as err:
        return False
    return True

@click.command()
@click.argument('file')
def main(file):
    parse_file(file)