from stac_check.lint import Linter


def test_lint_assets_no_links():
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file, assets=True, assets_open_urls=False)
    assert linter.message == {
        "version": "1.0.0",
        "path": file,
        "schema": [
            "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
        ],
        "valid_stac": True,
        "asset_type": "ITEM",
        "validation_method": "default",
        "assets_validated": {
            "format_valid": [
                "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic.tif",
                "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
                "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.tif",
                "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic_udm.tif",
                "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
                "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
            ],
            "format_invalid": [],
            "request_valid": [],
            "request_invalid": [],
        },
    }


def test_linter_bad_assets():
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file, assets=True)
    asset_format_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg"
    ]
    asset_request_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
        "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
        "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
    ]
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert linter.invalid_asset_format == asset_format_errors
    assert linter.invalid_asset_request == asset_request_errors


def test_linter_bad_links():
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file, links=True)
    link_format_errors = ["http:/remotdata.io/catalog/20201211_223832_CS2/index.html"]
    link_request_errors = [
        "http://catalog/collection.json",
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html",
    ]
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert len(linter.invalid_link_format) > 0
    assert linter.invalid_link_format == link_format_errors
    assert linter.invalid_link_request == link_request_errors


def test_linter_bad_links_assets():
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file, assets=True, links=True)
    asset_format_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg"
    ]
    asset_request_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
        "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
        "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
    ]
    link_format_errors = [
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html",
    ]
    link_request_errors = [
        "http://catalog/collection.json",
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html",
    ]
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert len(linter.invalid_link_format) > 0
    assert linter.invalid_asset_format == asset_format_errors
    assert linter.invalid_asset_request == asset_request_errors
    assert linter.invalid_link_format == link_format_errors
    assert linter.invalid_link_request == link_request_errors
