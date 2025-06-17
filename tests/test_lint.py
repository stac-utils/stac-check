import json

import requests_mock

from stac_check.lint import Linter


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
        "Object should be called 'collection.json' not 'collection-no-summaries.json'",
        "",
        "A STAC collection should contain a summaries field",
        "It is recommended to store information like eo:bands in summaries",
        "",
    ]


def test_linter_catalog():
    file = "sample_files/1.0.0/catalog.json"
    linter = Linter(file, assets=False, links=False)
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "CATALOG"
    assert linter.check_bloated_links() == False


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
    assert linter.check_catalog_file_name() == False


def test_linter_item_id_format_best_practices():
    file = "sample_files/1.0.0/core-item-invalid-id.json"
    linter = Linter(file)
    assert linter.check_searchable_identifiers() == False
    assert linter.check_percent_encoded() == True


def test_datetime_set_to_null():
    file = "sample_files/1.0.0/core-item-null-datetime.json"
    linter = Linter(file)
    assert linter.check_datetime_null() == True


def test_unlocated_item():
    file = "sample_files/1.0.0/core-item-unlocated.json"
    linter = Linter(file)
    assert linter.check_unlocated() == True
    assert linter.check_geometry_null() == True

    file = "sample_files/1.0.0/core-item-unlocated-null-bbox.json"
    linter = Linter(file)
    assert linter.check_unlocated() == False
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


def test_catalog_name():
    file = "sample_files/1.0.0/catalog.json"
    linter = Linter(file)
    assert linter.check_catalog_file_name()
    file = "sample_files/1.0.0/collection.json"
    linter = Linter(file)
    assert linter.check_catalog_file_name()


def test_lint_header():
    file = "sample_files/1.0.0/core-item.json"
    url = "https://localhost/" + file

    no_headers = {}
    valid_headers = {"x-api-key": "a-valid-api-key"}

    with requests_mock.Mocker(real_http=True) as mock, open(file) as json_data:
        mock.get(url, request_headers=no_headers, status_code=403, json={})
        mock.get(url, request_headers=valid_headers, json=json.load(json_data))

        linter = Linter(url, assets=False, headers=valid_headers)
        assert linter.message == {
            "version": "1.0.0",
            "path": "https://localhost/sample_files/1.0.0/core-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        }

        linter = Linter(url, assets=False, headers=no_headers)
        msg = linter.message
        assert msg["valid_stac"] is False
        assert msg["error_type"] == "HTTPError"
        # Accept either 'message' or 'error_message' as the error string
        error_msg = msg.get("error_message") or msg.get("message")
        assert (
            error_msg
            == "403 Client Error: None for url: https://localhost/sample_files/1.0.0/core-item.json"
        )
        # Optionally check path, version, schema if present
        if "path" in msg:
            assert msg["path"] == "https://localhost/sample_files/1.0.0/core-item.json"


def test_verbose_error_message():
    """Test that verbose error messages are properly formatted and included."""
    # Test with a known bad item that will generate validation errors
    file = "sample_files/1.0.0/bad-item.json"
    linter = Linter(file, verbose=True)

    # Verify the item is invalid
    assert linter.valid_stac is False

    # Check that we have the expected error message
    assert "id" in linter.error_msg.lower()
    assert "required" in linter.error_msg.lower()

    # Check that verbose error message contains expected structure
    assert isinstance(linter.verbose_error_msg, dict)
    assert "validator" in linter.verbose_error_msg
    assert "path_in_schema" in linter.verbose_error_msg

    # Check specific parts of the verbose error message
    assert linter.verbose_error_msg.get("validator") == "required"

    # Check path_in_schema - it might contain both strings and integers
    path_in_schema = linter.verbose_error_msg.get("path_in_schema", [])
    assert any(isinstance(p, (str, int)) for p in path_in_schema)

    # Check that the error message is included in the string representation
    verbose_str = str(linter.verbose_error_msg)
    assert "required" in verbose_str
    assert "id" in verbose_str
