import pkg_resources
from stac_validator.validate import StacValidate
from stac_validator.utilities import is_valid_url
import json
import yaml
import os
from dataclasses import dataclass
import requests
from typing import Optional
from dotenv import load_dotenv
import pkg_resources

load_dotenv()

@dataclass
class Linter:
    item: str
    config_file: Optional[str] = None
    assets: bool = False
    links: bool = False
    recursive: bool = False
    max_depth: Optional[int] = None

    def __post_init__(self):
        self.data = self.load_data(self.item)
        self.message = self.validate_file(self.item)
        self.config = self.parse_config(self.config_file)
        self.asset_type = self.message["asset_type"] if "asset_type" in self.message else ""
        self.version = self.message["version"] if "version" in self.message else ""
        self.validator_version = pkg_resources.require("stac-validator")[0].version
        self.validate_all = self.recursive_validation(self.item)
        self.valid_stac = self.message["valid_stac"]
        self.error_type = self.check_error_type()
        self.error_msg = self.check_error_message()
        self.invalid_asset_format = self.check_links_assets(10, "assets", "format") if self.assets else None
        self.invalid_asset_request = self.check_links_assets(10, "assets", "request") if self.assets else None
        self.invalid_link_format = self.check_links_assets(10, "links", "format") if self.links else None
        self.invalid_link_request = self.check_links_assets(10, "links", "request") if self.links else None
        self.schema = self.message["schema"] if "schema" in self.message else []
        self.object_id = self.data["id"] if "id" in self.data else ""
        self.file_name = os.path.basename(self.item).split('.')[0]
        self.best_practices_msg = self.create_best_practices_msg()

    @staticmethod
    def parse_config(config_file):
        default_config_file = os.getenv("STAC_CHECK_CONFIG")
        if default_config_file:
            with open(default_config_file) as f:
                default_config = yaml.load(f, Loader=yaml.FullLoader)
        else:
            with pkg_resources.resource_stream(__name__, "stac-check.config.yml") as f:
                default_config = yaml.load(f, Loader=yaml.FullLoader)
        if config_file:
            with open(config_file) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
            default_config.update(config)
            
        return default_config

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
            stac = StacValidate(file, recursive=True, max_depth=self.max_depth)
            stac.run()
            return stac.message

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

    def check_bloated_links(self, max_links: Optional[int] = 20):
        if "links" in self.data:
            return len(self.data["links"]) > max_links

    def check_bloated_metadata(self, max_properties: Optional[int] = 20):
        if "properties" in self.data:
            return len(self.data["properties"].keys()) > max_properties

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
                    else:
                        return False
        return True

    def check_links_title_field(self):
        if self.asset_type == "COLLECTION" or self.asset_type == "CATALOG":
            for link in self.data["links"]:
                if "title" not in link and link["rel"] != "self":
                    return False
        return True

    def check_links_self(self):
        if self.asset_type == "ITEM":
            return True
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
        if self.asset_type == "CATALOG" and self.file_name != 'catalog':
            return False 
        elif self.asset_type == "COLLECTION" and self.file_name != 'collection':
            return False
        else:
            return True

    def create_best_practices_dict(self):
        best_practices_dict = {}
        config = self.config["linting"]
        max_links = self.config["settings"]["max_links"]
        max_properties = self.config["settings"]["max_properties"]

        # best practices - item ids should only contain searchable identifiers
        if self.check_searchable_identifiers() == False and config["searchable_identifiers"] == True: 
            msg_1 = f"Item name '{self.object_id}' should only contain Searchable identifiers"
            msg_2 = f"Identifiers should consist of only lowercase characters, numbers, '_', and '-'"
            best_practices_dict["searchable_identifiers"] = [msg_1, msg_2]

        # best practices - item ids should not contain ':' or '/' characters
        if self.check_percent_encoded() and config["percent_encoded"] == True:
            msg_1 = f"Item name '{self.object_id}' should not contain ':' or '/'"
            msg_2 = f"https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#item-ids"
            best_practices_dict["percent_encoded"] = [msg_1, msg_2]

        # best practices - item ids should match file names
        if not self.check_item_id_file_name() and config["item_id_file_name"] == True:
            msg_1 = f"Item file names should match their ids: '{self.file_name}' not equal to '{self.object_id}"
            best_practices_dict["check_item_id"] = [msg_1]

        # best practices - collection and catalog file names should be collection.json and catalog.json 
        if not self.check_catalog_id_file_name() and config["catalog_id_file_name"] == True: 
            msg_1 = f"Object should be called '{self.asset_type.lower()}.json' not '{self.file_name}.json'"
            best_practices_dict["check_catalog_id"] = [msg_1]

        # best practices - collections should contain summaries
        if self.check_summaries() == False and config["check_summaries"] == True:
            msg_1 = f"A STAC collection should contain a summaries field"
            msg_2 = f"It is recommended to store information like eo:bands in summaries"
            best_practices_dict["check_summaries"] = [msg_1, msg_2]

        # best practices - datetime fields should not be set to null
        if self.check_datetime_null() and config["null_datetime"] == True:
            msg_1 = f"Please avoid setting the datetime field to null, many clients search on this field"
            best_practices_dict["datetime_null"] = [msg_1]

        # best practices - check unlocated items to make sure bbox field is not set
        if self.check_unlocated() and config["check_unlocated"] == True:
            msg_1 = f"Unlocated item. Please avoid setting the bbox field when geometry is set to null"
            best_practices_dict["check_unlocated"] = [msg_1]

        # best practices - recommend items have a geometry
        if self.check_geometry_null() and config["check_geometry"] == True:
            msg_1 = f"All items should have a geometry field. STAC is not meant for non-spatial data"
            best_practices_dict["null_geometry"] = [msg_1]

        # check to see if there are too many links
        if self.check_bloated_links(max_links=max_links) and config["bloated_links"] == True:
            msg_1 = f"You have {len(self.data['links'])} links. Please consider using sub-collections or sub-catalogs"
            best_practices_dict["bloated_links"] = [msg_1]

        # best practices - check for bloated metadata in properties
        if self.check_bloated_metadata(max_properties=max_properties) and config["bloated_metadata"] == True:
            msg_1 = f"You have {len(self.data['properties'])} properties. Please consider using links to avoid bloated metadata"
            best_practices_dict["bloated_metadata"] = [msg_1]

        # best practices - ensure thumbnail is a small file size ["png", "jpeg", "jpg", "webp"]
        if not self.check_thumbnail() and self.asset_type == "ITEM" and config["check_thumbnail"] == True:
            msg_1 = f"A thumbnail should have a small file size ie. png, jpeg, jpg, webp"
            best_practices_dict["check_thumbnail"] = [msg_1]

        # best practices - ensure that links in catalogs and collections include a title field
        if not self.check_links_title_field() and config["links_title"] == True:
            msg_1 = f"Links in catalogs and collections should always have a 'title' field"
            best_practices_dict["check_links_title"] = [msg_1]

        # best practices - ensure that links in catalogs and collections include self link
        if not self.check_links_self() and config["links_self"] == True:
            msg_1 = f"A link to 'self' in links is strongly recommended"
            best_practices_dict["check_links_self"] = [msg_1]

        return best_practices_dict

    def create_best_practices_msg(self):
        best_practices = list()
        base_string = "STAC Best Practices: "
        best_practices.append(base_string)

        for _,v in self.create_best_practices_dict().items():
            for value in v:
                best_practices.extend(["    " +value])  
            best_practices.extend([""])

        return best_practices