# stac-check

<!-- markdownlint-disable MD033 MD041 -->

<p align="left">
  <img src="https://raw.githubusercontent.com/stac-utils/stac-check/main/assets/stac-check.png" width=560>
</p>

[![Downloads](https://static.pepy.tech/badge/stac-check?color=blue)](https://pepy.tech/project/stac-check)
[![GitHub contributors](https://img.shields.io/github/contributors/stac-utils/stac-check?color=blue)](https://github.com/stac-utils/stac-check/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/stac-utils/stac-check.svg?color=blue)](https://github.com/stac-utils/stac-check/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/stac-utils/stac-check.svg?color=blue)](https://github.com/stac-utils/stac-check/network/members)
[![PyPI version](https://img.shields.io/pypi/v/stac-check.svg?color=blue)](https://pypi.org/project/stac-check/)
[![STAC](https://img.shields.io/badge/STAC-1.1.0-blue.svg)](https://github.com/radiantearth/stac-spec/tree/v1.1.0)

## A linting and validation tool for STAC assets

The intent of this project is to provide a validation tool that also follows the official [STAC Best Practices document](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md)

## Latest News

- **11/26/2026:** 🚀 **stac-check 2.0!** The legacy validation engine has been removed — stac-check now validates everything with stac-valid FastValidator in a single pass, and recursive display no longer re-fetches or re-validates every asset. `--fast` now means "validation only": it skips linting and geometry checks for maximum speed, and `--fast-linting` has been removed (linting runs by default). `--max-depth` is honored in recursive mode, `--assets`/`--links` checks now work with every mode, and STAC documents older than 1.0.0 are rejected with a clear error instead of a cryptic schema failure. See the [2.0.0 changelog entry](CHANGELOG.md#v200) for the full migration notes.

- **11/26/2026:** ⚡ **Fast Recursive Validation! (v1.15.0)** `--fast` now works with `--recursive`, validating an entire catalog and all of its linked objects with stac-valid FastValidator in a single pass instead of re-fetching and re-validating every asset during display. In our benchmarks it validated a local catalog of 61 objects **~30× faster** than standard recursion (0.08s vs 2.5s validation time, ~19× end-to-end) and a remote catalog end-to-end **~6× faster** (2.9s vs 17.6s). Custom `--headers` are applied to remote fetches, `--fast-linting` additionally runs linting and geometry checks per object (removed in 2.0.0 — linting is now the default), and results are shown in the compact summary with errors grouped across the whole walk.

## Table of Contents

- [Latest News](#latest-news)
- [Documentation](#documentation)
- [Installation](#installation)
  - [Pip](#pip)
  - [Docker](#docker)
- [Usage](#usage)
  - [CLI Usage](#cli-usage)
  - [Configuration](#configuration)
  - [Geometry Validation](#geometry-validation)
  - [Python API Usage](#python-api-usage)
- [Examples](#examples)
  - [Basic Validation](#basic-validation)
  - [Recursive Validation](#recursive-validation)
  - [Asset Validation](#asset-validation)
  - [Link and Asset Validation](#link-and-asset-validation)
  - [Invalid STAC](#invalid-stac)
  - [Using HTTP Headers](#using-http-headers)
  - [Fast Validation](#fast-validation)
  - [STAC API Validation](#stac-api-validation)
- [Development](#development)
  - [Building Documentation](#building-documentation)
- [Sponsors and Supporters](#sponsors-and-supporters)
- [Contributing](#contributing)
  - [How to Contribute](#how-to-contribute)
  - [Development Guidelines](#development-guidelines)
  - [Reporting Issues](#reporting-issues)
- [License](#license)

## Documentation

The documentation is hosted on GitHub Pages at [stac-utils.github.io/stac-check](https://stac-utils.github.io/stac-check/).

For development and building the documentation locally, see the [Development](#development) section below.

## Installation

### Pip

```bash
$ pip install stac-check
```

For local development, this project uses [uv](https://docs.astral.sh/uv/):

```bash
$ uv sync --extra dev
```

Or with pip:

```bash
$ pip install -e '.[dev]'
```

### Docker

```bash
$ make build
$ make shell
```

## Usage

### CLI Usage

```
Usage: stac-check [OPTIONS] FILE

Options:
  --version                Show the version and exit.
  -l, --links              Validate links for format and response.
  -a, --assets             Validate assets for format and response.
  -m, --max-depth INTEGER  Maximum depth to traverse when recursing. Omit this
                           argument to get full recursion.
  -r, --recursive          Recursively validate all related stac objects.
  --no-assets-urls         Disables the opening of href links when validating assets
                           (enabled by default).
  --header KEY VALUE       HTTP header to include in the requests. Can be used
                           multiple times.
  --pydantic               Use stac-pydantic for enhanced validation with Pydantic models.
  -v, --verbose            Show per-asset validation details; without it only
                           a summary is printed.
  -o, --output FILE        Save output to the specified file.
  --fast                   Skip linting and geometry checks for maximum validation
                           speed. Also applies to --recursive.
  --item-collection        Validate item collection response. Can be combined with
                           --pages. Defaults to one page.
  --collections            Validate collections endpoint response. Can be combined with
                           --pages. Defaults to one page.
  --catalogs               Validate catalogs endpoint response (STAC API catalogs
                           extension). Can be combined with --pages. Defaults to one page.
  -p, --pages INTEGER      Maximum number of pages to validate per paginated list,
                           via --item-collection/--collections/--catalogs or
                           --recursive (default: one page per list; 0 for all
                           pages).
  --help                   Show this message and exit.
```

### Configuration

stac-check uses a configuration file to control which validation checks are performed. By default, it uses the built-in configuration at `stac_check/stac-check.config.yml`. You can customize the validation behavior by creating your own configuration file.

The configuration file has three main sections:

1. **linting**: Controls which general best practices checks are enabled
2. **geometry_validation**: Controls geometry-specific validation checks [BETA]
3. **settings**: Configures thresholds for certain checks

Here's an example of the configuration options:

```yaml
linting:
  # Identifiers should consist of only lowercase characters, numbers, '_', and '-'
  searchable_identifiers: true
  # Item name '{self.object_id}' should not contain ':' or '/'
  percent_encoded: true
  # Item file names should match their ids
  item_id_file_name: true
  # Collections and catalogs should be named collection.json and catalog.json
  catalog_id_file_name: true
  # A STAC collection should contain a summaries field
  check_summaries: true
  # Datetime fields should not be set to null
  null_datetime: true
  # best practices - check unlocated items to make sure bbox field is not set
  check_unlocated: true
  # best practices - recommend items have a geometry
  check_geometry: true
  # check to see if there are too many links
  bloated_links: true
  # best practices - check for bloated metadata in properties
  bloated_metadata: true
  # best practices - ensure thumbnail is a small file size ["png", "jpeg", "jpg", "webp"]
  check_thumbnail: true
  # best practices - ensure that links in catalogs and collections include a title field
  links_title: true
  # best practices - ensure that links in catalogs and collections include self link
  links_self: true

geometry_validation:
  # Master switch to enable/disable all geometry validation checks
  enabled: true
  # check if geometry coordinates are potentially ordered incorrectly (longitude, latitude)
  geometry_coordinates_order: true
  # check if geometry coordinates contain definite errors (latitude > ±90°, longitude > ±180°)
  geometry_coordinates_definite_errors: true
  # check if bbox matches the bounds of the geometry
  bbox_geometry_match: true
  # check if a bbox that crosses the antimeridian is correctly formatted
  bbox_antimeridian: true

settings:
  # number of links before the bloated links warning is shown
  max_links: 20
  # number of properties before the bloated metadata warning is shown
  max_properties: 20
```

To use a custom configuration file, set the `STAC_CHECK_CONFIG` environment variable to the path of your configuration file:

```bash
export STAC_CHECK_CONFIG=/path/to/your/config.yml
stac-check sample_files/1.0.0/core-item.json
```

### Geometry Validation

Geometry validation is a feature of stac-check that allows you to validate the geometry of your STAC items. This feature is enabled by default, but can be disabled by setting `geometry_validation.enabled` to `false` in your configuration file.

The geometry validation feature checks for the following:

*   Geometry coordinates are potentially ordered incorrectly (longitude, latitude)
*   Geometry coordinates contain definite errors (latitude > ±90°, longitude > ±180°)
*   Bbox matches the bounds of the geometry
*   Bbox that crosses the antimeridian is correctly formatted

You can customize the geometry validation behavior by setting the following options in your configuration file:

*   `geometry_validation.geometry_coordinates_order`: Check if geometry coordinates are potentially ordered incorrectly (longitude, latitude)
*   `geometry_validation.geometry_coordinates_definite_errors`: Check if geometry coordinates contain definite errors (latitude > ±90°, longitude > ±180°)
*   `geometry_validation.bbox_geometry_match`: Check if bbox matches the bounds of the geometry
*   `geometry_validation.bbox_antimeridian`: Check if a bbox that crosses the antimeridian is correctly formatted

### Python API Usage

```python
from stac_check.lint import Linter

linter = Linter('<json_path>')

for k, v in linter.create_best_practices_dict().items():
    print(k, ":", v)
```

## Examples

### Basic Validation

```bash
stac-check sample_files/1.0.0/core-item.json
```

<pre><b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 1.0.0 to version 1.1.0!

Validator: stac-valid 4.6.4

Validation method: stac-valid FastValidator

ITEM Passed: True

Schemas checked:
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

STAC Best Practices:
    Item name '20201211_223832_CS2' should only contain Searchable identifiers
    Identifiers should consist of only lowercase characters, numbers, '_', and '-'

    Item file names should match their ids: 'core-item' not equal to '20201211_223832_CS2

    Please avoid setting the datetime field to null, many clients search on this field

Geometry Validation [BETA]:
    Geometry coordinates may be in the wrong order (required order: longitude, latitude)

This object has 4 links
</pre>

### Recursive Validation

```bash
stac-check https://digital-atlas.s3.amazonaws.com/stac/public_stac/population/worldpop_2020/collection.json --recursive --verbose
```

Recursive validation walks the whole catalog in a single pass with stac-valid FastValidator and runs linting and geometry checks on every object by default. Add `--fast` to skip those checks for maximum speed:

```bash
stac-check catalog.json --recursive --fast
```

`--max-depth` caps how deep the walk goes (objects at or beyond the limit are not validated), and `--headers` apply to remote fetches. On remote STAC APIs the walk follows `rel=data`/`rel=items` links and paginates through each collections/items list — the first `rel="next"` page of each list by default (`--pages N` raises the cap, `--pages 0` follows every page; a note is printed when a list is cut short). Note that stac-check validates STAC 1.0.0 and later; documents declaring an older `stac_version` fail with a clear unsupported-version error instead of a cryptic schema failure.

Multi-asset modes (`--recursive`, `--collections`, `--item-collection`) print a header and a validation summary by default. Add `--verbose`/`-v` for per-asset detail, as shown below:

<pre><b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 1.0.0 to version 1.1.0!

Validator: stac-valid 4.6.4

Validation method: stac-valid FastValidator


Recursive: Validate all assets in a collection or catalog
Max-depth = unlimited
-------------------------

 Asset 1: https://digital-atlas.s3.amazonaws.com/stac/public_stac/population/worldpop_2020/collection.json

COLLECTION Passed: True

Schemas checked:
    https://schemas.stacspec.org/v1.0.0/collection-spec/json-schema/collection.json

STAC Best Practices:
    A STAC collection should contain a summaries field
    It is recommended to store information like eo:bands in summaries

-------------------------
 Asset 2: https://digital-atlas.s3.amazonaws.com/stac/public_stac/population/worldpop_2020/pop_2020/pop_2020.json

ITEM Passed: True
-------------------------

 Validation Summary

✅ Passed: 4/4
</pre>


### Asset Validation

```bash
stac-check sample_files/1.0.0/core-item.json --assets
```

<pre>
<b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 1.0.0 to version 1.1.0!

Validator: stac-valid 4.6.4

Validation method: stac-valid FastValidator

ITEM Passed: True

Schemas checked:
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

STAC Best Practices:
    Item name '20201211_223832_CS2' should only contain Searchable identifiers
    Identifiers should consist of only lowercase characters, numbers, '_', and '-'

    Item file names should match their ids: 'core-item' not equal to '20201211_223832_CS2

    Please avoid setting the datetime field to null, many clients search on this field

    A link to 'self' in links is strongly recommended


No ASSET format errors!

ASSET request errors:
    http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH

This object has 4 links
</pre>

### Link and Asset Validation

```bash
stac-check sample_files/1.0.0/core-item-bad-links.json --links --assets
```

<pre>
<b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 1.0.0 to version 1.1.0!

Validator: stac-valid 4.6.4

Validation method: stac-valid FastValidator

ITEM Passed: True

Schemas checked:
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

STAC Best Practices:
    Item name '20201211_223832_CS2' should only contain Searchable identifiers
    Identifiers should consist of only lowercase characters, numbers, '_', and '-'

    Item file names should match their ids: 'core-item-bad-links' not equal to '20201211_223832_CS2

    Please avoid setting the datetime field to null, many clients search on this field

    A link to 'self' in links is strongly recommended


ASSET format errors:
    https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg

ASSET request errors:
    https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg
    http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH

LINK format errors:
    http:/remotdata.io/catalog/20201211_223832_CS2/index.html

LINK request errors:
    http:/remotdata.io/catalog/20201211_223832_CS2/index.html

This object has 4 links
</pre>

### Invalid STAC

```bash
stac-check sample_files/1.0.0/bad-item.json
```

<pre>
<b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 1.0.0 to version 1.1.0!

Validator: stac-valid 4.6.4

Validation method: stac-valid FastValidator

ITEM Passed: False

Schemas checked:
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json
    https://stac-extensions.github.io/eo/v1.0.0/schema.json

Validation error type:
    FastValidationError
Validation error message:
    [Base Item] Field '$': must contain ['id'] properties

This object has 4 links
</pre>

### Using HTTP Headers

```bash
stac-check https://stac-catalog.eu/collections/sentinel-s2-l2a/items/item1 --assets --no-assets-urls --header x-api-key $MY_API_KEY --header foo bar
```

<pre>
<b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 1.0.0 to version 1.1.0!

Validator: stac-valid 4.6.4

Validation method: stac-valid FastValidator

ITEM Passed: True

Schemas checked: 
    https://stac-extensions.github.io/timestamps/v1.1.0/schema.json
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

STAC Best Practices: 
    A STAC collection should contain a summaries field
    It is recommended to store information like eo:bands in summaries


No ASSET format errors!

This object has 4 links
</pre>

### Fast Validation

stac-check always validates with stac-valid FastValidator. By default it also runs best practices linting and geometry checks; for large collections or when you only need spec compliance, use `--fast` to skip them for maximum validation speed.

```bash
stac-check large_collection.json --fast
```

<pre><b>stac-check: STAC spec validation and linting tool</b>

Validator: stac-valid 4.6.4

Validation method: stac-valid FastValidator

 Validation Summary

✅ Passed: 998/1000
❌ Failed: 2/1000

⚡ Timing Information:
  Total Validation Time: 245.67 ms
  Average per Object: 0.246 ms

Schemas checked:
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json
    https://stac-extensions.github.io/eo/v1.0.0/schema.json
    https://stac-extensions.github.io/projection/v1.0.0/schema.json

 Validation Errors

❌ STAC Spec Violation: Missing {'rel': 'collection'} in links array.
   Affected Items: 2 | Examples: item_1, item_2
</pre>

`--fast` also applies to `--recursive`, skipping the per-object linting and geometry checks across the whole catalog walk (see [Recursive Validation](#recursive-validation)).

The `--fast-linting` flag was removed in 2.0.0: linting and geometry checks already run by default.

Use `--fast` when:
- Validating large collections (100+ items)
- Recursively validating large or remote catalogs (`--recursive --fast`)
- You only need STAC spec compliance
- You want maximum validation speed

### STAC API Validation

stac-check can validate STAC API endpoints, including item collections, collections, and catalogs (STAC API catalogs extension) endpoints. It supports pagination and can validate multiple pages of results. Item collection (`{"type": "FeatureCollection", "features": [...]}`), collections endpoint (`{"collections": [...]}`), and catalogs endpoint (`{"catalogs": [...]}`) responses are auto-detected, so the corresponding flags are optional.

**Validating an Item Collection Endpoint:**

```bash
stac-check https://stac.geobon.org/collections/chelsa-clim/items --item-collection
```

<pre><b>stac-check: STAC spec validation and linting tool</b>

Validator: stac-valid 4.6.4

Item Collection: Validate all assets in a feature collection
Pages = 1

Valid ITEM: True

Schemas validated:
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

This object has 10 items
</pre>

**Validating Multiple Pages of an Item Collection:**

```bash
stac-check https://stac.geobon.org/collections/chelsa-clim/items --item-collection --pages 3
```

<pre><b>stac-check: STAC spec validation and linting tool</b>

Validator: stac-valid 4.6.4

Item Collection: Validate all assets in a feature collection
Pages = 3

Valid ITEM: True

Schemas validated:
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

This object has 30 items
</pre>

**Validating a Collections Endpoint:**

```bash
stac-check https://stac.geobon.org/collections --collections
```

<pre><b>stac-check: STAC spec validation and linting tool</b>

Validator: stac-valid 4.6.4

Collections: Validate all collections in a STAC API
Pages = 1

Valid COLLECTION: True

Schemas validated:
    https://schemas.stacspec.org/v1.0.0/collection-spec/json-schema/collection.json

This object has 5 collections
</pre>

## Development

### Building Documentation

Documentation is automatically built and published to GitHub Pages on every push to the `main` branch. You can view the latest version at [stac-utils.github.io/stac-check](https://stac-utils.github.io/stac-check/).

To build the documentation locally (for development or testing), you'll need Python >= 3.11 and the documentation dependencies:

```bash
# Install the package with documentation dependencies
uv sync --extra docs

# Build the documentation
make docs

# Open the built documentation
xdg-open docs/_build/html/index.html  # On Linux
open docs/_build/html/index.html    # On macOS
start docs/_build/html/index.html   # On Windows
```

Or using Docker:

```bash
# Build the Docker image and documentation
make docker-docs
```

The documentation is built using Sphinx with the following extensions:
- `sphinx.ext.autodoc` for API documentation
- `sphinx_click` for CLI documentation
- `sphinx_rtd_theme` for the ReadTheDocs theme
- `myst_parser` for Markdown support

## Sponsors and Supporters

The following organizations have contributed time and/or funding to support the development of this project:
- [Healy Hyperspatial](https://healy-hyperspatial.github.io/)
- [Radiant Earth Foundation](https://radiant.earth/)

<p align="left">
  <a href="https://healy-hyperspatial.github.io/"><img src="https://raw.githubusercontent.com/stac-utils/stac-fastapi-elasticsearch-opensearch/refs/heads/main/assets/hh-logo-blue.png" alt="Healy Hyperspatial" height="100" hspace="20"></a>
  <a href="https://radiant.earth/"><img src="assets/radiant-earth.webp" alt="Radiant Earth Foundation" height="100" hspace="20"></a>
</p>

We are grateful for the support of our sponsors who help make this project possible. If your organization uses stac-check and would like to become a sponsor, please reach out to us!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. **Fork the repository** - Create your own fork of the project
2. **Create a feature branch** - `git checkout -b feature/your-feature-name`
3. **Commit your changes** - Make sure to write clear, concise commit messages
4. **Push to your branch** - `git push origin feature/your-feature-name`
5. **Open a Pull Request** - Describe your changes in detail

### Development Guidelines

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Make sure all tests pass before submitting a PR

### Reporting Issues

If you find a bug or have a feature request, please open an issue on the [GitHub repository](https://github.com/stac-utils/stac-check/issues).

## License

This project is licensed under the Apache License 2.0.