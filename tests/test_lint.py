from stac_check.lint import Linter
import pytest

def test_linter_bad_asset_requests():
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file, assets=True)
    asset_request_errors = [
        "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH"
    ]
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert linter.invalid_asset_format == []
    assert linter.invalid_asset_request == asset_request_errors

def test_linter_bad_assets():
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file, assets=True)
    asset_format_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg"
    ]
    asset_request_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
        "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH"
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
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html"
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
        "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH"
    ]
    link_format_errors = ["http:/remotdata.io/catalog/20201211_223832_CS2/index.html"]
    link_request_errors = [
        "http://catalog/collection.json", 
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html"
    ]
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert len(linter.invalid_link_format) > 0
    assert linter.invalid_asset_format == asset_format_errors
    assert linter.invalid_asset_request == asset_request_errors
    assert linter.invalid_link_format == link_format_errors
    assert linter.invalid_link_request == link_request_errors

def test_linter_collection():
    file = "sample_files/1.0.0/collection.json"
    linter = Linter(file, assets=False, links=False)
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "COLLECTION"
    assert linter.summaries == True

def test_linter_collection_no_summaries():
    file = "sample_files/1.0.0/collection_no_summaries.json"
    linter = Linter(file, assets=False, links=False)
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "COLLECTION"
    assert linter.summaries == False
    assert linter.best_practices_msg == [
        "STAC Best Practices: ",
        "    A STAC collection should contain a summaries field",
        "    https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md",
        ""
    ]

def test_linter_catalog():
    file = "sample_files/1.0.0/catalog.json"
    linter = Linter(file, assets=False, links=False)
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "CATALOG"
    assert linter.num_links == 6

def test_linter_collection_recursive_remote():
    file = "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json"
    linter = Linter(file, assets=False, links=False, recursive=True)
    assert linter.version == "0.9.0"
    assert linter.recursive == True
    assert linter.recursive_error_msg == "Exception Could not read uri https://landsat-stac.s3.amazonaws.com/landsat-8-l1/paths/catalog.json"

def test_linter_item_id_not_matching_file_name():
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file)
    assert linter.file_name == "core-item"
    assert linter.object_id == "20201211_223832_CS2"
    assert linter.file_name != linter.object_id

def test_linter_item_id_format_best_practices():
    file = "sample_files/1.0.0/core-item-invalid-id.json"
    linter = Linter(file)
    assert linter.searchable_identifiers == False
