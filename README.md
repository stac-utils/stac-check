# stac-check
## Linting and validation tool for STAC assets

This project is a work in progress. The intent is to provide a validation tool that also follows the official STAC Best Practices document: https://github.com/radiantearth/stac-spec/blob/master/best-practices.md
    
``` pip install -e . ```    
    
``` stac_check https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json --recursive ```
```
 ____  ____  __    ___       ___  _  _  ____  ___  __ _ 
/ ___)(_  _)/ _\  / __)___  / __)/ )( \(  __)/ __)(  / )
\___ \  )( /    \( (__(___)( (__ ) __ ( ) _)( (__  )  ( 
(____/ (__)\_/\_/ \___)     \___)\_)(_/(____)\___)(__\_)
    
stac-check: STAC spec validaton and linting tool

Please upgrade from version 0.9.0 to version 1.0.0!

Validator: pystac 1.1.0
    Recursive: Validate all assets in a collection or catalog

Valid COLLECTION: True
Schemas validated: 
    https://cdn.staclint.com/v0.9.0/collection.json

Recursive validation has failed!
Validation error message: 
    Exception Could not read uri https://landsat-stac.s3.amazonaws.com/landsat-8-l1/paths/catalog.json

WARNING: STAC Best Practices asks for a summaries field in a STAC collection
    https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md

This object has 4 links
```

``` stac_check sample_files/0.9.0/landsat8-sample.json```

<pre><b>stac-check: STAC spec validaton and linting tool</b>
Please upgrade from version 0.9.0 to version 1.0.0!

Validator: stac-validator 2.4.0

Valid ITEM: True

STAC Best Practices: Item names should match their ids
    'landsat8-sample' not equal to 'LC81530252014153LGN00'

Schemas validated: 
    https://cdn.staclint.com/v0.9.0/extension/eo.json
    https://cdn.staclint.com/v0.9.0/extension/view.json
    https://cdn.staclint.com/v0.9.0/item.json

This object has 4 links
</pre>

``` stac_check sample_files/1.0.0/core-item.json --assets```    
<pre>
<b>stac-check: STAC spec validaton and linting tool</b>
Thanks for using STAC version 1.0.0!

Validator: stac-validator 2.4.0

Valid ITEM: True

STAC Best Practices: Item names should match their ids
    'core-item' not equal to '20201211_223832_CS2'

Schemas validated: 
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

No ASSET format errors!

ASSET request errors: 
    http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH

This object has 4 links
</pre>


   
``` stac_check sample_files/1.0.0/core-item-bad-links.json --links --assets```    
<pre>
<b>stac-check: STAC spec validaton and linting tool</b>
Thanks for using STAC version 1.0.0!

Validator: stac-validator 2.4.0

Valid ITEM: True

STAC Best Practices: Item names should match their ids
    'core-item-bad-links' not equal to '20201211_223832_CS2'

Schemas validated: 
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json

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
  
  
    
``` stac_check sample_files/0.9.0/bad-item.json```    
<pre>
<b>stac-check: STAC spec validaton and linting tool</b>
Please upgrade from version 0.9.0 to version 1.0.0!

Validator: stac-validator 2.4.0

Valid : False
Schemas validated: 
    https://cdn.staclint.com/v0.9.0/item.json
Validation error type: 
    ValidationError
Validation error message: 
    'id' is a required property of the root of the STAC object

This object has 5 links
</pre>