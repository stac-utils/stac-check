from re import L
from stac_check.lint import Linter
import pytest

@pytest.mark.skip(reason="test is ineffective - bad links are redirecting to a third party site")
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
        "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
        "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH"
    ]
    link_format_errors = [
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html",
    ]
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
    linter = Linter(file, assets=False, links=False, recursive=True)
    assert linter.version == "1.0.0"
    assert linter.recursive == True
    assert linter.validate_all[0] == {
        "version": "1.0.0",
        "path": "sample_files/1.0.0/catalog-with-bad-item.json",
        "schema": [
            "https://schemas.stacspec.org/v1.0.0/catalog-spec/json-schema/catalog.json"
        ],
        "valid_stac": True,
        "asset_type": "CATALOG",
        "validation_method": "recursive"
    }

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
            "https://stac-extensions.github.io/view/v1.0.0/schema.json"
        ],
        "stac_version": "1.0.0",
        "description": "A simple collection demonstrating core catalog fields with links to a couple of items",
        "title": "Simple Example Collection",
        "providers": [
            {
            "name": "Remote Data, Inc",
            "description": "Producers of awesome spatiotemporal assets",
            "roles": [
                "producer",
                "processor"
            ],
            "url": "http://remotedata.io"
            }
        ],
        "extent": {
            "spatial": {
            "bbox": [
                [
                172.91173669923782,
                1.3438851951615003,
                172.95469614953714,
                1.3690476620161975
                ]
            ]
            },
            "temporal": {
            "interval": [
                [
                "2020-12-11T22:38:32.125Z",
                "2020-12-14T18:02:31.437Z"
                ]
            ]
            }
        },
        "license": "CC-BY-4.0",
        "summaries": {
            "platform": [
            "cool_sat1",
            "cool_sat2"
            ],
            "constellation": [
            "ion"
            ],
            "instruments": [
            "cool_sensor_v1",
            "cool_sensor_v2"
            ],
            "gsd": {
            "minimum": 0.512,
            "maximum": 0.66
            },
            "eo:cloud_cover": {
            "minimum": 1.2,
            "maximum": 1.2
            },
            "proj:epsg": {
            "minimum": 32659,
            "maximum": 32659
            },
            "view:sun_elevation": {
            "minimum": 54.9,
            "maximum": 54.9
            },
            "view:off_nadir": {
            "minimum": 3.8,
            "maximum": 3.8
            },
            "view:sun_azimuth": {
            "minimum": 135.7,
            "maximum": 135.7
            }
        },
        "links": [
            {
            "rel": "root",
            "href": "./collection.json",
            "type": "application/json",
            "title": "Simple Example Collection"
            },
            {
            "rel": "item",
            "href": "./simple-item.json",
            "type": "application/geo+json",
            "title": "Simple Item"
            },
            {
            "rel": "item",
            "href": "./core-item.json",
            "type": "application/geo+json"
            },
            {
            "rel": "item",
            "href": "./extended-item.json",
            "type": "application/geo+json",
            "title": "Extended Item"
            }
        ]
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
            1.3690476620161975
        ],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
            [
                [
                172.91173669923782,
                1.3438851951615003
                ],
                [
                172.95469614953714,
                1.3438851951615003
                ],
                [
                172.95469614953714,
                1.3690476620161975
                ],
                [
                172.91173669923782,
                1.3690476620161975
                ],
                [
                172.91173669923782,
                1.3438851951615003
                ]
            ]
            ]
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
            "instruments": [
            "cool_sensor_v1"
            ],
            "constellation": "ion",
            "mission": "collection 5624",
            "gsd": 0.512
        },
        "collection": "simple-collection",
        "links": [
            {
            "rel": "collection",
            "href": "./collection.json",
            "type": "application/json",
            "title": "Simple Example Collection"
            },
            {
            "rel": "root",
            "href": "./collection.json",
            "type": "application/json",
            "title": "Simple Example Collection"
            },
            {
            "rel": "parent",
            "href": "./collection.json",
            "type": "application/json",
            "title": "Simple Example Collection"
            },
            {
            "rel": "alternate",
            "type": "text/html",
            "href": "http://remotedata.io/catalog/20201211_223832_CS2/index.html",
            "title": "HTML version of this STAC Item"
            }
        ],
        "assets": {
            "analytic": {
            "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic.tif",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "4-Band Analytic",
            "roles": [
                "data"
            ]
            },
            "thumbnail": {
            "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
            "title": "Thumbnail",
            "type": "image/png",
            "roles": [
                "thumbnail"
            ]
            },
            "visual": {
            "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.tif",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "3-Band Visual",
            "roles": [
                "visual"
            ]
            },
            "udm": {
            "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic_udm.tif",
            "title": "Unusable Data Mask",
            "type": "image/tiff; application=geotiff;"
            },
            "json-metadata": {
            "href": "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
            "title": "Extended Metadata",
            "type": "application/json",
            "roles": [
                "metadata"
            ]
            },
            "ephemeris": {
            "href": "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
            "title": "Satellite Ephemeris Metadata"
            }
        }
    }
    linter = Linter(file)
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert linter.check_datetime_null() == True
    assert linter.create_best_practices_dict()["datetime_null"] == ['Please avoid setting the datetime field to null, many clients search on this field']
