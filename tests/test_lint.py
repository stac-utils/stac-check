from re import L
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
    assert linter.check_summaries() == True

def test_linter_collection_no_summaries():
    file = "sample_files/1.0.0/collection-no-summaries.json"
    linter = Linter(file, assets=False, links=False)
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "COLLECTION"
    assert linter.check_summaries() == False
    assert linter.best_practices_msg == [
        "STAC Best Practices: ",
        "    Object should be called 'collection.json' not 'collection-no-summaries.json'",
        "",
        "    A STAC collection should contain a summaries field",
        "    It is recommended to store information like eo:bands in summaries",
        ""
    ]

def test_linter_catalog():
    file = "sample_files/1.0.0/catalog.json"
    linter = Linter(file, assets=False, links=False)
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "CATALOG"
    assert linter.check_bloated_links() == False

def test_linter_collection_recursive():
    file = "sample_files/1.0.0/catalog-with-bad-item.json"
    linter = Linter(file, assets=False, links=False, recursive=1000)
    assert linter.version == "1.0.0"
    assert linter.recursive == 1000
    assert linter.validate_all == [
        {
            "version": "1.0.0",
            "path": "sample_files/1.0.0/catalog-with-bad-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0/catalog-spec/json-schema/catalog.json"
            ],
            "valid_stac": True,
            "asset_type": "CATALOG",
            "validation_method": "recursive"
        },
        {
            "version": "1.0.0",
            "path": "sample_files/1.0.0/./bad-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0/catalog-spec/json-schema/catalog.json"
            ],
            "valid_stac": False,
            "error_type": "FileNotFoundError",
            "error_message": "[Errno 2] No such file or directory: 'sample_files/1.0.0/./bad-item.json'"
        }
    ]

def test_linter_item_id_not_matching_file_name():
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file)
    assert linter.file_name == "core-item"
    assert linter.object_id == "20201211_223832_CS2"
    assert linter.file_name != linter.object_id
    assert linter.check_item_id_file_name() == False

def test_linter_collection_catalog_id():
    file = "sample_files/1.0.0/collection-no-title.json"
    linter = Linter(file)
    assert linter.check_catalog_id_file_name() == False

def test_linter_item_id_format_best_practices():
    file = "sample_files/1.0.0/core-item-invalid-id.json"
    linter = Linter(file)
    assert linter.check_searchable_identifiers() == False
    assert linter.check_percent_encoded() == True

def test_datetime_set_to_null():
    file = "sample_files/1.0.0/core-item-null-datetime.json"
    linter = Linter(file)
    assert linter.check_datetime_null()== True

def test_unlocated_item():
    file = "sample_files/1.0.0/core-item-unlocated.json"
    linter = Linter(file)
    assert linter.check_unlocated() == True
    assert linter.check_geometry_null() == True

def test_bloated_item():
    file = "sample_files/1.0.0/core-item-bloated.json"
    linter = Linter(file)

    assert linter.check_bloated_metadata() == True
    assert len(linter.data["properties"]) > 20

    assert linter.check_bloated_links() == True
    assert len(linter.data["links"]) > 20

def test_small_thumbnail():
    file = "sample_files/1.0.0/core-item-large-thumbnail.json"
    linter = Linter(file)

    assert linter.check_thumbnail() != True

    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file)

    assert linter.check_thumbnail() == True

def test_title_field():
    file = "sample_files/1.0.0/collection-no-title.json"
    linter = Linter(file)

    assert linter.check_links_title_field() == False

def test_self_in_links():
    file = "sample_files/1.0.0/collection-no-title.json"
    linter = Linter(file)

    assert linter.check_links_self() == False