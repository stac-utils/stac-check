# stac-check
Linting and validation tool for STAC assets

This project is a work in progress. The intent is to provide a validation tool that also follows tthe official STAC Best Practices document: https://github.com/radiantearth/stac-spec/blob/master/best-practices.md

``` pipenv shell ```   
``` pip install -i https://test.pypi.org/simple/ stac-validator==2.3.0 ```   
``` pip install -e . ```   
``` stac_check sample_files/0.9.0/landsat8-sample.json```

<pre><b>stac-check: STAC spec validaton and linting tool</b>
<font color="#C01C28">Please upgrade from version 0.9.0 to version 1.0.0!</font>
<span style="background-color:#12488B"><font color="#D0CFCC">Validator: stac-validator 2.3.0</font></span>
<font color="#26A269">Valid ITEM: True</font>
<font color="#12488B">Schemas validated: </font>
<font color="#12488B">    https://cdn.staclint.com/v0.9.0/extension/eo.json,</font>
<font color="#12488B">    https://cdn.staclint.com/v0.9.0/extension/view.json,</font>
<font color="#12488B">    https://cdn.staclint.com/v0.9.0/item.json,</font>
<font color="#12488B"></font>
</pre>



``` stac_check sample_files/1.0.0/core-item.json --assets```    
<pre>
<b>stac-check: STAC spec validaton and linting tool</b>
Thanks for using STAC version 1.0.0!
Validator: stac-validator 2.3.0
Valid ITEM: True
Schemas validated: 
    https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json
No ASSET format errors!
ASSET request errors: 
    http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH
</pre>


   
``` stac_check sample_files/1.0.0/core-item-bad-links.json --links --assets```    
<pre>
<b>stac-check: STAC spec validaton and linting tool</b>
Thanks for using STAC version 1.0.0!
Validator: stac-validator 2.3.0
Valid ITEM: True
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
</pre>
  
  
    
``` stac_check sample_files/0.9.0/bad-item.json```    
<pre>
<b>stac-check: STAC spec validaton and linting tool</b>
Please upgrade from version 0.9.0 to version 1.0.0!
Validator: stac-validator 2.3.0
Valid : False
Schemas validated: 
    https://cdn.staclint.com/v0.9.0/item.json
Validation error type: 
    ValidationError
Validation error message: 
    'id' is a required property of the root of the STAC object
</pre>