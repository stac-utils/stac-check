# stac-check
Linting and validation tool for STAC assets

``` pipenv shell ```   
``` pip install -e . ```   
``` stac_check sample_files/0.9.0/landsat8-sample.json```

```
Please upgrade from version 0.9.0 to version 1.0.0!
{'version': '0.9.0', 'path': 'sample_files/0.9.0/landsat8-sample.json', 'schema': ['https://cdn.staclint.com/v0.9.0/extension/eo.json', 'https://cdn.staclint.com/v0.9.0/extension/view.json', 'https://cdn.staclint.com/v0.9.0/item.json'], 'valid_stac': True, 'asset_type': 'ITEM', 'validation_method': 'default'}
```
