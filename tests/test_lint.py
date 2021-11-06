from stac_check.lint.lint import Linter

def test_linter():
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file)
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "Item"