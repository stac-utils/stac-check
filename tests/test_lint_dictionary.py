from stac_check.lint import Linter


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
