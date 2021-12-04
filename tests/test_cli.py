from click.testing import CliRunner
from stac_check.cli import main
import pytest

INTRO = "stac-check: STAC spec validaton and linting tool"
VALID_ITEM = "Valid ITEM: True"
VERSION_MSG_1 = "Thanks for using STAC version 1.0.0!"
VALIDATOR = "Validator: stac-validator 2.4.0"
SCHEMA_MSG = "Schemas validated: "

@pytest.mark.skip(reason="cli output is changing constantly right now")
def test_core_item_100():
    runner = CliRunner()
    result = runner.invoke(main, ["sample_files/1.0.0/core-item.json"])
    assert result.exit_code == 0
    assert result.output.splitlines()[1] == INTRO
    assert result.output.splitlines()[2] == VERSION_MSG_1
    assert result.output.splitlines()[3] == VALIDATOR
    assert result.output.splitlines()[4] == VALID_ITEM
    assert result.output.splitlines()[5] == SCHEMA_MSG
    assert result.output.splitlines()[6] == """    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"""
