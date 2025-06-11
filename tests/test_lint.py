import json

import pytest
import requests_mock

from stac_check.lint import Linter


@pytest.mark.skip(
    reason="test is ineffective - bad links are redirecting to a third party site"
)
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
        "",
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
    linter = Linter(file, assets=False, links=False, recursive=True)
    assert linter.version == "1.0.0"
    assert linter.recursive == True
    msg = linter.validate_all[0]
    assert msg["valid_stac"] is False
    assert msg["error_type"] == "JSONSchemaValidationError"
    # Accept either 'message' or 'error_message' as the error string
    error_msg = msg.get("error_message") or msg.get("message", "")
    assert "'id' is a required property" in error_msg
    # Optionally check path, version, schema if present
    if "path" in msg:
        assert msg["path"].endswith("bad-item.json")


def test_linter_recursive_max_depth_1():
    file = "https://radarstac.s3.amazonaws.com/stac/catalog.json"
    stac = Linter(file, assets=False, links=False, recursive=True, max_depth=1)
    assert stac.validate_all == [
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "valid_stac": True,
        }
    ]


def test_linter_recursive_max_depth_4():
    file = "https://radarstac.s3.amazonaws.com/stac/catalog.json"
    stac = Linter(file, assets=False, links=False, recursive=True, max_depth=4)
    assert stac.validate_all == [
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/collection.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/collection.json"],
            "asset_type": "COLLECTION",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-05-13/RS1_M0630938_F2N_20120513_225708_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-06-14/RS1_M0634796_F3F_20120614_110317_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-06-14/RS1_M0634795_F3F_20120614_110311_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-10-12/RS1_M0634798_F3F_20121012_110325_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-10-12/RS1_M0634799_F3F_20121012_110331_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/raw/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/raw/2012-05-13/RS1_M0000676_F2N_20120513_225701_HH_RAW.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
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


def test_bbox_matches_geometry():
    # Test with matching bbox and geometry
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file)
    assert linter.check_bbox_matches_geometry() is True

    # Test with mismatched bbox and geometry
    mismatched_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-item",
        "bbox": [100.0, 0.0, 105.0, 1.0],  # Deliberately wrong bbox
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [172.91173669923782, 1.3438851951615003],
                    [172.95469614953714, 1.3438851951615003],
                    [172.95469614953714, 1.3690476620161975],
                    [172.91173669923782, 1.3690476620161975],
                    [172.91173669923782, 1.3438851951615003],
                ]
            ],
        },
        "properties": {"datetime": "2020-12-11T22:38:32.125Z"},
    }
    linter = Linter(mismatched_item)
    result = linter.check_bbox_matches_geometry()

    # Check that the result is a tuple and the first element is False
    assert isinstance(result, tuple)
    assert result[0] is False

    # Check that the tuple contains the expected elements (calculated bbox, actual bbox, differences)
    assert len(result) == 4
    calc_bbox, actual_bbox, differences = result[1], result[2], result[3]

    # Verify the calculated bbox matches the geometry coordinates
    assert calc_bbox == [
        172.91173669923782,
        1.3438851951615003,
        172.95469614953714,
        1.3690476620161975,
    ]

    # Verify the actual bbox is what we provided
    assert actual_bbox == [100.0, 0.0, 105.0, 1.0]

    # Verify the differences are calculated correctly
    expected_differences = [abs(actual_bbox[i] - calc_bbox[i]) for i in range(4)]
    assert differences == expected_differences

    # Test with null geometry (should return True as check is not applicable)
    null_geom_item = {
        "stac_version": "1.0.0",
        "type": "Feature",
        "id": "test-item-null-geom",
        "bbox": [100.0, 0.0, 105.0, 1.0],
        "geometry": None,
        "properties": {"datetime": "2020-12-11T22:38:32.125Z"},
    }
    linter = Linter(null_geom_item)
    assert linter.check_bbox_matches_geometry() is True

    # Test with missing bbox (should return True as check is not applicable)
    no_bbox_item = {
        "stac_version": "1.0.0",
        "type": "Feature",
        "id": "test-item-no-bbox",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [172.91173669923782, 1.3438851951615003],
                    [172.95469614953714, 1.3438851951615003],
                    [172.95469614953714, 1.3690476620161975],
                    [172.91173669923782, 1.3690476620161975],
                    [172.91173669923782, 1.3438851951615003],
                ]
            ],
        },
        "properties": {"datetime": "2020-12-11T22:38:32.125Z"},
    }
    linter = Linter(no_bbox_item)
    assert linter.check_bbox_matches_geometry() is True


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


def test_lint_dict_collection():
    file = {
        "id": "simple-collection",
        "type": "Collection",
        "stac_extensions": [
            "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.0.0/schema.json",
        ],
        "stac_version": "1.0.0",
        "description": "A simple collection demonstrating core catalog fields with links to a couple of items",
        "title": "Simple Example Collection",
        "providers": [
            {
                "name": "Remote Data, Inc",
                "description": "Producers of awesome spatiotemporal assets",
                "roles": ["producer", "processor"],
                "url": "http://remotedata.io",
            }
        ],
        "extent": {
            "spatial": {
                "bbox": [
                    [
                        172.91173669923782,
                        1.3438851951615003,
                        172.95469614953714,
                        1.3690476620161975,
                    ]
                ]
            },
            "temporal": {
                "interval": [["2020-12-11T22:38:32.125Z", "2020-12-14T18:02:31.437Z"]]
            },
        },
        "license": "CC-BY-4.0",
        "summaries": {
            "platform": ["cool_sat1", "cool_sat2"],
            "constellation": ["ion"],
            "instruments": ["cool_sensor_v1", "cool_sensor_v2"],
            "gsd": {"minimum": 0.512, "maximum": 0.66},
            "eo:cloud_cover": {"minimum": 1.2, "maximum": 1.2},
            "proj:epsg": {"minimum": 32659, "maximum": 32659},
            "view:sun_elevation": {"minimum": 54.9, "maximum": 54.9},
            "view:off_nadir": {"minimum": 3.8, "maximum": 3.8},
            "view:sun_azimuth": {"minimum": 135.7, "maximum": 135.7},
        },
        "links": [
            {
                "rel": "root",
                "href": "./collection.json",
                "type": "application/json",
                "title": "Simple Example Collection",
            },
            {
                "rel": "item",
                "href": "./simple-item.json",
                "type": "application/geo+json",
                "title": "Simple Item",
            },
            {"rel": "item", "href": "./core-item.json", "type": "application/geo+json"},
            {
                "rel": "item",
                "href": "./extended-item.json",
                "type": "application/geo+json",
                "title": "Extended Item",
            },
        ],
    }
    linter = Linter(file)
    assert linter.valid_stac == True
    assert linter.asset_type == "COLLECTION"
    assert linter.check_catalog_file_name() == True


def test_lint_dict_item():
    file = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "20201211_223832_CS2",
        "bbox": [
            172.91173669923782,
            1.3438851951615003,
            172.95469614953714,
            1.3690476620161975,
        ],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [172.91173669923782, 1.3438851951615003],
                    [172.95469614953714, 1.3438851951615003],
                    [172.95469614953714, 1.3690476620161975],
                    [172.91173669923782, 1.3690476620161975],
                    [172.91173669923782, 1.3438851951615003],
                ]
            ],
        },
        "properties": {
            "title": "Core Item",
            "description": "A sample STAC Item that includes examples of all common metadata",
            "datetime": None,
            "start_datetime": "2020-12-11T22:38:32.125Z",
            "end_datetime": "2020-12-11T22:38:32.327Z",
            "created": "2020-12-12T01:48:13.725Z",
            "updated": "2020-12-12T01:48:13.725Z",
            "platform": "cool_sat1",
            "instruments": ["cool_sensor_v1"],
            "constellation": "ion",
            "mission": "collection 5624",
            "gsd": 0.512,
        },
        "collection": "simple-collection",
        "links": [
            {
                "rel": "collection",
                "href": "./collection.json",
                "type": "application/json",
                "title": "Simple Example Collection",
            },
            {
                "rel": "root",
                "href": "./collection.json",
                "type": "application/json",
                "title": "Simple Example Collection",
            },
            {
                "rel": "parent",
                "href": "./collection.json",
                "type": "application/json",
                "title": "Simple Example Collection",
            },
            {
                "rel": "alternate",
                "type": "text/html",
                "href": "http://remotedata.io/catalog/20201211_223832_CS2/index.html",
                "title": "HTML version of this STAC Item",
            },
        ],
        "assets": {
            "analytic": {
                "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic.tif",
                "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                "title": "4-Band Analytic",
                "roles": ["data"],
            },
            "thumbnail": {
                "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
                "title": "Thumbnail",
                "type": "image/png",
                "roles": ["thumbnail"],
            },
            "visual": {
                "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.tif",
                "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                "title": "3-Band Visual",
                "roles": ["visual"],
            },
            "udm": {
                "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic_udm.tif",
                "title": "Unusable Data Mask",
                "type": "image/tiff; application=geotiff;",
            },
            "json-metadata": {
                "href": "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
                "title": "Extended Metadata",
                "type": "application/json",
                "roles": ["metadata"],
            },
            "ephemeris": {
                "href": "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
                "title": "Satellite Ephemeris Metadata",
            },
        },
    }
    linter = Linter(file)
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert linter.check_datetime_null() == True
    assert linter.create_best_practices_dict()["datetime_null"] == [
        "Please avoid setting the datetime field to null, many clients search on this field"
    ]


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


def test_geometry_coordinates_order():
    """Test the check_geometry_coordinates_order method for detecting potentially incorrectly ordered coordinates."""
    # Create a test item with coordinates in the correct order (longitude, latitude)
    correct_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-coordinates-correct",
        "bbox": [10.0, -10.0, 20.0, 10.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [10.0, -10.0],  # lon, lat
                    [20.0, -10.0],
                    [20.0, 10.0],
                    [10.0, 10.0],
                    [10.0, -10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Create a test item with coordinates in the wrong order (latitude, longitude)
    # but with values that don't trigger the validation checks
    undetectable_reversed_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-coordinates-undetectable-reversed",
        "bbox": [10.0, -10.0, 20.0, 10.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-10.0, 10.0],  # lat, lon (reversed) but within valid ranges
                    [-10.0, 20.0],
                    [10.0, 20.0],
                    [10.0, 10.0],
                    [-10.0, 10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Create a test item with coordinates that are clearly reversed (latitude > 90)
    clearly_incorrect_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-coordinates-clearly-incorrect",
        "bbox": [10.0, -10.0, 20.0, 10.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [10.0, 100.0],  # Second value (latitude) > 90
                    [20.0, 100.0],
                    [20.0, 100.0],
                    [10.0, 100.0],
                    [10.0, 100.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Create a test item with coordinates that may be reversed based on heuristic
    # (first value > 90, second value < 90, first value > second value*2)
    heuristic_incorrect_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-coordinates-heuristic-incorrect",
        "bbox": [10.0, -10.0, 20.0, 10.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [120.0, 40.0],  # First value > 90, second < 90, first > second*2
                    [120.0, 40.0],
                    [120.0, 40.0],
                    [120.0, 40.0],
                    [120.0, 40.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Test with correct coordinates - this should pass both checks
    linter = Linter(correct_item)
    assert linter.check_geometry_coordinates_order() == True
    assert linter.check_geometry_coordinates_definite_errors() == True

    # Test with reversed coordinates that are within valid ranges
    # Current implementation can't detect this case, so both checks pass
    linter = Linter(undetectable_reversed_item)
    assert (
        linter.check_geometry_coordinates_order() == True
    )  # Passes because values are within valid ranges
    assert (
        linter.check_geometry_coordinates_definite_errors() == True
    )  # Passes because values are within valid ranges

    # Test with clearly incorrect coordinates (latitude > 90)
    # This should fail the definite errors check but pass the order check (which now only uses heuristic)
    linter = Linter(clearly_incorrect_item)
    assert (
        linter.check_geometry_coordinates_order() == True
    )  # Now passes because it only checks heuristic

    # Check that definite errors are detected
    result = linter.check_geometry_coordinates_definite_errors()
    assert result is not True  # Should not be True
    assert isinstance(result, tuple)  # Should be a tuple
    assert result[0] is False  # First element should be False
    assert len(result[1]) > 0  # Should have at least one invalid coordinate
    assert result[1][0][1] == 100.0  # The latitude value should be 100.0
    assert "latitude > ±90°" in result[1][0][2]  # Should indicate latitude error

    # Test with coordinates that trigger the heuristic
    # This should fail the order check but pass the definite errors check
    linter = Linter(heuristic_incorrect_item)
    assert (
        linter.check_geometry_coordinates_order() == False
    )  # Fails because of heuristic
    assert (
        linter.check_geometry_coordinates_definite_errors() == True
    )  # Passes because values are within valid ranges

    # Test that the best practices dictionary contains the appropriate error messages
    best_practices = linter.create_best_practices_dict()

    # For heuristic-based detection
    linter = Linter(heuristic_incorrect_item)
    best_practices = linter.create_best_practices_dict()
    assert "geometry_coordinates_order" in best_practices
    assert (
        "may be in the wrong order" in best_practices["geometry_coordinates_order"][0]
    )

    # For definite errors detection
    linter = Linter(clearly_incorrect_item)
    best_practices = linter.create_best_practices_dict()
    assert "geometry_coordinates_definite_errors" in best_practices
    assert (
        "contain invalid values"
        in best_practices["geometry_coordinates_definite_errors"][0]
    )


def test_bbox_antimeridian():
    """Test the check_bbox_antimeridian method for detecting incorrectly formatted bboxes that cross the antimeridian."""
    # Create a test item with an incorrectly formatted bbox that belts the globe
    # instead of properly crossing the antimeridian
    incorrect_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-antimeridian-incorrect",
        "bbox": [
            -170.0,  # west
            -10.0,  # south
            170.0,  # east (incorrect: this belts the globe instead of crossing the antimeridian)
            10.0,  # north
        ],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [170.0, -10.0],
                    [-170.0, -10.0],
                    [-170.0, 10.0],
                    [170.0, 10.0],
                    [170.0, -10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Create a test item with a correctly formatted bbox that crosses the antimeridian
    # (west > east for antimeridian crossing)
    correct_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-antimeridian-correct",
        "bbox": [
            170.0,  # west
            -10.0,  # south
            -170.0,  # east (west > east indicates antimeridian crossing)
            10.0,  # north
        ],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [170.0, -10.0],
                    [-170.0, -10.0],
                    [-170.0, 10.0],
                    [170.0, 10.0],
                    [170.0, -10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Test with the incorrect item (belting the globe)
    linter = Linter(incorrect_item)
    # The check should return False for the incorrectly formatted bbox
    assert linter.check_bbox_antimeridian() == False

    # Verify that the best practices dictionary contains the appropriate message
    best_practices = linter.create_best_practices_dict()
    assert "check_bbox_antimeridian" in best_practices
    assert len(best_practices["check_bbox_antimeridian"]) == 2

    # Check that the error messages include the west and east longitude values
    west_val = incorrect_item["bbox"][0]
    east_val = incorrect_item["bbox"][2]
    assert (
        f"(found west={west_val}, east={east_val})"
        in best_practices["check_bbox_antimeridian"][0]
    )

    # Test with the correct item - this should pass
    linter = Linter(correct_item)
    # The check should return True for the correctly formatted bbox
    assert linter.check_bbox_antimeridian() == True

    # Test with a normal bbox that doesn't cross the antimeridian
    normal_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-normal-bbox",
        "bbox": [10.0, -10.0, 20.0, 10.0],  # west  # south  # east  # north
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [10.0, -10.0],
                    [20.0, -10.0],
                    [20.0, 10.0],
                    [10.0, 10.0],
                    [10.0, -10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Test with a normal bbox - this should pass
    linter = Linter(normal_item)
    assert linter.check_bbox_antimeridian() == True


# Check if stac-pydantic is available
try:
    import importlib

    importlib.import_module("stac_pydantic")
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False

# Test decorator for pydantic tests
pytest.mark.pydantic = pytest.mark.skipif(
    not PYDANTIC_AVAILABLE,
    reason="stac-pydantic is not installed. Run 'pip install -e .[dev]' to install test dependencies.",
)


@pytest.mark.pydantic
def test_lint_pydantic_validation_valid():
    """Test pydantic validation with a valid STAC item."""
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file, pydantic=True)

    assert linter.valid_stac is True
    assert linter.asset_type == "ITEM"
    assert any("stac-pydantic" in schema for schema in linter.message["schema"])
    assert linter.message["validation_method"] == "pydantic"


@pytest.mark.pydantic
def test_lint_pydantic_validation_invalid():
    """Test pydantic validation with an invalid STAC item (missing required fields)."""
    file = "sample_files/1.0.0/bad-item.json"
    linter = Linter(file, pydantic=True)

    assert linter.valid_stac is False
    assert "PydanticValidationError" in linter.message["error_type"]
    assert "id: Field required" in linter.message["error_message"]


def test_pydantic_fallback_without_import(monkeypatch):
    """Test that pydantic validation falls back to JSONSchema when stac-pydantic is not available."""
    # Skip this test if stac-pydantic is actually installed
    if PYDANTIC_AVAILABLE:
        pytest.skip("stac-pydantic is installed, skipping fallback test")

    # Test that pydantic=False works without stac-pydantic
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file, pydantic=False)
    assert linter.valid_stac is True
    assert linter.asset_type == "ITEM"
    assert linter.message["validation_method"] == "default"

    # Test that pydantic=True falls back to JSONSchema when stac-pydantic is not available
    linter = Linter(file, pydantic=True)
    assert linter.valid_stac is True
    assert linter.asset_type == "ITEM"
    assert linter.message["validation_method"] == "default"
