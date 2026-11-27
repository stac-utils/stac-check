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
        msg = linter.message
        assert msg["version"] == "1.0.0"
        assert msg["path"] == url
        assert msg["valid_stac"] is True
        assert msg["validation_method"] == "stac-valid FastValidator"
        assert linter.asset_type == "ITEM"
        assert linter.schema == [
            "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
        ]

        linter = Linter(url, assets=False, headers=no_headers)
        msg = linter.message
        assert msg["valid_stac"] is False
        assert msg["error_type"] == "FastValidationError"


def test_verbose_error_message():
    """Invalid items report the FastValidator error and structured
    per-error details in the message's errors list."""
    file = "sample_files/1.0.0/bad-item.json"
    linter = Linter(file, verbose=True)

    assert linter.valid_stac is False
    assert "id" in linter.error_msg.lower()
    assert "must contain" in linter.error_msg.lower()

    errors = linter.message.get("errors", [])
    assert errors
    assert errors[0]["error_message"]
    assert "affected_items" in errors[0]


def test_linter_fast_validates_valid_dict():
    """Fast mode should actually validate dicts, not skip validation."""
    file = "sample_files/1.0.0/core-item.json"
    with open(file) as f:
        data = json.load(f)
    linter = Linter(data, fast=True)
    assert linter.valid_stac == True
    assert linter.message["validation_method"] == "stac-valid FastValidator"


def test_linter_fast_validates_invalid_dict():
    """Fast mode should report invalid dicts as invalid."""
    file = "sample_files/1.0.0/bad-item.json"
    with open(file) as f:
        data = json.load(f)
    linter = Linter(data, fast=True)
    assert linter.valid_stac == False
    assert linter.error_type == "FastValidationError"


def test_linter_fast_prevalidated_dict_skips_validation():
    """prevalidated dicts skip validation in fast mode."""
    file = "sample_files/1.0.0/bad-item.json"
    with open(file) as f:
        data = json.load(f)
    linter = Linter(data, fast=True, prevalidated=True)
    assert linter.valid_stac == True


def test_linter_fast_skips_geometry_errors():
    """--fast skips geometry validation."""
    file = "sample_files/1.0.0/invalid-antimeridian-bbox.json"
    linter = Linter(file, fast=True)
    assert linter.geometry_errors_msg == []


def test_linter_geometry_errors_by_default():
    """Geometry validation errors surface by default (without --fast)."""
    file = "sample_files/1.0.0/invalid-antimeridian-bbox.json"
    linter = Linter(file)
    assert linter.geometry_errors_msg[0] == "Geometry Validation [BETA]: "
    assert any("antimeridian" in msg for msg in linter.geometry_errors_msg)


def test_linter_pre_1_0_rejected():
    """Pre-1.0 STAC documents fail with a clear unsupported-version error
    instead of a cryptic schema fetch failure."""
    file = "sample_files/0.9.0/landsat8-sample.json"
    linter = Linter(file)
    assert linter.valid_stac is False
    assert linter.error_type == "UnsupportedVersionError"
    assert "0.9.0" in linter.error_msg
    assert "1.0.0 and later" in linter.error_msg


def test_linter_pre_1_0_rejected_recursive():
    """Recursive fast validation reports pre-1.0 objects with the same
    clear error and does not descend into their children."""
    file = "sample_files/0.9.0/landsat8-sample.json"
    linter = Linter(file, recursive=True, fast=True)
    assert len(linter.validate_all) == 1
    result = linter.validate_all[0]
    assert result["valid_stac"] is False
    assert result["error_type"] == "UnsupportedVersionError"
    assert "1.0.0 and later" in result["error_message"]


def test_linter_pre_1_0_rejected_dict():
    """Dict input gets the same rejection."""
    with open("sample_files/0.9.0/landsat8-sample.json") as f:
        data = json.load(f)
    linter = Linter(data)
    assert linter.valid_stac is False
    assert linter.error_type == "UnsupportedVersionError"


def test_is_pre_1_0_two_part_version():
    """A two-part "1.0" version is not pre-1.0; padding must not sort
    it below "1.0.0"."""
    from stac_check.lint import _is_pre_1_0

    assert _is_pre_1_0({"stac_version": "1.0"}) is False
    assert _is_pre_1_0({"stac_version": "0.9"}) is True
    assert _is_pre_1_0({"stac_version": "1.0.0"}) is False


def test_linter_unrecognized_json_reports_error():
    """A JSON document that FastValidator cannot recognize reports its
    own error line rather than a blank error_message."""
    linter = Linter({"foo": "bar"})
    assert linter.valid_stac is False
    assert linter.error_type == "FastValidationError"
    assert "type" in linter.error_msg.lower() or "Unknown" in linter.error_msg


def test_linter_draft07_extension_schema():
    """Draft-07 extension schemas validate under their declared dialect.

    Regression test for https://github.com/stac-utils/stac-check/issues/159:
    the Portolan extension declares draft-07 and uses the tuple form of
    'items', which crashed the old jsonschema engine's hardcoded 2020-12
    resolver. FastValidator compiles it with fastjsonschema instead.
    """
    item = {
        "type": "Feature",
        "stac_version": "1.0.0",
        "id": "portolan-item",
        "geometry": {"type": "Point", "coordinates": [0, 0]},
        "bbox": [-180, -90, 180, 90],
        "properties": {"datetime": "2020-01-01T00:00:00Z"},
        "links": [],
        "assets": {},
        "stac_extensions": [
            "https://schemas.portolan-sdi.org/portolan/v0.1.1/schema.json"
        ],
    }
    linter = Linter(item)
    assert linter.valid_stac is True
    assert linter.error_type == ""
