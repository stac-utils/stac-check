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

## Table of Contents

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
- [Development](#development)
- [Sponsors and Supporters](#sponsors-and-supporters)
- [Contributing](#contributing)
  - [How to Contribute](#how-to-contribute)
  - [Development Guidelines](#development-guidelines)
  - [Reporting Issues](#reporting-issues)
- [License](#license)

## Documentation

The documentation is hosted on GitHub Pages at [stac-utils.github.io/stac-check](https://stac-utils.github.io/stac-check/).

### Building Documentation Locally

To build the documentation locally:

```bash
# Install the package with documentation dependencies
pip install -e ".[docs]"

# Build the documentation
make docs
```

The built documentation will be available in the `docs/_build/html` directory.

Alternatively, you can build the documentation using Docker:

```bash
# Build the Docker image and documentation
make docker-docs
```

## Installation

### Pip

```bash
$ pip install stac-check
```

For local development:

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
                           argument to get full recursion. Ignored if
                           `recursive == False`.
  -r, --recursive          Recursively validate all related stac objects.
  --no-assets-urls         Disables the opening of href links when validating assets
                           (enabled by default).
  --header KEY VALUE       HTTP header to include in the requests. Can be used
                           multiple times.
  --pydantic               Use stac-pydantic for enhanced validation with Pydantic models.
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
stac-check sample_files/0.9.0/landsat8-sample.json
```

<pre><b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 0.9.0 to version 1.1.0!

Validator: stac-validator 3.5.0

Valid ITEM: True

Schemas validated:
    https://cdn.staclint.com/v0.9.0/extension/eo.json
    https://cdn.staclint.com/v0.9.0/extension/view.json
    https://cdn.staclint.com/v0.9.0/item.json

STAC Best Practices:
    Item name 'LC81530252014153LGN00' should only contain Searchable identifiers
    Identifiers should consist of only lowercase characters, numbers, '_', and '-'
    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#searchable-identifiers

    Item file names should match their ids: 'landsat8-sample' not equal to 'LC81530252014153LGN00

    A link to 'self' in links is strongly recommended


This object has 4 links
</pre>

### Recursive Validation

```bash
stac-check https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json --recursive
```

<pre><b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 0.9.0 to version 1.1.0!

Validator: stac-validator 3.5.0


Recursive: Validate all assets in a collection or catalog
Max-depth = None
-------------------------
Asset 1 Validated: https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json

Valid COLLECTION: True

Schemas validated:
    https://cdn.staclint.com/v0.9.0/collection.json

STAC Best Practices:
    Object should be called 'collection.json' not 'landsat-collection.json'

    A STAC collection should contain a summaries field
    It is recommended to store information like eo:bands in summaries

    Links in catalogs and collections should always have a 'title' field

This object has 4 links

-------------------------
Asset 2 Validated: https://landsat-stac.s3.amazonaws.com/landsat-8-l1/paths/catalog.json

Valid: False
Schemas validated:
    https://cdn.staclint.com/v0.9.0/collection.json
Error Type: JSONDecodeError
Error Message: Expecting value: line 1 column 1 (char 0)
-------------------------
</pre>


### Asset Validation

```bash
stac-check sample_files/1.0.0/core-item.json --assets
```

<pre>
<b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 1.0.0 to version 1.1.0!

Validator: stac-validator 3.5.0

Valid ITEM: True

Schemas validated:
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

STAC Best Practices:
    Item name '20201211_223832_CS2' should only contain Searchable identifiers
    Identifiers should consist of only lowercase characters, numbers, '_', and '-'
    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#searchable-identifiers

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

Validator: stac-validator 3.5.0

Valid ITEM: True

Schemas validated:
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

STAC Best Practices:
    Item name '20201211_223832_CS2' should only contain Searchable identifiers
    Identifiers should consist of only lowercase characters, numbers, '_', and '-'
    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#searchable-identifiers

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
    http://catalog/collection.json
    http:/remotdata.io/catalog/20201211_223832_CS2/index.html

This object has 4 links
</pre>

### Invalid STAC

```bash
stac-check sample_files/0.9.0/bad-item.json
```

<pre>
<b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 0.9.0 to version 1.1.0!

Validator: stac-validator 3.5.0

Valid : False

Schemas validated:
    https://cdn.staclint.com/v0.9.0/item.json

STAC Best Practices:
    A link to 'self' in links is strongly recommended

Validation error type:
    ValidationError
Validation error message:
    'id' is a required property of the root of the STAC object

This object has 5 links
</pre>

### Using HTTP Headers

```bash
stac-check https://stac-catalog.eu/collections/sentinel-s2-l2a/items/item1 --assets --no-assets-urls --header x-api-key $MY_API_KEY --header foo bar
```

<pre>
<b>stac-check: STAC spec validation and linting tool</b>

Please upgrade from version 1.0.0 to version 1.1.0!

Validator: stac-validator 3.5.0

Valid ITEM: True

Schemas validated: 
    https://stac-extensions.github.io/timestamps/v1.1.0/schema.json
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

STAC Best Practices: 
    A STAC collection should contain a summaries field
    It is recommended to store information like eo:bands in summaries


No ASSET format errors!

This object has 4 links
</pre>

## Development

Create local docs in the /docs folder:

```bash
$ pdoc --output-dir pdoc ./stac_check
```

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