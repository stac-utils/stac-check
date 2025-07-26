from stac_check.lint import Linter


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
            "validator_engine": "jsonschema",
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
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/collection.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/collection.json"],
            "asset_type": "COLLECTION",
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-05-13/RS1_M0630938_F2N_20120513_225708_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-06-14/RS1_M0634796_F3F_20120614_110317_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-06-14/RS1_M0634795_F3F_20120614_110311_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-10-12/RS1_M0634798_F3F_20121012_110325_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-10-12/RS1_M0634799_F3F_20121012_110331_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/raw/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/raw/2012-05-13/RS1_M0000676_F2N_20120513_225701_HH_RAW.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "valid_stac": True,
        },
    ]


def test_linter_recursive_100():
    file = "https://digital-atlas.s3.amazonaws.com/stac/public_stac/population/worldpop_2020/collection.json"
    stac = Linter(file, assets=False, links=False, recursive=True, max_depth=4)
    assert stac.validate_all == [
        {
            "asset_type": "COLLECTION",
            "path": "https://digital-atlas.s3.amazonaws.com/stac/public_stac/population/worldpop_2020/collection.json",
            "schema": [
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/collection-spec/json-schema/collection.json",
            ],
            "valid_stac": True,
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "version": "1.0.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://digital-atlas.s3.amazonaws.com/stac/public_stac/population/worldpop_2020/./pop_2020/pop_2020.json",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.1.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/raster/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "version": "1.0.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://digital-atlas.s3.amazonaws.com/stac/public_stac/population/worldpop_2020/./popDens_2020/popDens_2020.json",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.1.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/raster/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "version": "1.0.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://digital-atlas.s3.amazonaws.com/stac/public_stac/population/worldpop_2020/./pop_2020_parquet/pop_2020_parquet.json",
            "schema": [
                "https://stac-extensions.github.io/table/v1.2.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "recursive",
            "validator_engine": "jsonschema",
            "version": "1.0.0",
        },
    ]
