from stac_validator.validate import StacValidate
from stac_validator.utilities import is_valid_url
import json
import os
from dataclasses import dataclass
import pystac
import requests

@dataclass
class Linter:
    item: str
    assets: bool = False
    links: bool = False
    recursive: bool = False

    def __post_init__(self):
        self.data = self.load_data(self.item)
        self.message = self.validate_file(self.item)
        self.asset_type = self.message["asset_type"] if "asset_type" in self.message else ""
        self.version = self.message["version"] if "version" in self.message else ""
        self.validator_version = "2.3.0"
        self.valid_stac = self.message["valid_stac"]
        self.error_type = self.check_error_type()
        self.error_msg = self.check_error_message()
        self.invalid_asset_format = self.check_links_assets(10, "assets", "format") if self.assets else None
        self.invalid_asset_request = self.check_links_assets(10, "assets", "request") if self.assets else None
        self.invalid_link_format = self.check_links_assets(10, "links", "format") if self.links else None
        self.invalid_link_request = self.check_links_assets(10, "links", "request") if self.links else None
        self.schema = self.message["schema"] if "schema" in self.message else []
        self.recursive_error_msg = ""
        self.validate_all = self.recursive_validation(self.load_data(self.item))
        self.object_id = self.data["id"] if "id" in self.data else ""
        self.file_name = os.path.basename(self.item).split('.')[0]
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
        if self.asset_type == "COLLECTION":
            return "summaries" in self.data

    def check_bloated_links(self):
        if "links" in self.data:
            return len(self.data["links"]) > 20

    def check_bloated_metadata(self):
        if "properties" in self.data:
            return len(self.data["properties"].keys()) > 20

    def check_datetime_null(self):
        if "properties" in self.data:
            if "datetime" in self.data["properties"]:
                if self.data["properties"]["datetime"] == None:
                    return True
        else:
            return False

    def check_unlocated(self):
        if "geometry" in self.data:
            return self.data["geometry"] is None and self.data["bbox"] is not None

    def check_geometry_null(self):
        if "geometry" in self.data:
            return self.data["geometry"] is None

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

    def check_thumbnail(self):
        if "assets" in self.data:
            if "thumbnail" in self.data["assets"]:
                if "type" in self.data["assets"]["thumbnail"]:
                    if "png" in self.data["assets"]["thumbnail"]["type"] or "jpeg" in self.data["assets"]["thumbnail"]["type"] or \
                        "jpg" in self.data["assets"]["thumbnail"]["type"] or "webp" in self.data["assets"]["thumbnail"]["type"]:
                        return True

    def check_links_title_field(self):
        if self.asset_type == "COLLECTION" or self.asset_type == "CATALOG":
            for link in self.data["links"]:
                if "title" not in link and link["rel"] != "self":
                    return False
        return True

    def check_links_self(self):
        if self.asset_type == "COLLECTION" or self.asset_type == "CATALOG":
            for link in self.data["links"]:
                if "self" in link["rel"]:
                    return True
        return False

    def check_item_id_file_name(self):
        if self.asset_type == "ITEM" and self.object_id != self.file_name:
            return False
        else:
            return True

    def check_catalog_id_file_name(self):
        if self.asset_type == "CATALOG" and self.file_name != 'catalog.json':
            return False 
        elif self.asset_type == "COLLECTION" and self.file_name != 'collection.json':
            return False
        else:
            return True

    def create_best_practices_msg(self):
        best_practices = list()
        base_string = "STAC Best Practices: "
        best_practices.append(base_string)

        # best practices - item ids should only contain searchable identifiers
        if self.check_searchable_identifiers() == False: 
            string_1 = f"    Item name '{self.object_id}' should only contain Searchable identifiers"
            string_2 = f"    Identifiers should consist of only lowercase characters, numbers, '_', and '-'"
            string_3 = f"    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#searchable-identifiers"
            best_practices.extend([string_1, string_2, string_3, ""])  

        # best practices - item ids should not contain ':' or '/' characters
        if self.check_percent_encoded():
            string_1 = f"    Item name '{self.object_id}' should not contain ':' or '/'"
            string_2 = f"    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#item-ids"
            best_practices.extend([string_1, string_2, ""])

        # best practices - item ids should match file names
        if not self.check_item_id_file_name():
            string_1 = f"    Item file names should match their ids: '{self.file_name}' not equal to '{self.object_id}"
            best_practices.extend([string_1, ""])

        # best practices - collection and catalog file names should be collection.json and catalog.json 
        if not self.check_catalog_id_file_name():
            string_1 = f"    Object should be called '{self.asset_type.lower()}.json' not '{self.file_name}.json'"
            best_practices.extend([string_1, ""])

        # best practices - collections should contain summaries
        if self.check_summaries() == False:
            string_1 = f"    A STAC collection should contain a summaries field"
            string_2 = f"    It is recommended to store information like eo:bands in summaries"
            best_practices.extend([string_1, string_2, ""])

        # best practices - datetime files should not be set to null
        if self.check_datetime_null():
            string_1 = f"    Please avoid setting the datetime field to null, many clients search on this field"
            best_practices.extend([string_1, ""])

        # best practices - check unlocated items to make sure bbox field is not set
        if self.check_unlocated():
            string_1 = f"    Unlocated item. Please avoid setting the bbox field when geometry is set to null"
            best_practices.extend([string_1, ""])

        # best practices - recommend items have a geometry
        if self.check_geometry_null():
            string_1 = f"    All items should have a geometry field. STAC is not meant for non-spatial data"
            best_practices.extend([string_1, ""])

        # check to see if there are too many links
        if self.check_bloated_links():
            string_1 = f"    You have {len(self.data['links'])} links. Please consider using sub-collections or sub-catalogs"
            string_2 = f"    https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#catalog--collection-practices"
            best_practices.extend([string_1, string_2, ""])

        # best practices - check for bloated metadata in properties
        if self.check_bloated_metadata():
            string_1 = f"    You have {len(self.data['properties'])} properties. Please consider using links to avoid bloated metadata"
            best_practices.extend([string_1, ""])

        # best practices - ensure thumbnail is a small file size ["png", "jpeg", "jpg", "webp"]
        if not self.check_thumbnail() and self.asset_type == "ITEM":
            string_1 = f"    A thumbnail should have a small file size ie. png, jpeg, jpg, webp"
            best_practices.extend([string_1, ""])

        # best practices - ensure that links in catalogs and collections include a title field
        if not self.check_links_title_field():
            string_1 = f"    Links in catalogs and collections should always have a 'title' field"
            best_practices.extend([string_1, ""])

        # best practices - ensure that links in catalogs and collections include self link
        if not self.check_links_self():
            string_1 = f"    A link to 'self' in links is strongly recommended"
            best_practices.extend([string_1, ""])

        return best_practices