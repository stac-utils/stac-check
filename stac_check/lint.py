from .validate import StacValidate
from .utilities import is_valid_url
import json
import os
from dataclasses import dataclass
import pystac
import requests
from urllib.parse import urlparse

@dataclass
class Linter:
    item: str
    assets: bool = False
    links: bool = False
    recursive: bool = False

    def __post_init__(self):
        self.data = self.load_data(self.item)
        self.message = self.validate_file(self.item)
        self.asset_type = self.check_asset_type()
        self.version = self.check_version()
        self.validator_version = "2.4.0"
        self.update_msg = self.set_update_message()
        self.valid_stac = self.message["valid_stac"]
        self.error_type = self.check_error_type()
        self.error_msg = self.check_error_message()
        self.invalid_asset_format = self.check_links_assets(10, "assets", "format") if self.assets else None
        self.invalid_asset_request = self.check_links_assets(10, "assets", "request") if self.assets else None
        self.invalid_link_format = self.check_links_assets(10, "links", "format") if self.links else None
        self.invalid_link_request = self.check_links_assets(10, "links", "request") if self.links else None
        self.schema = self.check_schema()
        self.summaries = self.check_summaries()
        self.bloated_links = self.get_bloated_links()
        self.bloated_metadata = self.get_bloated_metadata()
        self.recursive_error_msg = ""
        self.datetime_null = self.check_datetime()
        self.unlocated = self.check_unlocated()
        self.geometry = self.check_geometry()
        self.validate_all = self.recursive_validation(self.load_data(self.item))
        self.object_id = self.return_id()
        self.file_name = self.get_file_name()
        self.searchable_identifiers = self.check_searchable_identifiers()
        self.percent_encoded = self.check_percent_encoded()
        self.best_practices_msg = self.create_best_practices_msg()

    def load_data(self, file):
        if is_valid_url(file):
            resp = requests.get(file)
            data = resp.json()
        else:
            with open(file) as json_file:
                data = json.load(json_file)
        return data

    def validate_file(self, file):
        stac = StacValidate(file, links=self.links, assets=self.assets)
        stac.run()
        return stac.message[0]

    def recursive_validation(self, file):
        if self.recursive:
            try:
                catalog = pystac.read_dict(file)
                catalog.validate_all()
                return True
            except Exception as e:
                self.recursive_error_msg = f"Exception {str(e)}"
                return False

    def check_asset_type(self):
        if "asset_type" in self.message:
            return self.message["asset_type"]
        else:
            return ""

    def check_schema(self):
        if "schema" in self.message:
            return self.message["schema"]
        else:
            return []

    def check_version(self):
        if "version" in self.message:
            return self.message["version"]
        else:
            return ""

    def set_update_message(self):
        if self.version != "1.0.0":
            return f"Please upgrade from version {self.version} to version 1.0.0!"
        else:
            return "Thanks for using STAC version 1.0.0!"

    def check_links_assets(self, num_links:int, url_type:str, format_type:str):
        links = []
        if f"{url_type}_validated" in self.message:
            for invalid_request_url in self.message[f"{url_type}_validated"][f"{format_type}_invalid"]:
                if invalid_request_url not in links and 'http' in invalid_request_url:
                    links.append(invalid_request_url)
                num_links = num_links - 1
                if num_links == 0:
                    return links
        return links

    def check_error_type(self):
        if "error_type" in self.message:
            return self.message["error_type"]
        else:
            return ""

    def check_error_message(self):
        if "error_message" in self.message:
            return self.message["error_message"]
        else:
            return ""

    def check_summaries(self):
        return "summaries" in self.data

    def get_bloated_links(self):
        if "links" in self.data:
            return len(self.data["links"]) > 20

    def get_bloated_metadata(self):
        if "properties" in self.data:
            return len(self.data["properties"].keys()) > 20

    def return_id(self):
        if "id" in self.data:
            return self.data["id"]
        else:
            return ""

    def check_datetime(self):
        if "properties" in self.data:
            if "datetime" in self.data["properties"]:
                if self.data["properties"]["datetime"] == None:
                    return True
        else:
            return False

    def check_unlocated(self):
        if "geometry" in self.data:
            return self.data["geometry"] is None and self.data["bbox"] is not None

    def check_geometry(self):
        if "geometry" in self.data:
            return self.data["geometry"] is not None

    def get_file_name(self):
        return os.path.basename(self.item).split('.')[0]

    def check_searchable_identifiers(self):
        if self.asset_type == "ITEM": 
            for letter in self.object_id:
                if letter.islower() or letter.isnumeric() or letter == '-' or letter == '_':
                    pass
                else:
                    return False  
        return True

    def check_percent_encoded(self):
        return self.asset_type == "ITEM" and "/" in self.object_id or ":" in self.object_id

    def create_best_practices_msg(self):
        best_practices = list()
        base_string = "STAC Best Practices: "
        best_practices.append(base_string)

        # best practices - item ids should only contain searchable identifiers
        if self.searchable_identifiers == False: 
            string_1 = f"    Item name '{self.object_id}' should only contain Searchable identifiers"
            string_2 = f"    Identifiers should consist of only lowercase characters, numbers, '_', and '-'"
            string_3 = f"    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#searchable-identifiers"
            best_practices.extend([string_1, string_2, string_3, ""])  

        # best practices - item ids should not contain ':' or '/' characters
        if self.percent_encoded:
            string_1 = f"    Item name '{self.object_id}' should not contain ':' or '/'"
            string_2 = f"    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#item-ids"
            best_practices.extend([string_1, string_2, ""])

        # best practices - item ids should match file names
        if self.asset_type == "ITEM" and self.object_id != self.file_name:
            string_1 = f"    Item file names should match their ids: '{self.file_name}' not equal to '{self.object_id}"
            best_practices.extend([string_1, ""])

        # best practices - collections should contain summaries
        if self.asset_type == "COLLECTION" and self.summaries == False:
            string_1 = f"    A STAC collection should contain a summaries field"
            string_2 = f"    https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md"
            best_practices.extend([string_1, string_2, ""])

        # best practices - datetime files should not be set to null
        if self.datetime_null:
            string_1 = f"    Please avoid setting the datetime field to null, many clients search on this field"
            best_practices.extend([string_1, ""])

        # best practices - check unlocated items to make sure bbox field is not set
        if self.unlocated:
            string_1 = f"    Unlocated item. Please avoid setting the bbox field when geometry is set to null"
            best_practices.extend([string_1, ""])

        # best practices - recommend items have a geometry
        if not self.geometry and self.asset_type == "ITEM":
            string_1 = f"    All items should have a geometry field. STAC is not meant for non-spatial data"
            best_practices.extend([string_1, ""])

        # check to see if there are too many links
        if self.bloated_links:
            string_1 = f"    You have {len(self.data['links'])} links. Please consider using sub-collections or sub-catalogs"
            string_2 = f"    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#catalog--collection-practices"
            best_practices.extend([string_1, string_2, ""])

        # best practices - check for bloated metadata in properties
        if self.bloated_metadata:
            string_1 = f"    You have {len(self.data['properties'])} properties. Please consider using links to avoid bloated metadata"
            best_practices.extend([string_1, ""])

        return best_practices