# stac-check
## A linting and validation tool for STAC assets

The intent of this project is to provide a validation tool that also follows the official [STAC Best Practices document](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md)

---
### Documentation
[stac-check.readthedocs.io](https://stac-check.readthedocs.io/en/latest/)

---
### Install
`$ pip install stac-check`

or for local development

`$ pip install -e '.[dev]'`

---
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
  --help                   Show this message and exit.               Show this message and exit.
```
---
### Docker

```
$ make build
$ make shell
```
---
### Lint JSON

```
from stac_check.lint import Linter

linter = Linter('<json_path>')

for k, v in linter.create_best_practices_dict().items():
    print(k, ":", v)
```
---
### CLI Examples

``` stac-check https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json --recursive ```
```
 ____  ____  __    ___       ___  _  _  ____  ___  __ _
/ ___)(_  _)/ _\  / __)___  / __)/ )( \(  __)/ __)(  / )
\___ \  )( /    \( (__(___)( (__ ) __ ( ) _)( (__  )  (
(____/ (__)\_/\_/ \___)     \___)\_)(_/(____)\___)(__\_)

stac-check: STAC spec validaton and linting tool

Please upgrade from version 0.9.0 to version 1.0.0!

Validator: stac-validator 3.1.0


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
```

``` stac-check sample_files/0.9.0/landsat8-sample.json```

<pre><b>stac-check: STAC spec validaton and linting tool</b>

Please upgrade from version 0.9.0 to version 1.0.0!

Validator: stac-validator 2.3.0

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

``` stac-check sample_files/1.0.0/core-item.json --assets```
<pre>
<b>stac-check: STAC spec validaton and linting tool</b>

Thanks for using STAC version 1.0.0!

Validator: stac-validator 2.3.0

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



``` stac-check sample_files/1.0.0/core-item-bad-links.json --links --assets```
<pre>
<b>stac-check: STAC spec validaton and linting tool</b>

Thanks for using STAC version 1.0.0!

Validator: stac-validator 2.3.0

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

``` stac-check sample_files/0.9.0/bad-item.json```
<pre>
<b>stac-check: STAC spec validaton and linting tool</b>

Please upgrade from version 0.9.0 to version 1.0.0!

Validator: stac-validator 2.3.0

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
---
### Create local docs in the /docs folder
`$ pdoc --html --output-dir pdoc stac_check --force`
