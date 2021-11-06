from stac_check.lint.lint import Linter

def test_linter_bad_links():
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file)
    link_format_errors = ["http:/remotdata.io/catalog/20201211_223832_CS2/index.html"]
    link_request_errors = [
        "http://catalog/collection.json", 
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html"
    ]
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert len(linter.invalid_link_format) > 0
    assert linter.invalid_link_format == link_format_errors
    assert linter.invalid_link_request == link_request_errors