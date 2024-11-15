API Reference
=============

.. raw:: html

    <embed>
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />
        <meta name="generator" content="pdoc 0.9.2" />
        <title>stac_check.lint API documentation</title>
        <meta name="description" content="" />
        <link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/sanitize.min.css" integrity="sha256-PK9q560IAAa6WVRRh76LtCaI8pjTJ2z11v0miyNNjrs=" crossorigin>
        <link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/typography.min.css" integrity="sha256-7l/o7C8jubJiy74VsKTidCy1yBkRtiUGbVkYBylBqUg=" crossorigin>
        <link rel="stylesheet preload" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/styles/github.min.css" crossorigin>
        <style>:root{--highlight-color:#fe9}.flex{display:flex !important}body{line-height:1.5em}#content{padding:20px}#sidebar{padding:30px;overflow:hidden}#sidebar > *:last-child{margin-bottom:2cm}.http-server-breadcrumbs{font-size:130%;margin:0 0 15px 0}#footer{font-size:.75em;padding:5px 30px;border-top:1px solid #ddd;text-align:right}#footer p{margin:0 0 0 1em;display:inline-block}#footer p:last-child{margin-right:30px}h1,h2,h3,h4,h5{font-weight:300}h1{font-size:2.5em;line-height:1.1em}h2{font-size:1.75em;margin:1em 0 .50em 0}h3{font-size:1.4em;margin:25px 0 10px 0}h4{margin:0;font-size:105%}h1:target,h2:target,h3:target,h4:target,h5:target,h6:target{background:var(--highlight-color);padding:.2em 0}a{color:#058;text-decoration:none;transition:color .3s ease-in-out}a:hover{color:#e82}.title code{font-weight:bold}h2[id^="header-"]{margin-top:2em}.ident{color:#900}pre code{background:#f8f8f8;font-size:.8em;line-height:1.4em}code{background:#f2f2f1;padding:1px 4px;overflow-wrap:break-word}h1 code{background:transparent}pre{background:#f8f8f8;border:0;border-top:1px solid #ccc;border-bottom:1px solid #ccc;margin:1em 0;padding:1ex}#http-server-module-list{display:flex;flex-flow:column}#http-server-module-list div{display:flex}#http-server-module-list dt{min-width:10%}#http-server-module-list p{margin-top:0}.toc ul,#index{list-style-type:none;margin:0;padding:0}#index code{background:transparent}#index h3{border-bottom:1px solid #ddd}#index ul{padding:0}#index h4{margin-top:.6em;font-weight:bold}@media (min-width:200ex){#index .two-column{column-count:2}}@media (min-width:300ex){#index .two-column{column-count:3}}dl{margin-bottom:2em}dl dl:last-child{margin-bottom:4em}dd{margin:0 0 1em 3em}#header-classes + dl > dd{margin-bottom:3em}dd dd{margin-left:2em}dd p{margin:10px 0}.name{background:#eee;font-weight:bold;font-size:.85em;padding:5px 10px;display:inline-block;min-width:40%}.name:hover{background:#e0e0e0}dt:target .name{background:var(--highlight-color)}.name > span:first-child{white-space:nowrap}.name.class > span:nth-child(2){margin-left:.4em}.inherited{color:#999;border-left:5px solid #eee;padding-left:1em}.inheritance em{font-style:normal;font-weight:bold}.desc h2{font-weight:400;font-size:1.25em}.desc h3{font-size:1em}.desc dt code{background:inherit}.source summary,.git-link-div{color:#666;text-align:right;font-weight:400;font-size:.8em;text-transform:uppercase}.source summary > *{white-space:nowrap;cursor:pointer}.git-link{color:inherit;margin-left:1em}.source pre{max-height:500px;overflow:auto;margin:0}.source pre code{font-size:12px;overflow:visible}.hlist{list-style:none}.hlist li{display:inline}.hlist li:after{content:',\2002'}.hlist li:last-child:after{content:none}.hlist .hlist{display:inline;padding-left:1em}img{max-width:100%}td{padding:0 .5em}.admonition{padding:.1em .5em;margin-bottom:1em}.admonition-title{font-weight:bold}.admonition.note,.admonition.info,.admonition.important{background:#aef}.admonition.todo,.admonition.versionadded,.admonition.tip,.admonition.hint{background:#dfd}.admonition.warning,.admonition.versionchanged,.admonition.deprecated{background:#fd4}.admonition.error,.admonition.danger,.admonition.caution{background:lightpink}</style>
        <style media="screen and (min-width: 7000px)">@media screen and (min-width:7000px){#sidebar{width:30%;height:100vh;overflow:auto;position:sticky;top:0}#content{width:70%;max-width:100ch;padding:3em 4em;border-left:1px solid #ddd}pre code{font-size:1em}.item .name{font-size:1em}main{display:flex;flex-direction:row-reverse;justify-content:flex-end}.toc ul ul,#index ul{padding-left:1.5em}.toc > ul > li{margin-top:.5em}}</style>
        <style media="print">@media print{#sidebar h1{page-break-before:always}.source{display:none}}@media print{*{background:transparent !important;color:#000 !important;box-shadow:none !important;text-shadow:none !important}a[href]:after{content:" (" attr(href) ")";font-size:90%}a[href][title]:after{content:none}abbr[title]:after{content:" (" attr(title) ")"}.ir a:after,a[href^="javascript:"]:after,a[href^="#"]:after{content:""}pre,blockquote{border:1px solid #999;page-break-inside:avoid}thead{display:table-header-group}tr,img{page-break-inside:avoid}img{max-width:100% !important}@page{margin:0.5cm}p,h2,h3{orphans:3;widows:3}h1,h2,h3,h4,h5,h6{page-break-after:avoid}}</style>
        <script defer src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/highlight.min.js" integrity="sha256-Uv3H6lx7dJmRfRvH8TH6kJD1TSK1aFcwgx+mdg3epi8=" crossorigin></script>
        <script>window.addEventListener('DOMContentLoaded', () => hljs.initHighlighting())</script>
        </head>
        <body>
        <main>
        <article id="content">
        <header>
        <h1 class="title">Module <code>stac_check.lint</code></h1>
        </header>
        <section id="section-intro">
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">
        from stac_validator.validate import StacValidate
        from stac_validator.utilities import is_valid_url
        import json
        import yaml
        import os
        from dataclasses import dataclass
        import requests
        from typing import Optional, Union, Dict, Any, List
        from dotenv import load_dotenv
        import importlib.metadata
	import importlib.resources

        load_dotenv()

        @dataclass
        class Linter:
            &#34;&#34;&#34;A class for linting STAC JSON files and generating validation messages.

            Args:
                item (Union[str, dict]): A URL, file name, or dictionary representing a STAC JSON file.
                config_file (Optional[str], optional): A path to a YAML configuration file. Defaults to None.
                assets (bool, optional): A boolean value indicating whether to validate assets. Defaults to False.
                links (bool, optional): A boolean value indicating whether to validate links. Defaults to False.
                recursive (bool, optional): A boolean value indicating whether to perform recursive validation. Defaults to False.
                max_depth (Optional[int], optional): An optional integer indicating the maximum depth to validate recursively. Defaults to None.

            Attributes:
                data (dict): A dictionary representing the STAC JSON file.
                message (dict): A dictionary containing the validation message for the STAC JSON file.
                config (dict): A dictionary containing the configuration settings.
                asset_type (str): A string representing the asset type, if one is specified.
                version (str): A string representing the version of the STAC standard used in the STAC JSON file.
                validator_version (str): A string representing the version of the STAC validator used to validate the STAC JSON file.
                validate_all (dict): A dictionary containing the validation message for all STAC JSON files found recursively, if recursive validation was performed.
                valid_stac (bool): A boolean value indicating whether the STAC JSON file is valid.
                error_type (str): A string representing the type of error in the STAC JSON file, if one exists.
                error_msg (str): A string representing the error message in the STAC JSON file, if one exists.
                invalid_asset_format (List[str]): A list of URLs with invalid asset formats, if assets were validated.
                invalid_asset_request (List[str]): A list of URLs with invalid asset requests, if assets were validated.
                invalid_link_format (List[str]): A list of URLs with invalid link formats, if links were validated.
                invalid_link_request (List[str]): A list of URLs with invalid link requests, if links were validated.
                schema (List[str]): A list of the STAC JSON file&#39;s JSON schema files.
                object_id (str): A string representing the STAC JSON file&#39;s ID.
                file_name (str): A string representing the name of the file containing the STAC JSON data.
                best_practices_msg (str): A string representing best practices messages for the STAC JSON file.

            Methods:
                parse_config(config_file: Optional[str] = None) -&gt; Dict:
                    Parses a YAML configuration file and returns a dictionary with the configuration settings.

                def get_asset_name(self, file: Union[str, Dict] = None) -&gt; str:
                    Returns the name of a file.

                load_data(self, file: Union[str, Dict]) -&gt; Dict:
                    Loads a STAC JSON file from a URL or file path and returns a dictionary representation.

                validate_file(self, file: Union[str, dict]) -&gt; Dict[str, Any]:
                    Validates a STAC JSON file and returns a dictionary with the validation message.

                recursive_validation(self, file: Union[str, Dict[str, Any]]) -&gt; str:
                    Validates a STAC JSON file recursively and returns a dictionary with the validation message.

                set_update_message(self) -&gt; str:
                    Sets a message regarding the recommended version of the STAC JSON file standard.

                check_links_assets(self, num_links: int, url_type: str, format_type: str) -&gt; List[str]:
                    Checks whether the STAC JSON file has links or assets with invalid formats or requests.

                check_error_type(self) -&gt; str:                  
                    Checks whether the STAC JSON file has an error type.

                check_error_message(self) -&gt; str:
                    Checks whether the STAC JSON file has an error message. 

                def check_summaries(self) -&gt; bool:
                    Checks whether the STAC JSON file has summaries.

                check_bloated_links(self, max_links: Optional[int] = 20) -&gt; bool:
                    Checks whether the STAC JSON file has bloated links.

                check_bloated_metadata(self, max_properties: Optional[int] = 20) -&gt; bool:
                    Checks whether the STAC JSON file has bloated metadata.

                check_datetime_null(self) -&gt; bool:
                    Checks whether the STAC JSON file has a null datetime.

                check_unlocated(self) -&gt; bool:
                    Checks whether the STAC JSON file has unlocated items.

                check_geometry_null(self) -&gt; bool:
                    Checks whether the STAC JSON file has a null geometry.  

                check_searchable_identifiers(self) -&gt; bool: 
                    Checks whether the STAC JSON file has searchable identifiers.

                check_percent_encoded(self) -&gt; bool:
                    Checks whether the STAC JSON file has percent-encoded characters.

                check_thumbnail(self) -&gt; bool:
                    Checks whether the STAC JSON file has a thumbnail.

                check_links_title_field(self) -&gt; bool:
                    Checks whether the STAC JSON file has a title field in its links.

                check_links_self(self) -&gt; bool:
                    Checks whether the STAC JSON file has a self link.

                check_item_id_file_name(self) -&gt; bool:
                    Checks whether the filename of an Item conforms to the STAC specification.

                check_catalog_file_name(self) -&gt; str:
                    Checks whether the filename of a Catalog or Collection conforms to the STAC specification.

                create_best_practices_dict(self) -&gt; Dict[str, Any]:
                    Creates a dictionary with best practices recommendations for the STAC JSON file.

                create_best_practices_msg(self) -&gt; List[str]:
                    Creates a message with best practices recommendations for the STAC JSON file.
            &#34;&#34;&#34;
            item: Union[str, dict] # url, file name, or dictionary
            config_file: Optional[str] = None
            assets: bool = False
            links: bool = False
            recursive: bool = False
            max_depth: Optional[int] = None

            def __post_init__(self):
                self.data = self.load_data(self.item)
                self.message = self.validate_file(self.item)
                self.config = self.parse_config(self.config_file)
                self.asset_type = self.message[&#34;asset_type&#34;] if &#34;asset_type&#34; in self.message else &#34;&#34;
                self.version = self.message[&#34;version&#34;] if &#34;version&#34; in self.message else &#34;&#34;
                self.validator_version = importlib.metadata.distribution(&#34;stac-validator&#34;).version
                self.validate_all = self.recursive_validation(self.item)
                self.valid_stac = self.message[&#34;valid_stac&#34;]
                self.error_type = self.check_error_type()
                self.error_msg = self.check_error_message()
                self.invalid_asset_format = self.check_links_assets(10, &#34;assets&#34;, &#34;format&#34;) if self.assets else None
                self.invalid_asset_request = self.check_links_assets(10, &#34;assets&#34;, &#34;request&#34;) if self.assets else None
                self.invalid_link_format = self.check_links_assets(10, &#34;links&#34;, &#34;format&#34;) if self.links else None
                self.invalid_link_request = self.check_links_assets(10, &#34;links&#34;, &#34;request&#34;) if self.links else None
                self.schema = self.message[&#34;schema&#34;] if &#34;schema&#34; in self.message else []
                self.object_id = self.data[&#34;id&#34;] if &#34;id&#34; in self.data else &#34;&#34;
                self.file_name = self.get_asset_name(self.item)
                self.best_practices_msg = self.create_best_practices_msg()

            @staticmethod
            def parse_config(config_file: Optional[str] = None) -&gt; Dict:
                &#34;&#34;&#34;Parse the configuration file for STAC checks.

                The method first looks for a file path specified in the `STAC_CHECK_CONFIG`
                environment variable. If the variable is defined, the method loads the
                YAML configuration file located at that path. Otherwise, it loads the default
                configuration file packaged with the `stac-check` module.

                If `config_file` is specified, the method also loads the YAML configuration
                file located at that path and merges its contents with the default or
                environment-based configuration.

                Args:
                    config_file (str): The path to the YAML configuration file.

                Returns:
                    A dictionary containing the parsed configuration values.

                Raises:
                    IOError: If `config_file` is specified but cannot be read.
                    yaml.YAMLError: If any YAML syntax errors occur while parsing the
                        configuration file(s).
                &#34;&#34;&#34;
                default_config_file = os.getenv(&#34;STAC_CHECK_CONFIG&#34;)
                if default_config_file:
                    with open(default_config_file) as f:
                        default_config = yaml.load(f, Loader=yaml.FullLoader)
                else:
                    with importlib.resources.open_text(__name__, &#34;stac-check.config.yml&#34;) as f:
                        default_config = yaml.load(f, Loader=yaml.FullLoader)
                if config_file:
                    with open(config_file) as f:
                        config = yaml.load(f, Loader=yaml.FullLoader)
                    default_config.update(config)
                    
                return default_config

            def get_asset_name(self, file: Union[str, Dict] = None) -&gt; str:
                &#34;&#34;&#34;Extracts the name of an asset from its file path or from a STAC item asset dictionary.

                Args:
                    file (Union[str, dict], optional): A string representing the file path to the asset or a dictionary representing the
                        asset as specified in a STAC item&#39;s `assets` property.

                Returns:
                    A string containing the name of the asset.

                Raises:
                    TypeError: If the input `file` is not a string or a dictionary.
                &#34;&#34;&#34;
                if isinstance(file, str):
                    return os.path.basename(file).split(&#39;.&#39;)[0]
                else:
                    return file[&#34;id&#34;]

            def load_data(self, file: Union[str, Dict]) -&gt; Dict:
                &#34;&#34;&#34;Loads JSON data from a file or URL.

                Args:
                    file (Union[str, Dict]): A string representing the path to a JSON file or a dictionary containing the JSON data.

                Returns:
                    A dictionary containing the loaded JSON data.

                Raises:
                    TypeError: If the input `file` is not a string or dictionary.
                    ValueError: If `file` is a string that doesn&#39;t represent a valid URL or file path.
                    requests.exceptions.RequestException: If there is an error making a request to a URL.
                    JSONDecodeError: If the JSON data cannot be decoded.
                    FileNotFoundError: If the specified file cannot be found.
                &#34;&#34;&#34;

                if isinstance(file, str):
                    if is_valid_url(file):
                        resp = requests.get(file)
                        data = resp.json()
                    else:
                        with open(file) as json_file:
                            data = json.load(json_file)
                    return data
                else:
                    return file

            def validate_file(self, file: Union[str, dict]) -&gt; Dict[str, Any]:
                &#34;&#34;&#34;Validates the given file path or STAC dictionary against the validation schema.

                Args:
                    file (Union[str, dict]): A string representing the file path to the STAC file or a dictionary representing the STAC
                        item.

                Returns:
                    A dictionary containing the results of the validation, including the status of the validation and any errors
                    encountered.

                Raises:
                    ValueError: If `file` is not a valid file path or STAC dictionary.
                &#34;&#34;&#34;
                if isinstance(file, str):
                    stac = StacValidate(file, links=self.links, assets=self.assets)
                    stac.run()
                elif isinstance(file, dict):
                    stac = StacValidate()
                    stac.validate_dict(file)
                else:
                    raise ValueError(&#34;Input must be a file path or STAC dictionary.&#34;)
                return stac.message[0]

            def recursive_validation(self, file: Union[str, Dict[str, Any]]) -&gt; str:
                &#34;&#34;&#34;Recursively validate a STAC item or catalog file and its child items.

                Args:
                    file (Union[str, Dict[str, Any]]): A string representing the file path to the STAC item or catalog, or a
                        dictionary representing the STAC item or catalog.

                Returns:
                    A string containing the validation message.

                Raises:
                    TypeError: If the input `file` is not a string or a dictionary.
                &#34;&#34;&#34;
                if self.recursive:
                    if isinstance(file, str):
                        stac = StacValidate(file, recursive=True, max_depth=self.max_depth)
                        stac.run()
                    else:
                        stac = StacValidate(recursive=True, max_depth=self.max_depth)
                        stac.validate_dict(file)
                    return stac.message

            def set_update_message(self) -&gt; str:
                &#34;&#34;&#34;Returns a message for users to update their STAC version.

                Returns:
                    A string containing a message for users to update their STAC version.
                &#34;&#34;&#34;
                if self.version != &#34;1.0.0&#34;:
                    return f&#34;Please upgrade from version {self.version} to version 1.0.0!&#34;
                else:
                    return &#34;Thanks for using STAC version 1.0.0!&#34;

            def check_links_assets(self, num_links: int, url_type: str, format_type: str) -&gt; List[str]:
                &#34;&#34;&#34;Checks the links and assets in the STAC catalog and returns a list of invalid links of a specified type and format.

                Args:
                    num_links (int): The maximum number of invalid links to return.
                    url_type (str): The type of URL to check, which can be either &#39;self&#39; or &#39;external&#39;.
                    format_type (str): The format of the URL to check, which can be either &#39;html&#39; or &#39;json&#39;.

                Returns:
                    A list of invalid links of the specified type and format. If there are no invalid links, an empty list is returned.
                &#34;&#34;&#34;
                links = []
                if f&#34;{url_type}_validated&#34; in self.message:
                    for invalid_request_url in self.message[f&#34;{url_type}_validated&#34;][f&#34;{format_type}_invalid&#34;]:
                        if invalid_request_url not in links and &#39;http&#39; in invalid_request_url:
                            links.append(invalid_request_url)
                        num_links = num_links - 1
                        if num_links == 0:
                            return links
                return links

            def check_error_type(self) -&gt; str:
                &#34;&#34;&#34;Returns the error type of a STAC validation if it exists in the validation message, 
                and an empty string otherwise.

                Returns:
                    str: A string containing the error type of a STAC validation if it exists in the validation message, and an
                    empty string otherwise.
                &#34;&#34;&#34;
                if &#34;error_type&#34; in self.message:
                    return self.message[&#34;error_type&#34;]
                else:
                    return &#34;&#34;

            def check_error_message(self) -&gt; str:
                &#34;&#34;&#34;Checks whether the `message` attribute contains an `error_message` field.

                Returns:
                    A string containing the value of the `error_message` field, or an empty string if the field is not present.
                &#34;&#34;&#34;
                if &#34;error_message&#34; in self.message:
                    return self.message[&#34;error_message&#34;]
                else:
                    return &#34;&#34;

            def check_summaries(self) -&gt; bool:
                &#34;&#34;&#34;Check if a Collection asset has a &#34;summaries&#34; property.

                Returns:
                    A boolean indicating whether the Collection asset has a &#34;summaries&#34; property.
                &#34;&#34;&#34;
                if self.asset_type == &#34;COLLECTION&#34;:
                    return &#34;summaries&#34; in self.data

            def check_bloated_links(self, max_links: Optional[int] = 20) -&gt; bool:
                &#34;&#34;&#34;Checks if the number of links in the STAC data exceeds a certain maximum.

                Args:
                    max_links (Optional[int]): The maximum number of links that the STAC data is allowed to have. Default is 20.

                Returns:
                    bool: A boolean indicating if the number of links in the STAC data exceeds the specified maximum.
                &#34;&#34;&#34;
                if &#34;links&#34; in self.data:
                    return len(self.data[&#34;links&#34;]) &gt; max_links

            def check_bloated_metadata(self, max_properties: Optional[int] = 20) -&gt; bool:
                &#34;&#34;&#34;Checks whether a STAC item&#39;s metadata contains too many properties.

                Args:
                    max_properties (int, optional): The maximum number of properties that the metadata can contain before it is
                        considered too bloated. Defaults to 20.

                Returns:
                    bool: True if the number of properties in the metadata exceeds the maximum number of properties specified by
                        `max_properties`, False otherwise.
                &#34;&#34;&#34;
                if &#34;properties&#34; in self.data:
                    return len(self.data[&#34;properties&#34;].keys()) &gt; max_properties
                return False

            def check_datetime_null(self) -&gt; bool:
                &#34;&#34;&#34;Checks if the STAC item has a null datetime property.

                Returns:
                    bool: A boolean indicating whether the datetime property is null (True) or not (False).
                &#34;&#34;&#34;
                if &#34;properties&#34; in self.data:
                    if &#34;datetime&#34; in self.data[&#34;properties&#34;]:
                        if self.data[&#34;properties&#34;][&#34;datetime&#34;] == None:
                            return True
                else:
                    return False
                return False

            def check_unlocated(self) -&gt; bool:
                &#34;&#34;&#34;Checks if a STAC item is unlocated, i.e., has no geometry but has a bounding box.

                Returns:
                    bool: True if the STAC item is unlocated, False otherwise.
                &#34;&#34;&#34;
                if &#34;geometry&#34; in self.data:
                    return self.data[&#34;geometry&#34;] is None and self.data[&#34;bbox&#34;] is not None

            def check_geometry_null(self) -&gt; bool:
                &#34;&#34;&#34;Checks if a STAC item has a null geometry property.
                    
                Returns:
                    bool: A boolean indicating whether the geometry property is null (True) or not (False).          
                &#34;&#34;&#34;
                if &#34;geometry&#34; in self.data:
                    return self.data[&#34;geometry&#34;] is None

            def check_searchable_identifiers(self) -&gt; bool:
                &#34;&#34;&#34;Checks if the identifiers of a STAC item are searchable, i.e., 
                they only contain lowercase letters, numbers, hyphens, and underscores.
                
                Returns:
                    bool: True if the identifiers are searchable, False otherwise.        
                &#34;&#34;&#34;
                if self.asset_type == &#34;ITEM&#34;: 
                    for letter in self.object_id:
                        if letter.islower() or letter.isnumeric() or letter == &#39;-&#39; or letter == &#39;_&#39;:
                            pass
                        else:
                            return False  
                return True

            def check_percent_encoded(self) -&gt; bool:
                &#34;&#34;&#34;Checks if the identifiers of a STAC item are percent-encoded, i.e.,
                they only contain lowercase letters, numbers, hyphens, and underscores.

                Returns:
                    bool: True if the identifiers are percent-encoded, False otherwise.
                &#34;&#34;&#34;
                return self.asset_type == &#34;ITEM&#34; and &#34;/&#34; in self.object_id or &#34;:&#34; in self.object_id

            def check_thumbnail(self) -&gt; bool:
                &#34;&#34;&#34;Checks if the thumbnail of a STAC item is valid, i.e., it has a valid format.
                
                Returns:
                    bool: True if the thumbnail is valid, False otherwise.
                &#34;&#34;&#34;
                if &#34;assets&#34; in self.data:
                    if &#34;thumbnail&#34; in self.data[&#34;assets&#34;]:
                        if &#34;type&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;]:
                            if &#34;png&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;] or &#34;jpeg&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;] or \
                                &#34;jpg&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;] or &#34;webp&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;]:
                                return True
                            else:
                                return False
                return True
            
            def check_links_title_field(self) -&gt; bool:
                &#34;&#34;&#34;Checks if all links in a STAC collection or catalog have a &#39;title&#39; field.
                The &#39;title&#39; field is not required for the &#39;self&#39; link.

                Returns:
                    bool: True if all links have a &#39;title&#39; field, False otherwise.
                &#34;&#34;&#34;
                if self.asset_type == &#34;COLLECTION&#34; or self.asset_type == &#34;CATALOG&#34;:
                    for link in self.data[&#34;links&#34;]:
                        if &#34;title&#34; not in link and link[&#34;rel&#34;] != &#34;self&#34;:
                            return False
                return True


            def check_links_self(self) -&gt; bool:
                &#34;&#34;&#34;Checks whether the &#34;self&#34; link is present in the STAC collection or catalog or absent in STAC item.
                
                Returns:
                    bool: True if the &#34;self&#34; link is present in STAC collection or catalog or absent in STAC item, False otherwise.
                &#34;&#34;&#34;
                if self.asset_type == &#34;ITEM&#34;:
                    return True
                if self.asset_type == &#34;COLLECTION&#34; or self.asset_type == &#34;CATALOG&#34;:
                    for link in self.data[&#34;links&#34;]:
                        if &#34;self&#34; in link[&#34;rel&#34;]:
                            return True
                return False

            def check_item_id_file_name(self) -&gt; bool:
                if self.asset_type == &#34;ITEM&#34; and self.object_id != self.file_name:
                    return False
                else:
                    return True

            def check_catalog_file_name(self) -&gt; bool:
                &#34;&#34;&#34;Checks whether the filename of a Catalog or Collection conforms to the STAC specification.
                
                Returns:
                    bool: True if the filename is valid, False otherwise.
                &#34;&#34;&#34;
                if isinstance(self.item, str) and &#34;.json&#34; in self.item:
                    if self.asset_type == &#34;CATALOG&#34; and &#39;catalog.json&#39; not in self.item:
                        return False 
                    elif self.asset_type == &#34;COLLECTION&#34; and &#39;collection.json&#39; not in self.item:
                        return False
                    return True
                else:
                    return True

            def create_best_practices_dict(self) -&gt; Dict:
                &#34;&#34;&#34;Creates a dictionary of best practices violations for the current STAC object. The violations are determined
                by a set of configurable linting rules specified in the config file.

                Returns:
                    A dictionary of best practices violations for the current STAC object. The keys in the dictionary correspond
                    to the linting rules that were violated, and the values are lists of strings containing error messages and
                    recommendations for how to fix the violations.
                &#34;&#34;&#34;
                best_practices_dict = {}
                config = self.config[&#34;linting&#34;]
                max_links = self.config[&#34;settings&#34;][&#34;max_links&#34;]
                max_properties = self.config[&#34;settings&#34;][&#34;max_properties&#34;]

                # best practices - item ids should only contain searchable identifiers
                if self.check_searchable_identifiers() == False and config[&#34;searchable_identifiers&#34;] == True: 
                    msg_1 = f&#34;Item name &#39;{self.object_id}&#39; should only contain Searchable identifiers&#34;
                    msg_2 = f&#34;Identifiers should consist of only lowercase characters, numbers, &#39;_&#39;, and &#39;-&#39;&#34;
                    best_practices_dict[&#34;searchable_identifiers&#34;] = [msg_1, msg_2]

                # best practices - item ids should not contain &#39;:&#39; or &#39;/&#39; characters
                if self.check_percent_encoded() and config[&#34;percent_encoded&#34;] == True:
                    msg_1 = f&#34;Item name &#39;{self.object_id}&#39; should not contain &#39;:&#39; or &#39;/&#39;&#34;
                    msg_2 = f&#34;https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#item-ids&#34;
                    best_practices_dict[&#34;percent_encoded&#34;] = [msg_1, msg_2]

                # best practices - item ids should match file names
                if not self.check_item_id_file_name() and config[&#34;item_id_file_name&#34;] == True:
                    msg_1 = f&#34;Item file names should match their ids: &#39;{self.file_name}&#39; not equal to &#39;{self.object_id}&#34;
                    best_practices_dict[&#34;check_item_id&#34;] = [msg_1]

                # best practices - collection and catalog file names should be collection.json and catalog.json 
                if self.check_catalog_file_name() == False and config[&#34;catalog_id_file_name&#34;] == True: 
                    msg_1 = f&#34;Object should be called &#39;{self.asset_type.lower()}.json&#39; not &#39;{self.file_name}.json&#39;&#34;
                    best_practices_dict[&#34;check_catalog_id&#34;] = [msg_1]

                # best practices - collections should contain summaries
                if self.check_summaries() == False and config[&#34;check_summaries&#34;] == True:
                    msg_1 = f&#34;A STAC collection should contain a summaries field&#34;
                    msg_2 = f&#34;It is recommended to store information like eo:bands in summaries&#34;
                    best_practices_dict[&#34;check_summaries&#34;] = [msg_1, msg_2]

                # best practices - datetime fields should not be set to null
                if self.check_datetime_null() and config[&#34;null_datetime&#34;] == True:
                    msg_1 = f&#34;Please avoid setting the datetime field to null, many clients search on this field&#34;
                    best_practices_dict[&#34;datetime_null&#34;] = [msg_1]

                # best practices - check unlocated items to make sure bbox field is not set
                if self.check_unlocated() and config[&#34;check_unlocated&#34;] == True:
                    msg_1 = f&#34;Unlocated item. Please avoid setting the bbox field when geometry is set to null&#34;
                    best_practices_dict[&#34;check_unlocated&#34;] = [msg_1]

                # best practices - recommend items have a geometry
                if self.check_geometry_null() and config[&#34;check_geometry&#34;] == True:
                    msg_1 = f&#34;All items should have a geometry field. STAC is not meant for non-spatial data&#34;
                    best_practices_dict[&#34;null_geometry&#34;] = [msg_1]

                # check to see if there are too many links
                if self.check_bloated_links(max_links=max_links) and config[&#34;bloated_links&#34;] == True:
                    msg_1 = f&#34;You have {len(self.data[&#39;links&#39;])} links. Please consider using sub-collections or sub-catalogs&#34;
                    best_practices_dict[&#34;bloated_links&#34;] = [msg_1]

                # best practices - check for bloated metadata in properties
                if self.check_bloated_metadata(max_properties=max_properties) and config[&#34;bloated_metadata&#34;] == True:
                    msg_1 = f&#34;You have {len(self.data[&#39;properties&#39;])} properties. Please consider using links to avoid bloated metadata&#34;
                    best_practices_dict[&#34;bloated_metadata&#34;] = [msg_1]

                # best practices - ensure thumbnail is a small file size [&#34;png&#34;, &#34;jpeg&#34;, &#34;jpg&#34;, &#34;webp&#34;]
                if not self.check_thumbnail() and self.asset_type == &#34;ITEM&#34; and config[&#34;check_thumbnail&#34;] == True:
                    msg_1 = f&#34;A thumbnail should have a small file size ie. png, jpeg, jpg, webp&#34;
                    best_practices_dict[&#34;check_thumbnail&#34;] = [msg_1]

                # best practices - ensure that links in catalogs and collections include a title field
                if not self.check_links_title_field() and config[&#34;links_title&#34;] == True:
                    msg_1 = f&#34;Links in catalogs and collections should always have a &#39;title&#39; field&#34;
                    best_practices_dict[&#34;check_links_title&#34;] = [msg_1]

                # best practices - ensure that links in catalogs and collections include self link
                if not self.check_links_self() and config[&#34;links_self&#34;] == True:
                    msg_1 = f&#34;A link to &#39;self&#39; in links is strongly recommended&#34;
                    best_practices_dict[&#34;check_links_self&#34;] = [msg_1]

                return best_practices_dict

            def create_best_practices_msg(self) -&gt; List[str]:
                &#34;&#34;&#34;
                Generates a list of best practices messages based on the results of the &#39;create_best_practices_dict&#39; method.

                Returns:
                    A list of strings, where each string contains a best practice message. Each message starts with the 
                    &#39;STAC Best Practices:&#39; base string and is followed by a specific recommendation. Each message is indented 
                    with four spaces, and there is an empty string between each message for readability.
                &#34;&#34;&#34;
                best_practices = list()
                base_string = &#34;STAC Best Practices: &#34;
                best_practices.append(base_string)

                for _,v in self.create_best_practices_dict().items():
                    for value in v:
                        best_practices.extend([&#34;    &#34; +value])  
                    best_practices.extend([&#34;&#34;])

                return best_practices</code></pre>
        </details>
        </section>
        <section>
        </section>
        <section>
        </section>
        <section>
        </section>
        <section>
        <h2 class="section-title" id="header-classes">Classes</h2>
        <dl>
        <dt id="stac_check.lint.Linter"><code class="flex name class">
        <span>class <span class="ident">Linter</span></span>
        <span>(</span><span>item: Union[str, dict], config_file: Optional[str] = None, assets: bool = False, links: bool = False, recursive: bool = False, max_depth: Optional[int] = None)</span>
        </code></dt>
        <dd>
        <div class="desc"><p>A class for linting STAC JSON files and generating validation messages.</p>
        <h2 id="args">Args</h2>
        <dl>
        <dt><strong><code>item</code></strong> :&ensp;<code>Union[str, dict]</code></dt>
        <dd>A URL, file name, or dictionary representing a STAC JSON file.</dd>
        <dt><strong><code>config_file</code></strong> :&ensp;<code>Optional[str]</code>, optional</dt>
        <dd>A path to a YAML configuration file. Defaults to None.</dd>
        <dt><strong><code>assets</code></strong> :&ensp;<code>bool</code>, optional</dt>
        <dd>A boolean value indicating whether to validate assets. Defaults to False.</dd>
        <dt><strong><code>links</code></strong> :&ensp;<code>bool</code>, optional</dt>
        <dd>A boolean value indicating whether to validate links. Defaults to False.</dd>
        <dt><strong><code>recursive</code></strong> :&ensp;<code>bool</code>, optional</dt>
        <dd>A boolean value indicating whether to perform recursive validation. Defaults to False.</dd>
        <dt><strong><code>max_depth</code></strong> :&ensp;<code>Optional[int]</code>, optional</dt>
        <dd>An optional integer indicating the maximum depth to validate recursively. Defaults to None.</dd>
        </dl>
        <h2 id="attributes">Attributes</h2>
        <dl>
        <dt><strong><code>data</code></strong> :&ensp;<code>dict</code></dt>
        <dd>A dictionary representing the STAC JSON file.</dd>
        <dt><strong><code>message</code></strong> :&ensp;<code>dict</code></dt>
        <dd>A dictionary containing the validation message for the STAC JSON file.</dd>
        <dt><strong><code>config</code></strong> :&ensp;<code>dict</code></dt>
        <dd>A dictionary containing the configuration settings.</dd>
        <dt><strong><code>asset_type</code></strong> :&ensp;<code>str</code></dt>
        <dd>A string representing the asset type, if one is specified.</dd>
        <dt><strong><code>version</code></strong> :&ensp;<code>str</code></dt>
        <dd>A string representing the version of the STAC standard used in the STAC JSON file.</dd>
        <dt><strong><code>validator_version</code></strong> :&ensp;<code>str</code></dt>
        <dd>A string representing the version of the STAC validator used to validate the STAC JSON file.</dd>
        <dt><strong><code>validate_all</code></strong> :&ensp;<code>dict</code></dt>
        <dd>A dictionary containing the validation message for all STAC JSON files found recursively, if recursive validation was performed.</dd>
        <dt><strong><code>valid_stac</code></strong> :&ensp;<code>bool</code></dt>
        <dd>A boolean value indicating whether the STAC JSON file is valid.</dd>
        <dt><strong><code>error_type</code></strong> :&ensp;<code>str</code></dt>
        <dd>A string representing the type of error in the STAC JSON file, if one exists.</dd>
        <dt><strong><code>error_msg</code></strong> :&ensp;<code>str</code></dt>
        <dd>A string representing the error message in the STAC JSON file, if one exists.</dd>
        <dt><strong><code>invalid_asset_format</code></strong> :&ensp;<code>List[str]</code></dt>
        <dd>A list of URLs with invalid asset formats, if assets were validated.</dd>
        <dt><strong><code>invalid_asset_request</code></strong> :&ensp;<code>List[str]</code></dt>
        <dd>A list of URLs with invalid asset requests, if assets were validated.</dd>
        <dt><strong><code>invalid_link_format</code></strong> :&ensp;<code>List[str]</code></dt>
        <dd>A list of URLs with invalid link formats, if links were validated.</dd>
        <dt><strong><code>invalid_link_request</code></strong> :&ensp;<code>List[str]</code></dt>
        <dd>A list of URLs with invalid link requests, if links were validated.</dd>
        <dt><strong><code>schema</code></strong> :&ensp;<code>List[str]</code></dt>
        <dd>A list of the STAC JSON file's JSON schema files.</dd>
        <dt><strong><code>object_id</code></strong> :&ensp;<code>str</code></dt>
        <dd>A string representing the STAC JSON file's ID.</dd>
        <dt><strong><code>file_name</code></strong> :&ensp;<code>str</code></dt>
        <dd>A string representing the name of the file containing the STAC JSON data.</dd>
        <dt><strong><code>best_practices_msg</code></strong> :&ensp;<code>str</code></dt>
        <dd>A string representing best practices messages for the STAC JSON file.</dd>
        </dl>
        <h2 id="methods">Methods</h2>
        <p>parse_config(config_file: Optional[str] = None) -&gt; Dict:
        Parses a YAML configuration file and returns a dictionary with the configuration settings.</p>
        <p>def get_asset_name(self, file: Union[str, Dict] = None) -&gt; str:
        Returns the name of a file.</p>
        <p>load_data(self, file: Union[str, Dict]) -&gt; Dict:
        Loads a STAC JSON file from a URL or file path and returns a dictionary representation.</p>
        <p>validate_file(self, file: Union[str, dict]) -&gt; Dict[str, Any]:
        Validates a STAC JSON file and returns a dictionary with the validation message.</p>
        <p>recursive_validation(self, file: Union[str, Dict[str, Any]]) -&gt; str:
        Validates a STAC JSON file recursively and returns a dictionary with the validation message.</p>
        <p>set_update_message(self) -&gt; str:
        Sets a message regarding the recommended version of the STAC JSON file standard.</p>
        <p>check_links_assets(self, num_links: int, url_type: str, format_type: str) -&gt; List[str]:
        Checks whether the STAC JSON file has links or assets with invalid formats or requests.</p>
        <p>check_error_type(self) -&gt; str:
        <br>
        Checks whether the STAC JSON file has an error type.</p>
        <p>check_error_message(self) -&gt; str:
        Checks whether the STAC JSON file has an error message. </p>
        <p>def check_summaries(self) -&gt; bool:
        Checks whether the STAC JSON file has summaries.</p>
        <p>check_bloated_links(self, max_links: Optional[int] = 20) -&gt; bool:
        Checks whether the STAC JSON file has bloated links.</p>
        <p>check_bloated_metadata(self, max_properties: Optional[int] = 20) -&gt; bool:
        Checks whether the STAC JSON file has bloated metadata.</p>
        <p>check_datetime_null(self) -&gt; bool:
        Checks whether the STAC JSON file has a null datetime.</p>
        <p>check_unlocated(self) -&gt; bool:
        Checks whether the STAC JSON file has unlocated items.</p>
        <p>check_geometry_null(self) -&gt; bool:
        Checks whether the STAC JSON file has a null geometry.
        </p>
        <p>check_searchable_identifiers(self) -&gt; bool:
        Checks whether the STAC JSON file has searchable identifiers.</p>
        <p>check_percent_encoded(self) -&gt; bool:
        Checks whether the STAC JSON file has percent-encoded characters.</p>
        <p>check_thumbnail(self) -&gt; bool:
        Checks whether the STAC JSON file has a thumbnail.</p>
        <p>check_links_title_field(self) -&gt; bool:
        Checks whether the STAC JSON file has a title field in its links.</p>
        <p>check_links_self(self) -&gt; bool:
        Checks whether the STAC JSON file has a self link.</p>
        <p>check_item_id_file_name(self) -&gt; bool:
        Checks whether the filename of an Item conforms to the STAC specification.</p>
        <p>check_catalog_file_name(self) -&gt; str:
        Checks whether the filename of a Catalog or Collection conforms to the STAC specification.</p>
        <p>create_best_practices_dict(self) -&gt; Dict[str, Any]:
        Creates a dictionary with best practices recommendations for the STAC JSON file.</p>
        <p>create_best_practices_msg(self) -&gt; List[str]:
        Creates a message with best practices recommendations for the STAC JSON file.</p></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">@dataclass
        class Linter:
            &#34;&#34;&#34;A class for linting STAC JSON files and generating validation messages.

            Args:
                item (Union[str, dict]): A URL, file name, or dictionary representing a STAC JSON file.
                config_file (Optional[str], optional): A path to a YAML configuration file. Defaults to None.
                assets (bool, optional): A boolean value indicating whether to validate assets. Defaults to False.
                links (bool, optional): A boolean value indicating whether to validate links. Defaults to False.
                recursive (bool, optional): A boolean value indicating whether to perform recursive validation. Defaults to False.
                max_depth (Optional[int], optional): An optional integer indicating the maximum depth to validate recursively. Defaults to None.

            Attributes:
                data (dict): A dictionary representing the STAC JSON file.
                message (dict): A dictionary containing the validation message for the STAC JSON file.
                config (dict): A dictionary containing the configuration settings.
                asset_type (str): A string representing the asset type, if one is specified.
                version (str): A string representing the version of the STAC standard used in the STAC JSON file.
                validator_version (str): A string representing the version of the STAC validator used to validate the STAC JSON file.
                validate_all (dict): A dictionary containing the validation message for all STAC JSON files found recursively, if recursive validation was performed.
                valid_stac (bool): A boolean value indicating whether the STAC JSON file is valid.
                error_type (str): A string representing the type of error in the STAC JSON file, if one exists.
                error_msg (str): A string representing the error message in the STAC JSON file, if one exists.
                invalid_asset_format (List[str]): A list of URLs with invalid asset formats, if assets were validated.
                invalid_asset_request (List[str]): A list of URLs with invalid asset requests, if assets were validated.
                invalid_link_format (List[str]): A list of URLs with invalid link formats, if links were validated.
                invalid_link_request (List[str]): A list of URLs with invalid link requests, if links were validated.
                schema (List[str]): A list of the STAC JSON file&#39;s JSON schema files.
                object_id (str): A string representing the STAC JSON file&#39;s ID.
                file_name (str): A string representing the name of the file containing the STAC JSON data.
                best_practices_msg (str): A string representing best practices messages for the STAC JSON file.

            Methods:
                parse_config(config_file: Optional[str] = None) -&gt; Dict:
                    Parses a YAML configuration file and returns a dictionary with the configuration settings.

                def get_asset_name(self, file: Union[str, Dict] = None) -&gt; str:
                    Returns the name of a file.

                load_data(self, file: Union[str, Dict]) -&gt; Dict:
                    Loads a STAC JSON file from a URL or file path and returns a dictionary representation.

                validate_file(self, file: Union[str, dict]) -&gt; Dict[str, Any]:
                    Validates a STAC JSON file and returns a dictionary with the validation message.

                recursive_validation(self, file: Union[str, Dict[str, Any]]) -&gt; str:
                    Validates a STAC JSON file recursively and returns a dictionary with the validation message.

                set_update_message(self) -&gt; str:
                    Sets a message regarding the recommended version of the STAC JSON file standard.

                check_links_assets(self, num_links: int, url_type: str, format_type: str) -&gt; List[str]:
                    Checks whether the STAC JSON file has links or assets with invalid formats or requests.

                check_error_type(self) -&gt; str:                  
                    Checks whether the STAC JSON file has an error type.

                check_error_message(self) -&gt; str:
                    Checks whether the STAC JSON file has an error message. 

                def check_summaries(self) -&gt; bool:
                    Checks whether the STAC JSON file has summaries.

                check_bloated_links(self, max_links: Optional[int] = 20) -&gt; bool:
                    Checks whether the STAC JSON file has bloated links.

                check_bloated_metadata(self, max_properties: Optional[int] = 20) -&gt; bool:
                    Checks whether the STAC JSON file has bloated metadata.

                check_datetime_null(self) -&gt; bool:
                    Checks whether the STAC JSON file has a null datetime.

                check_unlocated(self) -&gt; bool:
                    Checks whether the STAC JSON file has unlocated items.

                check_geometry_null(self) -&gt; bool:
                    Checks whether the STAC JSON file has a null geometry.  

                check_searchable_identifiers(self) -&gt; bool: 
                    Checks whether the STAC JSON file has searchable identifiers.

                check_percent_encoded(self) -&gt; bool:
                    Checks whether the STAC JSON file has percent-encoded characters.

                check_thumbnail(self) -&gt; bool:
                    Checks whether the STAC JSON file has a thumbnail.

                check_links_title_field(self) -&gt; bool:
                    Checks whether the STAC JSON file has a title field in its links.

                check_links_self(self) -&gt; bool:
                    Checks whether the STAC JSON file has a self link.

                check_item_id_file_name(self) -&gt; bool:
                    Checks whether the filename of an Item conforms to the STAC specification.

                check_catalog_file_name(self) -&gt; str:
                    Checks whether the filename of a Catalog or Collection conforms to the STAC specification.

                create_best_practices_dict(self) -&gt; Dict[str, Any]:
                    Creates a dictionary with best practices recommendations for the STAC JSON file.

                create_best_practices_msg(self) -&gt; List[str]:
                    Creates a message with best practices recommendations for the STAC JSON file.
            &#34;&#34;&#34;
            item: Union[str, dict] # url, file name, or dictionary
            config_file: Optional[str] = None
            assets: bool = False
            links: bool = False
            recursive: bool = False
            max_depth: Optional[int] = None

            def __post_init__(self):
                self.data = self.load_data(self.item)
                self.message = self.validate_file(self.item)
                self.config = self.parse_config(self.config_file)
                self.asset_type = self.message[&#34;asset_type&#34;] if &#34;asset_type&#34; in self.message else &#34;&#34;
                self.version = self.message[&#34;version&#34;] if &#34;version&#34; in self.message else &#34;&#34;
                self.validator_version = importlib.metadata.distribution(&#34;stac-validator&#34;).version
                self.validate_all = self.recursive_validation(self.item)
                self.valid_stac = self.message[&#34;valid_stac&#34;]
                self.error_type = self.check_error_type()
                self.error_msg = self.check_error_message()
                self.invalid_asset_format = self.check_links_assets(10, &#34;assets&#34;, &#34;format&#34;) if self.assets else None
                self.invalid_asset_request = self.check_links_assets(10, &#34;assets&#34;, &#34;request&#34;) if self.assets else None
                self.invalid_link_format = self.check_links_assets(10, &#34;links&#34;, &#34;format&#34;) if self.links else None
                self.invalid_link_request = self.check_links_assets(10, &#34;links&#34;, &#34;request&#34;) if self.links else None
                self.schema = self.message[&#34;schema&#34;] if &#34;schema&#34; in self.message else []
                self.object_id = self.data[&#34;id&#34;] if &#34;id&#34; in self.data else &#34;&#34;
                self.file_name = self.get_asset_name(self.item)
                self.best_practices_msg = self.create_best_practices_msg()

            @staticmethod
            def parse_config(config_file: Optional[str] = None) -&gt; Dict:
                &#34;&#34;&#34;Parse the configuration file for STAC checks.

                The method first looks for a file path specified in the `STAC_CHECK_CONFIG`
                environment variable. If the variable is defined, the method loads the
                YAML configuration file located at that path. Otherwise, it loads the default
                configuration file packaged with the `stac-check` module.

                If `config_file` is specified, the method also loads the YAML configuration
                file located at that path and merges its contents with the default or
                environment-based configuration.

                Args:
                    config_file (str): The path to the YAML configuration file.

                Returns:
                    A dictionary containing the parsed configuration values.

                Raises:
                    IOError: If `config_file` is specified but cannot be read.
                    yaml.YAMLError: If any YAML syntax errors occur while parsing the
                        configuration file(s).
                &#34;&#34;&#34;
                default_config_file = os.getenv(&#34;STAC_CHECK_CONFIG&#34;)
                if default_config_file:
                    with open(default_config_file) as f:
                        default_config = yaml.load(f, Loader=yaml.FullLoader)
                else:
                    with importlib.resources.open_text(__name__, &#34;stac-check.config.yml&#34;) as f:
                        default_config = yaml.load(f, Loader=yaml.FullLoader)
                if config_file:
                    with open(config_file) as f:
                        config = yaml.load(f, Loader=yaml.FullLoader)
                    default_config.update(config)
                    
                return default_config

            def get_asset_name(self, file: Union[str, Dict] = None) -&gt; str:
                &#34;&#34;&#34;Extracts the name of an asset from its file path or from a STAC item asset dictionary.

                Args:
                    file (Union[str, dict], optional): A string representing the file path to the asset or a dictionary representing the
                        asset as specified in a STAC item&#39;s `assets` property.

                Returns:
                    A string containing the name of the asset.

                Raises:
                    TypeError: If the input `file` is not a string or a dictionary.
                &#34;&#34;&#34;
                if isinstance(file, str):
                    return os.path.basename(file).split(&#39;.&#39;)[0]
                else:
                    return file[&#34;id&#34;]

            def load_data(self, file: Union[str, Dict]) -&gt; Dict:
                &#34;&#34;&#34;Loads JSON data from a file or URL.

                Args:
                    file (Union[str, Dict]): A string representing the path to a JSON file or a dictionary containing the JSON data.

                Returns:
                    A dictionary containing the loaded JSON data.

                Raises:
                    TypeError: If the input `file` is not a string or dictionary.
                    ValueError: If `file` is a string that doesn&#39;t represent a valid URL or file path.
                    requests.exceptions.RequestException: If there is an error making a request to a URL.
                    JSONDecodeError: If the JSON data cannot be decoded.
                    FileNotFoundError: If the specified file cannot be found.
                &#34;&#34;&#34;

                if isinstance(file, str):
                    if is_valid_url(file):
                        resp = requests.get(file)
                        data = resp.json()
                    else:
                        with open(file) as json_file:
                            data = json.load(json_file)
                    return data
                else:
                    return file

            def validate_file(self, file: Union[str, dict]) -&gt; Dict[str, Any]:
                &#34;&#34;&#34;Validates the given file path or STAC dictionary against the validation schema.

                Args:
                    file (Union[str, dict]): A string representing the file path to the STAC file or a dictionary representing the STAC
                        item.

                Returns:
                    A dictionary containing the results of the validation, including the status of the validation and any errors
                    encountered.

                Raises:
                    ValueError: If `file` is not a valid file path or STAC dictionary.
                &#34;&#34;&#34;
                if isinstance(file, str):
                    stac = StacValidate(file, links=self.links, assets=self.assets)
                    stac.run()
                elif isinstance(file, dict):
                    stac = StacValidate()
                    stac.validate_dict(file)
                else:
                    raise ValueError(&#34;Input must be a file path or STAC dictionary.&#34;)
                return stac.message[0]

            def recursive_validation(self, file: Union[str, Dict[str, Any]]) -&gt; str:
                &#34;&#34;&#34;Recursively validate a STAC item or catalog file and its child items.

                Args:
                    file (Union[str, Dict[str, Any]]): A string representing the file path to the STAC item or catalog, or a
                        dictionary representing the STAC item or catalog.

                Returns:
                    A string containing the validation message.

                Raises:
                    TypeError: If the input `file` is not a string or a dictionary.
                &#34;&#34;&#34;
                if self.recursive:
                    if isinstance(file, str):
                        stac = StacValidate(file, recursive=True, max_depth=self.max_depth)
                        stac.run()
                    else:
                        stac = StacValidate(recursive=True, max_depth=self.max_depth)
                        stac.validate_dict(file)
                    return stac.message

            def set_update_message(self) -&gt; str:
                &#34;&#34;&#34;Returns a message for users to update their STAC version.

                Returns:
                    A string containing a message for users to update their STAC version.
                &#34;&#34;&#34;
                if self.version != &#34;1.0.0&#34;:
                    return f&#34;Please upgrade from version {self.version} to version 1.0.0!&#34;
                else:
                    return &#34;Thanks for using STAC version 1.0.0!&#34;

            def check_links_assets(self, num_links: int, url_type: str, format_type: str) -&gt; List[str]:
                &#34;&#34;&#34;Checks the links and assets in the STAC catalog and returns a list of invalid links of a specified type and format.

                Args:
                    num_links (int): The maximum number of invalid links to return.
                    url_type (str): The type of URL to check, which can be either &#39;self&#39; or &#39;external&#39;.
                    format_type (str): The format of the URL to check, which can be either &#39;html&#39; or &#39;json&#39;.

                Returns:
                    A list of invalid links of the specified type and format. If there are no invalid links, an empty list is returned.
                &#34;&#34;&#34;
                links = []
                if f&#34;{url_type}_validated&#34; in self.message:
                    for invalid_request_url in self.message[f&#34;{url_type}_validated&#34;][f&#34;{format_type}_invalid&#34;]:
                        if invalid_request_url not in links and &#39;http&#39; in invalid_request_url:
                            links.append(invalid_request_url)
                        num_links = num_links - 1
                        if num_links == 0:
                            return links
                return links

            def check_error_type(self) -&gt; str:
                &#34;&#34;&#34;Returns the error type of a STAC validation if it exists in the validation message, 
                and an empty string otherwise.

                Returns:
                    str: A string containing the error type of a STAC validation if it exists in the validation message, and an
                    empty string otherwise.
                &#34;&#34;&#34;
                if &#34;error_type&#34; in self.message:
                    return self.message[&#34;error_type&#34;]
                else:
                    return &#34;&#34;

            def check_error_message(self) -&gt; str:
                &#34;&#34;&#34;Checks whether the `message` attribute contains an `error_message` field.

                Returns:
                    A string containing the value of the `error_message` field, or an empty string if the field is not present.
                &#34;&#34;&#34;
                if &#34;error_message&#34; in self.message:
                    return self.message[&#34;error_message&#34;]
                else:
                    return &#34;&#34;

            def check_summaries(self) -&gt; bool:
                &#34;&#34;&#34;Check if a Collection asset has a &#34;summaries&#34; property.

                Returns:
                    A boolean indicating whether the Collection asset has a &#34;summaries&#34; property.
                &#34;&#34;&#34;
                if self.asset_type == &#34;COLLECTION&#34;:
                    return &#34;summaries&#34; in self.data

            def check_bloated_links(self, max_links: Optional[int] = 20) -&gt; bool:
                &#34;&#34;&#34;Checks if the number of links in the STAC data exceeds a certain maximum.

                Args:
                    max_links (Optional[int]): The maximum number of links that the STAC data is allowed to have. Default is 20.

                Returns:
                    bool: A boolean indicating if the number of links in the STAC data exceeds the specified maximum.
                &#34;&#34;&#34;
                if &#34;links&#34; in self.data:
                    return len(self.data[&#34;links&#34;]) &gt; max_links

            def check_bloated_metadata(self, max_properties: Optional[int] = 20) -&gt; bool:
                &#34;&#34;&#34;Checks whether a STAC item&#39;s metadata contains too many properties.

                Args:
                    max_properties (int, optional): The maximum number of properties that the metadata can contain before it is
                        considered too bloated. Defaults to 20.

                Returns:
                    bool: True if the number of properties in the metadata exceeds the maximum number of properties specified by
                        `max_properties`, False otherwise.
                &#34;&#34;&#34;
                if &#34;properties&#34; in self.data:
                    return len(self.data[&#34;properties&#34;].keys()) &gt; max_properties
                return False

            def check_datetime_null(self) -&gt; bool:
                &#34;&#34;&#34;Checks if the STAC item has a null datetime property.

                Returns:
                    bool: A boolean indicating whether the datetime property is null (True) or not (False).
                &#34;&#34;&#34;
                if &#34;properties&#34; in self.data:
                    if &#34;datetime&#34; in self.data[&#34;properties&#34;]:
                        if self.data[&#34;properties&#34;][&#34;datetime&#34;] == None:
                            return True
                else:
                    return False
                return False

            def check_unlocated(self) -&gt; bool:
                &#34;&#34;&#34;Checks if a STAC item is unlocated, i.e., has no geometry but has a bounding box.

                Returns:
                    bool: True if the STAC item is unlocated, False otherwise.
                &#34;&#34;&#34;
                if &#34;geometry&#34; in self.data:
                    return self.data[&#34;geometry&#34;] is None and self.data[&#34;bbox&#34;] is not None

            def check_geometry_null(self) -&gt; bool:
                &#34;&#34;&#34;Checks if a STAC item has a null geometry property.
                    
                Returns:
                    bool: A boolean indicating whether the geometry property is null (True) or not (False).          
                &#34;&#34;&#34;
                if &#34;geometry&#34; in self.data:
                    return self.data[&#34;geometry&#34;] is None

            def check_searchable_identifiers(self) -&gt; bool:
                &#34;&#34;&#34;Checks if the identifiers of a STAC item are searchable, i.e., 
                they only contain lowercase letters, numbers, hyphens, and underscores.
                
                Returns:
                    bool: True if the identifiers are searchable, False otherwise.        
                &#34;&#34;&#34;
                if self.asset_type == &#34;ITEM&#34;: 
                    for letter in self.object_id:
                        if letter.islower() or letter.isnumeric() or letter == &#39;-&#39; or letter == &#39;_&#39;:
                            pass
                        else:
                            return False  
                return True

            def check_percent_encoded(self) -&gt; bool:
                &#34;&#34;&#34;Checks if the identifiers of a STAC item are percent-encoded, i.e.,
                they only contain lowercase letters, numbers, hyphens, and underscores.

                Returns:
                    bool: True if the identifiers are percent-encoded, False otherwise.
                &#34;&#34;&#34;
                return self.asset_type == &#34;ITEM&#34; and &#34;/&#34; in self.object_id or &#34;:&#34; in self.object_id

            def check_thumbnail(self) -&gt; bool:
                &#34;&#34;&#34;Checks if the thumbnail of a STAC item is valid, i.e., it has a valid format.
                
                Returns:
                    bool: True if the thumbnail is valid, False otherwise.
                &#34;&#34;&#34;
                if &#34;assets&#34; in self.data:
                    if &#34;thumbnail&#34; in self.data[&#34;assets&#34;]:
                        if &#34;type&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;]:
                            if &#34;png&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;] or &#34;jpeg&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;] or \
                                &#34;jpg&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;] or &#34;webp&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;]:
                                return True
                            else:
                                return False
                return True
            
            def check_links_title_field(self) -&gt; bool:
                &#34;&#34;&#34;Checks if all links in a STAC collection or catalog have a &#39;title&#39; field.
                The &#39;title&#39; field is not required for the &#39;self&#39; link.

                Returns:
                    bool: True if all links have a &#39;title&#39; field, False otherwise.
                &#34;&#34;&#34;
                if self.asset_type == &#34;COLLECTION&#34; or self.asset_type == &#34;CATALOG&#34;:
                    for link in self.data[&#34;links&#34;]:
                        if &#34;title&#34; not in link and link[&#34;rel&#34;] != &#34;self&#34;:
                            return False
                return True


            def check_links_self(self) -&gt; bool:
                &#34;&#34;&#34;Checks whether the &#34;self&#34; link is present in the STAC collection or catalog or absent in STAC item.
                
                Returns:
                    bool: True if the &#34;self&#34; link is present in STAC collection or catalog or absent in STAC item, False otherwise.
                &#34;&#34;&#34;
                if self.asset_type == &#34;ITEM&#34;:
                    return True
                if self.asset_type == &#34;COLLECTION&#34; or self.asset_type == &#34;CATALOG&#34;:
                    for link in self.data[&#34;links&#34;]:
                        if &#34;self&#34; in link[&#34;rel&#34;]:
                            return True
                return False

            def check_item_id_file_name(self) -&gt; bool:
                if self.asset_type == &#34;ITEM&#34; and self.object_id != self.file_name:
                    return False
                else:
                    return True

            def check_catalog_file_name(self) -&gt; bool:
                &#34;&#34;&#34;Checks whether the filename of a Catalog or Collection conforms to the STAC specification.
                
                Returns:
                    bool: True if the filename is valid, False otherwise.
                &#34;&#34;&#34;
                if isinstance(self.item, str) and &#34;.json&#34; in self.item:
                    if self.asset_type == &#34;CATALOG&#34; and &#39;catalog.json&#39; not in self.item:
                        return False 
                    elif self.asset_type == &#34;COLLECTION&#34; and &#39;collection.json&#39; not in self.item:
                        return False
                    return True
                else:
                    return True

            def create_best_practices_dict(self) -&gt; Dict:
                &#34;&#34;&#34;Creates a dictionary of best practices violations for the current STAC object. The violations are determined
                by a set of configurable linting rules specified in the config file.

                Returns:
                    A dictionary of best practices violations for the current STAC object. The keys in the dictionary correspond
                    to the linting rules that were violated, and the values are lists of strings containing error messages and
                    recommendations for how to fix the violations.
                &#34;&#34;&#34;
                best_practices_dict = {}
                config = self.config[&#34;linting&#34;]
                max_links = self.config[&#34;settings&#34;][&#34;max_links&#34;]
                max_properties = self.config[&#34;settings&#34;][&#34;max_properties&#34;]

                # best practices - item ids should only contain searchable identifiers
                if self.check_searchable_identifiers() == False and config[&#34;searchable_identifiers&#34;] == True: 
                    msg_1 = f&#34;Item name &#39;{self.object_id}&#39; should only contain Searchable identifiers&#34;
                    msg_2 = f&#34;Identifiers should consist of only lowercase characters, numbers, &#39;_&#39;, and &#39;-&#39;&#34;
                    best_practices_dict[&#34;searchable_identifiers&#34;] = [msg_1, msg_2]

                # best practices - item ids should not contain &#39;:&#39; or &#39;/&#39; characters
                if self.check_percent_encoded() and config[&#34;percent_encoded&#34;] == True:
                    msg_1 = f&#34;Item name &#39;{self.object_id}&#39; should not contain &#39;:&#39; or &#39;/&#39;&#34;
                    msg_2 = f&#34;https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#item-ids&#34;
                    best_practices_dict[&#34;percent_encoded&#34;] = [msg_1, msg_2]

                # best practices - item ids should match file names
                if not self.check_item_id_file_name() and config[&#34;item_id_file_name&#34;] == True:
                    msg_1 = f&#34;Item file names should match their ids: &#39;{self.file_name}&#39; not equal to &#39;{self.object_id}&#34;
                    best_practices_dict[&#34;check_item_id&#34;] = [msg_1]

                # best practices - collection and catalog file names should be collection.json and catalog.json 
                if self.check_catalog_file_name() == False and config[&#34;catalog_id_file_name&#34;] == True: 
                    msg_1 = f&#34;Object should be called &#39;{self.asset_type.lower()}.json&#39; not &#39;{self.file_name}.json&#39;&#34;
                    best_practices_dict[&#34;check_catalog_id&#34;] = [msg_1]

                # best practices - collections should contain summaries
                if self.check_summaries() == False and config[&#34;check_summaries&#34;] == True:
                    msg_1 = f&#34;A STAC collection should contain a summaries field&#34;
                    msg_2 = f&#34;It is recommended to store information like eo:bands in summaries&#34;
                    best_practices_dict[&#34;check_summaries&#34;] = [msg_1, msg_2]

                # best practices - datetime fields should not be set to null
                if self.check_datetime_null() and config[&#34;null_datetime&#34;] == True:
                    msg_1 = f&#34;Please avoid setting the datetime field to null, many clients search on this field&#34;
                    best_practices_dict[&#34;datetime_null&#34;] = [msg_1]

                # best practices - check unlocated items to make sure bbox field is not set
                if self.check_unlocated() and config[&#34;check_unlocated&#34;] == True:
                    msg_1 = f&#34;Unlocated item. Please avoid setting the bbox field when geometry is set to null&#34;
                    best_practices_dict[&#34;check_unlocated&#34;] = [msg_1]

                # best practices - recommend items have a geometry
                if self.check_geometry_null() and config[&#34;check_geometry&#34;] == True:
                    msg_1 = f&#34;All items should have a geometry field. STAC is not meant for non-spatial data&#34;
                    best_practices_dict[&#34;null_geometry&#34;] = [msg_1]

                # check to see if there are too many links
                if self.check_bloated_links(max_links=max_links) and config[&#34;bloated_links&#34;] == True:
                    msg_1 = f&#34;You have {len(self.data[&#39;links&#39;])} links. Please consider using sub-collections or sub-catalogs&#34;
                    best_practices_dict[&#34;bloated_links&#34;] = [msg_1]

                # best practices - check for bloated metadata in properties
                if self.check_bloated_metadata(max_properties=max_properties) and config[&#34;bloated_metadata&#34;] == True:
                    msg_1 = f&#34;You have {len(self.data[&#39;properties&#39;])} properties. Please consider using links to avoid bloated metadata&#34;
                    best_practices_dict[&#34;bloated_metadata&#34;] = [msg_1]

                # best practices - ensure thumbnail is a small file size [&#34;png&#34;, &#34;jpeg&#34;, &#34;jpg&#34;, &#34;webp&#34;]
                if not self.check_thumbnail() and self.asset_type == &#34;ITEM&#34; and config[&#34;check_thumbnail&#34;] == True:
                    msg_1 = f&#34;A thumbnail should have a small file size ie. png, jpeg, jpg, webp&#34;
                    best_practices_dict[&#34;check_thumbnail&#34;] = [msg_1]

                # best practices - ensure that links in catalogs and collections include a title field
                if not self.check_links_title_field() and config[&#34;links_title&#34;] == True:
                    msg_1 = f&#34;Links in catalogs and collections should always have a &#39;title&#39; field&#34;
                    best_practices_dict[&#34;check_links_title&#34;] = [msg_1]

                # best practices - ensure that links in catalogs and collections include self link
                if not self.check_links_self() and config[&#34;links_self&#34;] == True:
                    msg_1 = f&#34;A link to &#39;self&#39; in links is strongly recommended&#34;
                    best_practices_dict[&#34;check_links_self&#34;] = [msg_1]

                return best_practices_dict

            def create_best_practices_msg(self) -&gt; List[str]:
                &#34;&#34;&#34;
                Generates a list of best practices messages based on the results of the &#39;create_best_practices_dict&#39; method.

                Returns:
                    A list of strings, where each string contains a best practice message. Each message starts with the 
                    &#39;STAC Best Practices:&#39; base string and is followed by a specific recommendation. Each message is indented 
                    with four spaces, and there is an empty string between each message for readability.
                &#34;&#34;&#34;
                best_practices = list()
                base_string = &#34;STAC Best Practices: &#34;
                best_practices.append(base_string)

                for _,v in self.create_best_practices_dict().items():
                    for value in v:
                        best_practices.extend([&#34;    &#34; +value])  
                    best_practices.extend([&#34;&#34;])

                return best_practices</code></pre>
        </details>
        <h3>Class variables</h3>
        <dl>
        <dt id="stac_check.lint.Linter.assets"><code class="name">var <span class="ident">assets</span> : bool</code></dt>
        <dd>
        <div class="desc"></div>
        </dd>
        <dt id="stac_check.lint.Linter.config_file"><code class="name">var <span class="ident">config_file</span> : Optional[str]</code></dt>
        <dd>
        <div class="desc"></div>
        </dd>
        <dt id="stac_check.lint.Linter.item"><code class="name">var <span class="ident">item</span> : Union[str, dict]</code></dt>
        <dd>
        <div class="desc"></div>
        </dd>
        <dt id="stac_check.lint.Linter.links"><code class="name">var <span class="ident">links</span> : bool</code></dt>
        <dd>
        <div class="desc"></div>
        </dd>
        <dt id="stac_check.lint.Linter.max_depth"><code class="name">var <span class="ident">max_depth</span> : Optional[int]</code></dt>
        <dd>
        <div class="desc"></div>
        </dd>
        <dt id="stac_check.lint.Linter.recursive"><code class="name">var <span class="ident">recursive</span> : bool</code></dt>
        <dd>
        <div class="desc"></div>
        </dd>
        </dl>
        <h3>Static methods</h3>
        <dl>
        <dt id="stac_check.lint.Linter.parse_config"><code class="name flex">
        <span>def <span class="ident">parse_config</span></span>(<span>config_file: Optional[str] = None) ‑> Dict</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Parse the configuration file for STAC checks.</p>
        <p>The method first looks for a file path specified in the <code>STAC_CHECK_CONFIG</code>
        environment variable. If the variable is defined, the method loads the
        YAML configuration file located at that path. Otherwise, it loads the default
        configuration file packaged with the <code>stac-check</code> module.</p>
        <p>If <code>config_file</code> is specified, the method also loads the YAML configuration
        file located at that path and merges its contents with the default or
        environment-based configuration.</p>
        <h2 id="args">Args</h2>
        <dl>
        <dt><strong><code>config_file</code></strong> :&ensp;<code>str</code></dt>
        <dd>The path to the YAML configuration file.</dd>
        </dl>
        <h2 id="returns">Returns</h2>
        <p>A dictionary containing the parsed configuration values.</p>
        <h2 id="raises">Raises</h2>
        <dl>
        <dt><code>IOError</code></dt>
        <dd>If <code>config_file</code> is specified but cannot be read.</dd>
        <dt><code>yaml.YAMLError</code></dt>
        <dd>If any YAML syntax errors occur while parsing the
        configuration file(s).</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">@staticmethod
        def parse_config(config_file: Optional[str] = None) -&gt; Dict:
            &#34;&#34;&#34;Parse the configuration file for STAC checks.

            The method first looks for a file path specified in the `STAC_CHECK_CONFIG`
            environment variable. If the variable is defined, the method loads the
            YAML configuration file located at that path. Otherwise, it loads the default
            configuration file packaged with the `stac-check` module.

            If `config_file` is specified, the method also loads the YAML configuration
            file located at that path and merges its contents with the default or
            environment-based configuration.

            Args:
                config_file (str): The path to the YAML configuration file.

            Returns:
                A dictionary containing the parsed configuration values.

            Raises:
                IOError: If `config_file` is specified but cannot be read.
                yaml.YAMLError: If any YAML syntax errors occur while parsing the
                    configuration file(s).
            &#34;&#34;&#34;
            default_config_file = os.getenv(&#34;STAC_CHECK_CONFIG&#34;)
            if default_config_file:
                with open(default_config_file) as f:
                    default_config = yaml.load(f, Loader=yaml.FullLoader)
            else:
                with importlib.resources.open_text(__name__, &#34;stac-check.config.yml&#34;) as f:
                    default_config = yaml.load(f, Loader=yaml.FullLoader)
            if config_file:
                with open(config_file) as f:
                    config = yaml.load(f, Loader=yaml.FullLoader)
                default_config.update(config)
                
            return default_config</code></pre>
        </details>
        </dd>
        </dl>
        <h3>Methods</h3>
        <dl>
        <dt id="stac_check.lint.Linter.check_bloated_links"><code class="name flex">
        <span>def <span class="ident">check_bloated_links</span></span>(<span>self, max_links: Optional[int] = 20) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks if the number of links in the STAC data exceeds a certain maximum.</p>
        <h2 id="args">Args</h2>
        <dl>
        <dt><strong><code>max_links</code></strong> :&ensp;<code>Optional[int]</code></dt>
        <dd>The maximum number of links that the STAC data is allowed to have. Default is 20.</dd>
        </dl>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>A boolean indicating if the number of links in the STAC data exceeds the specified maximum.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_bloated_links(self, max_links: Optional[int] = 20) -&gt; bool:
            &#34;&#34;&#34;Checks if the number of links in the STAC data exceeds a certain maximum.

            Args:
                max_links (Optional[int]): The maximum number of links that the STAC data is allowed to have. Default is 20.

            Returns:
                bool: A boolean indicating if the number of links in the STAC data exceeds the specified maximum.
            &#34;&#34;&#34;
            if &#34;links&#34; in self.data:
                return len(self.data[&#34;links&#34;]) &gt; max_links</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_bloated_metadata"><code class="name flex">
        <span>def <span class="ident">check_bloated_metadata</span></span>(<span>self, max_properties: Optional[int] = 20) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks whether a STAC item's metadata contains too many properties.</p>
        <h2 id="args">Args</h2>
        <dl>
        <dt><strong><code>max_properties</code></strong> :&ensp;<code>int</code>, optional</dt>
        <dd>The maximum number of properties that the metadata can contain before it is
        considered too bloated. Defaults to 20.</dd>
        </dl>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>True if the number of properties in the metadata exceeds the maximum number of properties specified by
        <code>max_properties</code>, False otherwise.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_bloated_metadata(self, max_properties: Optional[int] = 20) -&gt; bool:
            &#34;&#34;&#34;Checks whether a STAC item&#39;s metadata contains too many properties.

            Args:
                max_properties (int, optional): The maximum number of properties that the metadata can contain before it is
                    considered too bloated. Defaults to 20.

            Returns:
                bool: True if the number of properties in the metadata exceeds the maximum number of properties specified by
                    `max_properties`, False otherwise.
            &#34;&#34;&#34;
            if &#34;properties&#34; in self.data:
                return len(self.data[&#34;properties&#34;].keys()) &gt; max_properties
            return False</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_catalog_file_name"><code class="name flex">
        <span>def <span class="ident">check_catalog_file_name</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks whether the filename of a Catalog or Collection conforms to the STAC specification.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>True if the filename is valid, False otherwise.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_catalog_file_name(self) -&gt; bool:
            &#34;&#34;&#34;Checks whether the filename of a Catalog or Collection conforms to the STAC specification.
            
            Returns:
                bool: True if the filename is valid, False otherwise.
            &#34;&#34;&#34;
            if isinstance(self.item, str) and &#34;.json&#34; in self.item:
                if self.asset_type == &#34;CATALOG&#34; and &#39;catalog.json&#39; not in self.item:
                    return False 
                elif self.asset_type == &#34;COLLECTION&#34; and &#39;collection.json&#39; not in self.item:
                    return False
                return True
            else:
                return True</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_datetime_null"><code class="name flex">
        <span>def <span class="ident">check_datetime_null</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks if the STAC item has a null datetime property.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>A boolean indicating whether the datetime property is null (True) or not (False).</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_datetime_null(self) -&gt; bool:
            &#34;&#34;&#34;Checks if the STAC item has a null datetime property.

            Returns:
                bool: A boolean indicating whether the datetime property is null (True) or not (False).
            &#34;&#34;&#34;
            if &#34;properties&#34; in self.data:
                if &#34;datetime&#34; in self.data[&#34;properties&#34;]:
                    if self.data[&#34;properties&#34;][&#34;datetime&#34;] == None:
                        return True
            else:
                return False
            return False</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_error_message"><code class="name flex">
        <span>def <span class="ident">check_error_message</span></span>(<span>self) ‑> str</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks whether the <code>message</code> attribute contains an <code>error_message</code> field.</p>
        <h2 id="returns">Returns</h2>
        <p>A string containing the value of the <code>error_message</code> field, or an empty string if the field is not present.</p></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_error_message(self) -&gt; str:
            &#34;&#34;&#34;Checks whether the `message` attribute contains an `error_message` field.

            Returns:
                A string containing the value of the `error_message` field, or an empty string if the field is not present.
            &#34;&#34;&#34;
            if &#34;error_message&#34; in self.message:
                return self.message[&#34;error_message&#34;]
            else:
                return &#34;&#34;</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_error_type"><code class="name flex">
        <span>def <span class="ident">check_error_type</span></span>(<span>self) ‑> str</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Returns the error type of a STAC validation if it exists in the validation message,
        and an empty string otherwise.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>str</code></dt>
        <dd>A string containing the error type of a STAC validation if it exists in the validation message, and an</dd>
        </dl>
        <p>empty string otherwise.</p></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_error_type(self) -&gt; str:
            &#34;&#34;&#34;Returns the error type of a STAC validation if it exists in the validation message, 
            and an empty string otherwise.

            Returns:
                str: A string containing the error type of a STAC validation if it exists in the validation message, and an
                empty string otherwise.
            &#34;&#34;&#34;
            if &#34;error_type&#34; in self.message:
                return self.message[&#34;error_type&#34;]
            else:
                return &#34;&#34;</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_geometry_null"><code class="name flex">
        <span>def <span class="ident">check_geometry_null</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks if a STAC item has a null geometry property.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>A boolean indicating whether the geometry property is null (True) or not (False).</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_geometry_null(self) -&gt; bool:
            &#34;&#34;&#34;Checks if a STAC item has a null geometry property.
                
            Returns:
                bool: A boolean indicating whether the geometry property is null (True) or not (False).          
            &#34;&#34;&#34;
            if &#34;geometry&#34; in self.data:
                return self.data[&#34;geometry&#34;] is None</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_item_id_file_name"><code class="name flex">
        <span>def <span class="ident">check_item_id_file_name</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_item_id_file_name(self) -&gt; bool:
            if self.asset_type == &#34;ITEM&#34; and self.object_id != self.file_name:
                return False
            else:
                return True</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_links_assets"><code class="name flex">
        <span>def <span class="ident">check_links_assets</span></span>(<span>self, num_links: int, url_type: str, format_type: str) ‑> List[str]</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks the links and assets in the STAC catalog and returns a list of invalid links of a specified type and format.</p>
        <h2 id="args">Args</h2>
        <dl>
        <dt><strong><code>num_links</code></strong> :&ensp;<code>int</code></dt>
        <dd>The maximum number of invalid links to return.</dd>
        <dt><strong><code>url_type</code></strong> :&ensp;<code>str</code></dt>
        <dd>The type of URL to check, which can be either 'self' or 'external'.</dd>
        <dt><strong><code>format_type</code></strong> :&ensp;<code>str</code></dt>
        <dd>The format of the URL to check, which can be either 'html' or 'json'.</dd>
        </dl>
        <h2 id="returns">Returns</h2>
        <p>A list of invalid links of the specified type and format. If there are no invalid links, an empty list is returned.</p></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_links_assets(self, num_links: int, url_type: str, format_type: str) -&gt; List[str]:
            &#34;&#34;&#34;Checks the links and assets in the STAC catalog and returns a list of invalid links of a specified type and format.

            Args:
                num_links (int): The maximum number of invalid links to return.
                url_type (str): The type of URL to check, which can be either &#39;self&#39; or &#39;external&#39;.
                format_type (str): The format of the URL to check, which can be either &#39;html&#39; or &#39;json&#39;.

            Returns:
                A list of invalid links of the specified type and format. If there are no invalid links, an empty list is returned.
            &#34;&#34;&#34;
            links = []
            if f&#34;{url_type}_validated&#34; in self.message:
                for invalid_request_url in self.message[f&#34;{url_type}_validated&#34;][f&#34;{format_type}_invalid&#34;]:
                    if invalid_request_url not in links and &#39;http&#39; in invalid_request_url:
                        links.append(invalid_request_url)
                    num_links = num_links - 1
                    if num_links == 0:
                        return links
            return links</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_links_self"><code class="name flex">
        <span>def <span class="ident">check_links_self</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks whether the "self" link is present in the STAC collection or catalog or absent in STAC item.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>True if the "self" link is present in STAC collection or catalog or absent in STAC item, False otherwise.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_links_self(self) -&gt; bool:
            &#34;&#34;&#34;Checks whether the &#34;self&#34; link is present in the STAC collection or catalog or absent in STAC item.
            
            Returns:
                bool: True if the &#34;self&#34; link is present in STAC collection or catalog or absent in STAC item, False otherwise.
            &#34;&#34;&#34;
            if self.asset_type == &#34;ITEM&#34;:
                return True
            if self.asset_type == &#34;COLLECTION&#34; or self.asset_type == &#34;CATALOG&#34;:
                for link in self.data[&#34;links&#34;]:
                    if &#34;self&#34; in link[&#34;rel&#34;]:
                        return True
            return False</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_links_title_field"><code class="name flex">
        <span>def <span class="ident">check_links_title_field</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks if all links in a STAC collection or catalog have a 'title' field.
        The 'title' field is not required for the 'self' link.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>True if all links have a 'title' field, False otherwise.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_links_title_field(self) -&gt; bool:
            &#34;&#34;&#34;Checks if all links in a STAC collection or catalog have a &#39;title&#39; field.
            The &#39;title&#39; field is not required for the &#39;self&#39; link.

            Returns:
                bool: True if all links have a &#39;title&#39; field, False otherwise.
            &#34;&#34;&#34;
            if self.asset_type == &#34;COLLECTION&#34; or self.asset_type == &#34;CATALOG&#34;:
                for link in self.data[&#34;links&#34;]:
                    if &#34;title&#34; not in link and link[&#34;rel&#34;] != &#34;self&#34;:
                        return False
            return True</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_percent_encoded"><code class="name flex">
        <span>def <span class="ident">check_percent_encoded</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks if the identifiers of a STAC item are percent-encoded, i.e.,
        they only contain lowercase letters, numbers, hyphens, and underscores.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>True if the identifiers are percent-encoded, False otherwise.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_percent_encoded(self) -&gt; bool:
            &#34;&#34;&#34;Checks if the identifiers of a STAC item are percent-encoded, i.e.,
            they only contain lowercase letters, numbers, hyphens, and underscores.

            Returns:
                bool: True if the identifiers are percent-encoded, False otherwise.
            &#34;&#34;&#34;
            return self.asset_type == &#34;ITEM&#34; and &#34;/&#34; in self.object_id or &#34;:&#34; in self.object_id</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_searchable_identifiers"><code class="name flex">
        <span>def <span class="ident">check_searchable_identifiers</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks if the identifiers of a STAC item are searchable, i.e.,
        they only contain lowercase letters, numbers, hyphens, and underscores.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>True if the identifiers are searchable, False otherwise.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_searchable_identifiers(self) -&gt; bool:
            &#34;&#34;&#34;Checks if the identifiers of a STAC item are searchable, i.e., 
            they only contain lowercase letters, numbers, hyphens, and underscores.
            
            Returns:
                bool: True if the identifiers are searchable, False otherwise.        
            &#34;&#34;&#34;
            if self.asset_type == &#34;ITEM&#34;: 
                for letter in self.object_id:
                    if letter.islower() or letter.isnumeric() or letter == &#39;-&#39; or letter == &#39;_&#39;:
                        pass
                    else:
                        return False  
            return True</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_summaries"><code class="name flex">
        <span>def <span class="ident">check_summaries</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Check if a Collection asset has a "summaries" property.</p>
        <h2 id="returns">Returns</h2>
        <p>A boolean indicating whether the Collection asset has a "summaries" property.</p></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_summaries(self) -&gt; bool:
            &#34;&#34;&#34;Check if a Collection asset has a &#34;summaries&#34; property.

            Returns:
                A boolean indicating whether the Collection asset has a &#34;summaries&#34; property.
            &#34;&#34;&#34;
            if self.asset_type == &#34;COLLECTION&#34;:
                return &#34;summaries&#34; in self.data</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_thumbnail"><code class="name flex">
        <span>def <span class="ident">check_thumbnail</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks if the thumbnail of a STAC item is valid, i.e., it has a valid format.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>True if the thumbnail is valid, False otherwise.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_thumbnail(self) -&gt; bool:
            &#34;&#34;&#34;Checks if the thumbnail of a STAC item is valid, i.e., it has a valid format.
            
            Returns:
                bool: True if the thumbnail is valid, False otherwise.
            &#34;&#34;&#34;
            if &#34;assets&#34; in self.data:
                if &#34;thumbnail&#34; in self.data[&#34;assets&#34;]:
                    if &#34;type&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;]:
                        if &#34;png&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;] or &#34;jpeg&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;] or \
                            &#34;jpg&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;] or &#34;webp&#34; in self.data[&#34;assets&#34;][&#34;thumbnail&#34;][&#34;type&#34;]:
                            return True
                        else:
                            return False
            return True</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.check_unlocated"><code class="name flex">
        <span>def <span class="ident">check_unlocated</span></span>(<span>self) ‑> bool</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Checks if a STAC item is unlocated, i.e., has no geometry but has a bounding box.</p>
        <h2 id="returns">Returns</h2>
        <dl>
        <dt><code>bool</code></dt>
        <dd>True if the STAC item is unlocated, False otherwise.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def check_unlocated(self) -&gt; bool:
            &#34;&#34;&#34;Checks if a STAC item is unlocated, i.e., has no geometry but has a bounding box.

            Returns:
                bool: True if the STAC item is unlocated, False otherwise.
            &#34;&#34;&#34;
            if &#34;geometry&#34; in self.data:
                return self.data[&#34;geometry&#34;] is None and self.data[&#34;bbox&#34;] is not None</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.create_best_practices_dict"><code class="name flex">
        <span>def <span class="ident">create_best_practices_dict</span></span>(<span>self) ‑> Dict</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Creates a dictionary of best practices violations for the current STAC object. The violations are determined
        by a set of configurable linting rules specified in the config file.</p>
        <h2 id="returns">Returns</h2>
        <p>A dictionary of best practices violations for the current STAC object. The keys in the dictionary correspond
        to the linting rules that were violated, and the values are lists of strings containing error messages and
        recommendations for how to fix the violations.</p></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def create_best_practices_dict(self) -&gt; Dict:
            &#34;&#34;&#34;Creates a dictionary of best practices violations for the current STAC object. The violations are determined
            by a set of configurable linting rules specified in the config file.

            Returns:
                A dictionary of best practices violations for the current STAC object. The keys in the dictionary correspond
                to the linting rules that were violated, and the values are lists of strings containing error messages and
                recommendations for how to fix the violations.
            &#34;&#34;&#34;
            best_practices_dict = {}
            config = self.config[&#34;linting&#34;]
            max_links = self.config[&#34;settings&#34;][&#34;max_links&#34;]
            max_properties = self.config[&#34;settings&#34;][&#34;max_properties&#34;]

            # best practices - item ids should only contain searchable identifiers
            if self.check_searchable_identifiers() == False and config[&#34;searchable_identifiers&#34;] == True: 
                msg_1 = f&#34;Item name &#39;{self.object_id}&#39; should only contain Searchable identifiers&#34;
                msg_2 = f&#34;Identifiers should consist of only lowercase characters, numbers, &#39;_&#39;, and &#39;-&#39;&#34;
                best_practices_dict[&#34;searchable_identifiers&#34;] = [msg_1, msg_2]

            # best practices - item ids should not contain &#39;:&#39; or &#39;/&#39; characters
            if self.check_percent_encoded() and config[&#34;percent_encoded&#34;] == True:
                msg_1 = f&#34;Item name &#39;{self.object_id}&#39; should not contain &#39;:&#39; or &#39;/&#39;&#34;
                msg_2 = f&#34;https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#item-ids&#34;
                best_practices_dict[&#34;percent_encoded&#34;] = [msg_1, msg_2]

            # best practices - item ids should match file names
            if not self.check_item_id_file_name() and config[&#34;item_id_file_name&#34;] == True:
                msg_1 = f&#34;Item file names should match their ids: &#39;{self.file_name}&#39; not equal to &#39;{self.object_id}&#34;
                best_practices_dict[&#34;check_item_id&#34;] = [msg_1]

            # best practices - collection and catalog file names should be collection.json and catalog.json 
            if self.check_catalog_file_name() == False and config[&#34;catalog_id_file_name&#34;] == True: 
                msg_1 = f&#34;Object should be called &#39;{self.asset_type.lower()}.json&#39; not &#39;{self.file_name}.json&#39;&#34;
                best_practices_dict[&#34;check_catalog_id&#34;] = [msg_1]

            # best practices - collections should contain summaries
            if self.check_summaries() == False and config[&#34;check_summaries&#34;] == True:
                msg_1 = f&#34;A STAC collection should contain a summaries field&#34;
                msg_2 = f&#34;It is recommended to store information like eo:bands in summaries&#34;
                best_practices_dict[&#34;check_summaries&#34;] = [msg_1, msg_2]

            # best practices - datetime fields should not be set to null
            if self.check_datetime_null() and config[&#34;null_datetime&#34;] == True:
                msg_1 = f&#34;Please avoid setting the datetime field to null, many clients search on this field&#34;
                best_practices_dict[&#34;datetime_null&#34;] = [msg_1]

            # best practices - check unlocated items to make sure bbox field is not set
            if self.check_unlocated() and config[&#34;check_unlocated&#34;] == True:
                msg_1 = f&#34;Unlocated item. Please avoid setting the bbox field when geometry is set to null&#34;
                best_practices_dict[&#34;check_unlocated&#34;] = [msg_1]

            # best practices - recommend items have a geometry
            if self.check_geometry_null() and config[&#34;check_geometry&#34;] == True:
                msg_1 = f&#34;All items should have a geometry field. STAC is not meant for non-spatial data&#34;
                best_practices_dict[&#34;null_geometry&#34;] = [msg_1]

            # check to see if there are too many links
            if self.check_bloated_links(max_links=max_links) and config[&#34;bloated_links&#34;] == True:
                msg_1 = f&#34;You have {len(self.data[&#39;links&#39;])} links. Please consider using sub-collections or sub-catalogs&#34;
                best_practices_dict[&#34;bloated_links&#34;] = [msg_1]

            # best practices - check for bloated metadata in properties
            if self.check_bloated_metadata(max_properties=max_properties) and config[&#34;bloated_metadata&#34;] == True:
                msg_1 = f&#34;You have {len(self.data[&#39;properties&#39;])} properties. Please consider using links to avoid bloated metadata&#34;
                best_practices_dict[&#34;bloated_metadata&#34;] = [msg_1]

            # best practices - ensure thumbnail is a small file size [&#34;png&#34;, &#34;jpeg&#34;, &#34;jpg&#34;, &#34;webp&#34;]
            if not self.check_thumbnail() and self.asset_type == &#34;ITEM&#34; and config[&#34;check_thumbnail&#34;] == True:
                msg_1 = f&#34;A thumbnail should have a small file size ie. png, jpeg, jpg, webp&#34;
                best_practices_dict[&#34;check_thumbnail&#34;] = [msg_1]

            # best practices - ensure that links in catalogs and collections include a title field
            if not self.check_links_title_field() and config[&#34;links_title&#34;] == True:
                msg_1 = f&#34;Links in catalogs and collections should always have a &#39;title&#39; field&#34;
                best_practices_dict[&#34;check_links_title&#34;] = [msg_1]

            # best practices - ensure that links in catalogs and collections include self link
            if not self.check_links_self() and config[&#34;links_self&#34;] == True:
                msg_1 = f&#34;A link to &#39;self&#39; in links is strongly recommended&#34;
                best_practices_dict[&#34;check_links_self&#34;] = [msg_1]

            return best_practices_dict</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.create_best_practices_msg"><code class="name flex">
        <span>def <span class="ident">create_best_practices_msg</span></span>(<span>self) ‑> List[str]</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Generates a list of best practices messages based on the results of the 'create_best_practices_dict' method.</p>
        <h2 id="returns">Returns</h2>
        <p>A list of strings, where each string contains a best practice message. Each message starts with the
        'STAC Best Practices:' base string and is followed by a specific recommendation. Each message is indented
        with four spaces, and there is an empty string between each message for readability.</p></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def create_best_practices_msg(self) -&gt; List[str]:
            &#34;&#34;&#34;
            Generates a list of best practices messages based on the results of the &#39;create_best_practices_dict&#39; method.

            Returns:
                A list of strings, where each string contains a best practice message. Each message starts with the 
                &#39;STAC Best Practices:&#39; base string and is followed by a specific recommendation. Each message is indented 
                with four spaces, and there is an empty string between each message for readability.
            &#34;&#34;&#34;
            best_practices = list()
            base_string = &#34;STAC Best Practices: &#34;
            best_practices.append(base_string)

            for _,v in self.create_best_practices_dict().items():
                for value in v:
                    best_practices.extend([&#34;    &#34; +value])  
                best_practices.extend([&#34;&#34;])

            return best_practices</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.get_asset_name"><code class="name flex">
        <span>def <span class="ident">get_asset_name</span></span>(<span>self, file: Union[str, Dict] = None) ‑> str</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Extracts the name of an asset from its file path or from a STAC item asset dictionary.</p>
        <h2 id="args">Args</h2>
        <dl>
        <dt><strong><code>file</code></strong> :&ensp;<code>Union[str, dict]</code>, optional</dt>
        <dd>A string representing the file path to the asset or a dictionary representing the
        asset as specified in a STAC item's <code>assets</code> property.</dd>
        </dl>
        <h2 id="returns">Returns</h2>
        <p>A string containing the name of the asset.</p>
        <h2 id="raises">Raises</h2>
        <dl>
        <dt><code>TypeError</code></dt>
        <dd>If the input <code>file</code> is not a string or a dictionary.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def get_asset_name(self, file: Union[str, Dict] = None) -&gt; str:
            &#34;&#34;&#34;Extracts the name of an asset from its file path or from a STAC item asset dictionary.

            Args:
                file (Union[str, dict], optional): A string representing the file path to the asset or a dictionary representing the
                    asset as specified in a STAC item&#39;s `assets` property.

            Returns:
                A string containing the name of the asset.

            Raises:
                TypeError: If the input `file` is not a string or a dictionary.
            &#34;&#34;&#34;
            if isinstance(file, str):
                return os.path.basename(file).split(&#39;.&#39;)[0]
            else:
                return file[&#34;id&#34;]</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.load_data"><code class="name flex">
        <span>def <span class="ident">load_data</span></span>(<span>self, file: Union[str, Dict]) ‑> Dict</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Loads JSON data from a file or URL.</p>
        <h2 id="args">Args</h2>
        <dl>
        <dt><strong><code>file</code></strong> :&ensp;<code>Union[str, Dict]</code></dt>
        <dd>A string representing the path to a JSON file or a dictionary containing the JSON data.</dd>
        </dl>
        <h2 id="returns">Returns</h2>
        <p>A dictionary containing the loaded JSON data.</p>
        <h2 id="raises">Raises</h2>
        <dl>
        <dt><code>TypeError</code></dt>
        <dd>If the input <code>file</code> is not a string or dictionary.</dd>
        <dt><code>ValueError</code></dt>
        <dd>If <code>file</code> is a string that doesn't represent a valid URL or file path.</dd>
        <dt><code>requests.exceptions.RequestException</code></dt>
        <dd>If there is an error making a request to a URL.</dd>
        <dt><code>JSONDecodeError</code></dt>
        <dd>If the JSON data cannot be decoded.</dd>
        <dt><code>FileNotFoundError</code></dt>
        <dd>If the specified file cannot be found.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def load_data(self, file: Union[str, Dict]) -&gt; Dict:
            &#34;&#34;&#34;Loads JSON data from a file or URL.

            Args:
                file (Union[str, Dict]): A string representing the path to a JSON file or a dictionary containing the JSON data.

            Returns:
                A dictionary containing the loaded JSON data.

            Raises:
                TypeError: If the input `file` is not a string or dictionary.
                ValueError: If `file` is a string that doesn&#39;t represent a valid URL or file path.
                requests.exceptions.RequestException: If there is an error making a request to a URL.
                JSONDecodeError: If the JSON data cannot be decoded.
                FileNotFoundError: If the specified file cannot be found.
            &#34;&#34;&#34;

            if isinstance(file, str):
                if is_valid_url(file):
                    resp = requests.get(file)
                    data = resp.json()
                else:
                    with open(file) as json_file:
                        data = json.load(json_file)
                return data
            else:
                return file</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.recursive_validation"><code class="name flex">
        <span>def <span class="ident">recursive_validation</span></span>(<span>self, file: Union[str, Dict[str, Any]]) ‑> str</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Recursively validate a STAC item or catalog file and its child items.</p>
        <h2 id="args">Args</h2>
        <dl>
        <dt><strong><code>file</code></strong> :&ensp;<code>Union[str, Dict[str, Any]]</code></dt>
        <dd>A string representing the file path to the STAC item or catalog, or a
        dictionary representing the STAC item or catalog.</dd>
        </dl>
        <h2 id="returns">Returns</h2>
        <p>A string containing the validation message.</p>
        <h2 id="raises">Raises</h2>
        <dl>
        <dt><code>TypeError</code></dt>
        <dd>If the input <code>file</code> is not a string or a dictionary.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def recursive_validation(self, file: Union[str, Dict[str, Any]]) -&gt; str:
            &#34;&#34;&#34;Recursively validate a STAC item or catalog file and its child items.

            Args:
                file (Union[str, Dict[str, Any]]): A string representing the file path to the STAC item or catalog, or a
                    dictionary representing the STAC item or catalog.

            Returns:
                A string containing the validation message.

            Raises:
                TypeError: If the input `file` is not a string or a dictionary.
            &#34;&#34;&#34;
            if self.recursive:
                if isinstance(file, str):
                    stac = StacValidate(file, recursive=True, max_depth=self.max_depth)
                    stac.run()
                else:
                    stac = StacValidate(recursive=True, max_depth=self.max_depth)
                    stac.validate_dict(file)
                return stac.message</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.set_update_message"><code class="name flex">
        <span>def <span class="ident">set_update_message</span></span>(<span>self) ‑> str</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Returns a message for users to update their STAC version.</p>
        <h2 id="returns">Returns</h2>
        <p>A string containing a message for users to update their STAC version.</p></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def set_update_message(self) -&gt; str:
            &#34;&#34;&#34;Returns a message for users to update their STAC version.

            Returns:
                A string containing a message for users to update their STAC version.
            &#34;&#34;&#34;
            if self.version != &#34;1.0.0&#34;:
                return f&#34;Please upgrade from version {self.version} to version 1.0.0!&#34;
            else:
                return &#34;Thanks for using STAC version 1.0.0!&#34;</code></pre>
        </details>
        </dd>
        <dt id="stac_check.lint.Linter.validate_file"><code class="name flex">
        <span>def <span class="ident">validate_file</span></span>(<span>self, file: Union[str, dict]) ‑> Dict[str, Any]</span>
        </code></dt>
        <dd>
        <div class="desc"><p>Validates the given file path or STAC dictionary against the validation schema.</p>
        <h2 id="args">Args</h2>
        <dl>
        <dt><strong><code>file</code></strong> :&ensp;<code>Union[str, dict]</code></dt>
        <dd>A string representing the file path to the STAC file or a dictionary representing the STAC
        item.</dd>
        </dl>
        <h2 id="returns">Returns</h2>
        <p>A dictionary containing the results of the validation, including the status of the validation and any errors
        encountered.</p>
        <h2 id="raises">Raises</h2>
        <dl>
        <dt><code>ValueError</code></dt>
        <dd>If <code>file</code> is not a valid file path or STAC dictionary.</dd>
        </dl></div>
        <details class="source">
        <summary>
        <span>Expand source code</span>
        </summary>
        <pre><code class="python">def validate_file(self, file: Union[str, dict]) -&gt; Dict[str, Any]:
            &#34;&#34;&#34;Validates the given file path or STAC dictionary against the validation schema.

            Args:
                file (Union[str, dict]): A string representing the file path to the STAC file or a dictionary representing the STAC
                    item.

            Returns:
                A dictionary containing the results of the validation, including the status of the validation and any errors
                encountered.

            Raises:
                ValueError: If `file` is not a valid file path or STAC dictionary.
            &#34;&#34;&#34;
            if isinstance(file, str):
                stac = StacValidate(file, links=self.links, assets=self.assets)
                stac.run()
            elif isinstance(file, dict):
                stac = StacValidate()
                stac.validate_dict(file)
            else:
                raise ValueError(&#34;Input must be a file path or STAC dictionary.&#34;)
            return stac.message[0]</code></pre>
        </details>
        </dd>
        </dl>
        </dd>
        </dl>
        </section>
        </article>
        <nav id="sidebar">
        <h1>Index</h1>
        <div class="toc">
        <ul></ul>
        </div>
        <ul id="index">
        <li><h3>Super-module</h3>
        <ul>
        <li><code><a title="stac_check" href="index.html">stac_check</a></code></li>
        </ul>
        </li>
        <li><h3><a href="#header-classes">Classes</a></h3>
        <ul>
        <li>
        <h4><code><a title="stac_check.lint.Linter" href="#stac_check.lint.Linter">Linter</a></code></h4>
        <ul class="">
        <li><code><a title="stac_check.lint.Linter.assets" href="#stac_check.lint.Linter.assets">assets</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_bloated_links" href="#stac_check.lint.Linter.check_bloated_links">check_bloated_links</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_bloated_metadata" href="#stac_check.lint.Linter.check_bloated_metadata">check_bloated_metadata</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_catalog_file_name" href="#stac_check.lint.Linter.check_catalog_file_name">check_catalog_file_name</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_datetime_null" href="#stac_check.lint.Linter.check_datetime_null">check_datetime_null</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_error_message" href="#stac_check.lint.Linter.check_error_message">check_error_message</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_error_type" href="#stac_check.lint.Linter.check_error_type">check_error_type</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_geometry_null" href="#stac_check.lint.Linter.check_geometry_null">check_geometry_null</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_item_id_file_name" href="#stac_check.lint.Linter.check_item_id_file_name">check_item_id_file_name</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_links_assets" href="#stac_check.lint.Linter.check_links_assets">check_links_assets</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_links_self" href="#stac_check.lint.Linter.check_links_self">check_links_self</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_links_title_field" href="#stac_check.lint.Linter.check_links_title_field">check_links_title_field</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_percent_encoded" href="#stac_check.lint.Linter.check_percent_encoded">check_percent_encoded</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_searchable_identifiers" href="#stac_check.lint.Linter.check_searchable_identifiers">check_searchable_identifiers</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_summaries" href="#stac_check.lint.Linter.check_summaries">check_summaries</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_thumbnail" href="#stac_check.lint.Linter.check_thumbnail">check_thumbnail</a></code></li>
        <li><code><a title="stac_check.lint.Linter.check_unlocated" href="#stac_check.lint.Linter.check_unlocated">check_unlocated</a></code></li>
        <li><code><a title="stac_check.lint.Linter.config_file" href="#stac_check.lint.Linter.config_file">config_file</a></code></li>
        <li><code><a title="stac_check.lint.Linter.create_best_practices_dict" href="#stac_check.lint.Linter.create_best_practices_dict">create_best_practices_dict</a></code></li>
        <li><code><a title="stac_check.lint.Linter.create_best_practices_msg" href="#stac_check.lint.Linter.create_best_practices_msg">create_best_practices_msg</a></code></li>
        <li><code><a title="stac_check.lint.Linter.get_asset_name" href="#stac_check.lint.Linter.get_asset_name">get_asset_name</a></code></li>
        <li><code><a title="stac_check.lint.Linter.item" href="#stac_check.lint.Linter.item">item</a></code></li>
        <li><code><a title="stac_check.lint.Linter.links" href="#stac_check.lint.Linter.links">links</a></code></li>
        <li><code><a title="stac_check.lint.Linter.load_data" href="#stac_check.lint.Linter.load_data">load_data</a></code></li>
        <li><code><a title="stac_check.lint.Linter.max_depth" href="#stac_check.lint.Linter.max_depth">max_depth</a></code></li>
        <li><code><a title="stac_check.lint.Linter.parse_config" href="#stac_check.lint.Linter.parse_config">parse_config</a></code></li>
        <li><code><a title="stac_check.lint.Linter.recursive" href="#stac_check.lint.Linter.recursive">recursive</a></code></li>
        <li><code><a title="stac_check.lint.Linter.recursive_validation" href="#stac_check.lint.Linter.recursive_validation">recursive_validation</a></code></li>
        <li><code><a title="stac_check.lint.Linter.set_update_message" href="#stac_check.lint.Linter.set_update_message">set_update_message</a></code></li>
        <li><code><a title="stac_check.lint.Linter.validate_file" href="#stac_check.lint.Linter.validate_file">validate_file</a></code></li>
        </ul>
        </li>
        </ul>
        </li>
        </ul>
        </nav>
        </main>
        <footer id="footer">
        <p>Generated by <a href="https://pdoc3.github.io/pdoc"><cite>pdoc</cite> 0.9.2</a>.</p>
        </footer>
        </body>
    </embed>