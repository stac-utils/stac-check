import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import pkg_resources
import requests
import yaml
from dotenv import load_dotenv
from stac_validator.utilities import is_valid_url
from stac_validator.validate import StacValidate

load_dotenv()


@dataclass
class Linter:
    """A class for linting STAC JSON files and generating validation messages.

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
        schema (List[str]): A list of the STAC JSON file's JSON schema files.
        object_id (str): A string representing the STAC JSON file's ID.
        file_name (str): A string representing the name of the file containing the STAC JSON data.
        best_practices_msg (str): A string representing best practices messages for the STAC JSON file.

    Methods:
        parse_config(config_file: Optional[str] = None) -> Dict:
            Parses a YAML configuration file and returns a dictionary with the configuration settings.

        def get_asset_name(self, file: Union[str, Dict] = None) -> str:
            Returns the name of a file.

        load_data(self, file: Union[str, Dict]) -> Dict:
            Loads a STAC JSON file from a URL or file path and returns a dictionary representation.

        validate_file(self, file: Union[str, dict]) -> Dict[str, Any]:
            Validates a STAC JSON file and returns a dictionary with the validation message.

        recursive_validation(self, file: Union[str, Dict[str, Any]]) -> str:
            Validates a STAC JSON file recursively and returns a dictionary with the validation message.

        set_update_message(self) -> str:
            Sets a message regarding the recommended version of the STAC JSON file standard.

        check_links_assets(self, num_links: int, url_type: str, format_type: str) -> List[str]:
            Checks whether the STAC JSON file has links or assets with invalid formats or requests.

        check_error_type(self) -> str:
            Checks whether the STAC JSON file has an error type.

        check_error_message(self) -> str:
            Checks whether the STAC JSON file has an error message.

        def check_summaries(self) -> bool:
            Checks whether the STAC JSON file has summaries.

        check_bloated_links(self, max_links: Optional[int] = 20) -> bool:
            Checks whether the STAC JSON file has bloated links.

        check_bloated_metadata(self, max_properties: Optional[int] = 20) -> bool:
            Checks whether the STAC JSON file has bloated metadata.

        check_datetime_null(self) -> bool:
            Checks whether the STAC JSON file has a null datetime.

        check_unlocated(self) -> bool:
            Checks whether the STAC JSON file has unlocated items.

        check_geometry_null(self) -> bool:
            Checks whether the STAC JSON file has a null geometry.

        check_searchable_identifiers(self) -> bool:
            Checks whether the STAC JSON file has searchable identifiers.

        check_percent_encoded(self) -> bool:
            Checks whether the STAC JSON file has percent-encoded characters.

        check_thumbnail(self) -> bool:
            Checks whether the STAC JSON file has a thumbnail.

        check_links_title_field(self) -> bool:
            Checks whether the STAC JSON file has a title field in its links.

        check_links_self(self) -> bool:
            Checks whether the STAC JSON file has a self link.

        check_item_id_file_name(self) -> bool:
            Checks whether the filename of an Item conforms to the STAC specification.

        check_catalog_file_name(self) -> str:
            Checks whether the filename of a Catalog or Collection conforms to the STAC specification.

        create_best_practices_dict(self) -> Dict[str, Any]:
            Creates a dictionary with best practices recommendations for the STAC JSON file.

        create_best_practices_msg(self) -> List[str]:
            Creates a message with best practices recommendations for the STAC JSON file.
    """

    item: Union[str, dict]  # url, file name, or dictionary
    config_file: Optional[str] = None
    assets: bool = False
    links: bool = False
    recursive: bool = False
    max_depth: Optional[int] = None

    def __post_init__(self):
        self.data = self.load_data(self.item)
        self.message = self.validate_file(self.item)
        self.config = self.parse_config(self.config_file)
        self.asset_type = (
            self.message["asset_type"] if "asset_type" in self.message else ""
        )
        self.version = self.message["version"] if "version" in self.message else ""
        self.validator_version = pkg_resources.require("stac-validator")[0].version
        self.validate_all = self.recursive_validation(self.item)
        self.valid_stac = self.message["valid_stac"]
        self.error_type = self.check_error_type()
        self.error_msg = self.check_error_message()
        self.invalid_asset_format = (
            self.check_links_assets(10, "assets", "format") if self.assets else None
        )
        self.invalid_asset_request = (
            self.check_links_assets(10, "assets", "request") if self.assets else None
        )
        self.invalid_link_format = (
            self.check_links_assets(10, "links", "format") if self.links else None
        )
        self.invalid_link_request = (
            self.check_links_assets(10, "links", "request") if self.links else None
        )
        self.schema = self.message["schema"] if "schema" in self.message else []
        self.object_id = self.data["id"] if "id" in self.data else ""
        self.file_name = self.get_asset_name(self.item)
        self.best_practices_msg = self.create_best_practices_msg()

    @staticmethod
    def parse_config(config_file: Optional[str] = None) -> Dict:
        """Parse the configuration file for STAC checks.

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
        """
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

    def get_asset_name(self, file: Union[str, Dict] = None) -> str:
        """Extracts the name of an asset from its file path or from a STAC item asset dictionary.

        Args:
            file (Union[str, dict], optional): A string representing the file path to the asset or a dictionary representing the
                asset as specified in a STAC item's `assets` property.

        Returns:
            A string containing the name of the asset.

        Raises:
            TypeError: If the input `file` is not a string or a dictionary.
        """
        if isinstance(file, str):
            return os.path.basename(file).split(".")[0]
        else:
            return file["id"]

    def load_data(self, file: Union[str, Dict]) -> Dict:
        """Loads JSON data from a file or URL.

        Args:
            file (Union[str, Dict]): A string representing the path to a JSON file or a dictionary containing the JSON data.

        Returns:
            A dictionary containing the loaded JSON data.

        Raises:
            TypeError: If the input `file` is not a string or dictionary.
            ValueError: If `file` is a string that doesn't represent a valid URL or file path.
            requests.exceptions.RequestException: If there is an error making a request to a URL.
            JSONDecodeError: If the JSON data cannot be decoded.
            FileNotFoundError: If the specified file cannot be found.
        """

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

    def validate_file(self, file: Union[str, dict]) -> Dict[str, Any]:
        """Validates the given file path or STAC dictionary against the validation schema.

        Args:
            file (Union[str, dict]): A string representing the file path to the STAC file or a dictionary representing the STAC
                item.

        Returns:
            A dictionary containing the results of the validation, including the status of the validation and any errors
            encountered.

        Raises:
            ValueError: If `file` is not a valid file path or STAC dictionary.
        """
        if isinstance(file, str):
            stac = StacValidate(file, links=self.links, assets=self.assets)
            stac.run()
        elif isinstance(file, dict):
            stac = StacValidate()
            stac.validate_dict(file)
        else:
            raise ValueError("Input must be a file path or STAC dictionary.")
        return stac.message[0]

    def recursive_validation(self, file: Union[str, Dict[str, Any]]) -> str:
        """Recursively validate a STAC item or catalog file and its child items.

        Args:
            file (Union[str, Dict[str, Any]]): A string representing the file path to the STAC item or catalog, or a
                dictionary representing the STAC item or catalog.

        Returns:
            A string containing the validation message.

        Raises:
            TypeError: If the input `file` is not a string or a dictionary.
        """
        if self.recursive:
            if isinstance(file, str):
                stac = StacValidate(file, recursive=True, max_depth=self.max_depth)
                stac.run()
            else:
                stac = StacValidate(recursive=True, max_depth=self.max_depth)
                stac.validate_dict(file)
            return stac.message
        else:
            return "Recursive validation is disabled."

    def set_update_message(self) -> str:
        """Returns a message for users to update their STAC version.

        Returns:
            A string containing a message for users to update their STAC version.
        """
        if self.version != "1.0.0":
            return f"Please upgrade from version {self.version} to version 1.0.0!"
        else:
            return "Thanks for using STAC version 1.0.0!"

    def check_links_assets(
        self, num_links: int, url_type: str, format_type: str
    ) -> List[str]:
        """Checks the links and assets in the STAC catalog and returns a list of invalid links of a specified type and format.

        Args:
            num_links (int): The maximum number of invalid links to return.
            url_type (str): The type of URL to check, which can be either 'self' or 'external'.
            format_type (str): The format of the URL to check, which can be either 'html' or 'json'.

        Returns:
            A list of invalid links of the specified type and format. If there are no invalid links, an empty list is returned.
        """
        links = []
        if f"{url_type}_validated" in self.message:
            for invalid_request_url in self.message[f"{url_type}_validated"][
                f"{format_type}_invalid"
            ]:
                if invalid_request_url not in links and "http" in invalid_request_url:
                    links.append(invalid_request_url)
                num_links = num_links - 1
                if num_links == 0:
                    return links
        return links

    def check_error_type(self) -> str:
        """Returns the error type of a STAC validation if it exists in the validation message,
        and an empty string otherwise.

        Returns:
            str: A string containing the error type of a STAC validation if it exists in the validation message, and an
            empty string otherwise.
        """
        if "error_type" in self.message:
            return self.message["error_type"]
        else:
            return ""

    def check_error_message(self) -> str:
        """Checks whether the `message` attribute contains an `error_message` field.

        Returns:
            A string containing the value of the `error_message` field, or an empty string if the field is not present.
        """
        if "error_message" in self.message:
            return self.message["error_message"]
        else:
            return ""

    def check_summaries(self) -> bool:
        """Check if a Collection asset has a "summaries" property.

        Returns:
            A boolean indicating whether the Collection asset has a "summaries" property.
        """
        if self.asset_type == "COLLECTION":
            return "summaries" in self.data
        else:
            return False

    def check_bloated_links(self, max_links: Optional[int] = 20) -> bool:
        """Checks if the number of links in the STAC data exceeds a certain maximum.

        Args:
            max_links (Optional[int]): The maximum number of links that the STAC data is allowed to have. Default is 20.

        Returns:
            bool: A boolean indicating if the number of links in the STAC data exceeds the specified maximum.
        """
        if "links" in self.data:
            return len(self.data["links"]) > max_links
        else:
            return False

    def check_bloated_metadata(self, max_properties: Optional[int] = 20) -> bool:
        """Checks whether a STAC item's metadata contains too many properties.

        Args:
            max_properties (int, optional): The maximum number of properties that the metadata can contain before it is
                considered too bloated. Defaults to 20.

        Returns:
            bool: True if the number of properties in the metadata exceeds the maximum number of properties specified by
                `max_properties`, False otherwise.
        """
        if "properties" in self.data:
            return len(self.data["properties"].keys()) > max_properties
        return False

    def check_datetime_null(self) -> bool:
        """Checks if the STAC item has a null datetime property.

        Returns:
            bool: A boolean indicating whether the datetime property is null (True) or not (False).
        """
        if "properties" in self.data:
            if "datetime" in self.data["properties"]:
                if self.data["properties"]["datetime"] is None:
                    return True
        else:
            return False
        return False

    def check_unlocated(self) -> bool:
        """Checks if a STAC item is unlocated, i.e., has no geometry but has a bounding box.

        Returns:
            bool: True if the STAC item is unlocated, False otherwise.
        """
        if "geometry" in self.data:
            return self.data["geometry"] is None and self.data["bbox"] is not None
        else:
            return False

    def check_geometry_null(self) -> bool:
        """Checks if a STAC item has a null geometry property.

        Returns:
            bool: A boolean indicating whether the geometry property is null (True) or not (False).
        """
        if "geometry" in self.data:
            return self.data["geometry"] is None
        else:
            return False

    def check_searchable_identifiers(self) -> bool:
        """Checks if the identifiers of a STAC item are searchable, i.e.,
        they only contain lowercase letters, numbers, hyphens, and underscores.

        Returns:
            bool: True if the identifiers are searchable, False otherwise.
        """
        if self.asset_type == "ITEM":
            for letter in self.object_id:
                if (
                    letter.islower()
                    or letter.isnumeric()
                    or letter == "-"
                    or letter == "_"
                ):
                    pass
                else:
                    return False
        return True

    def check_percent_encoded(self) -> bool:
        """Checks if the identifiers of a STAC item are percent-encoded, i.e.,
        they only contain lowercase letters, numbers, hyphens, and underscores.

        Returns:
            bool: True if the identifiers are percent-encoded, False otherwise.
        """
        return (
            self.asset_type == "ITEM" and "/" in self.object_id or ":" in self.object_id
        )

    def check_thumbnail(self) -> bool:
        """Checks if the thumbnail of a STAC item is valid, i.e., it has a valid format.

        Returns:
            bool: True if the thumbnail is valid, False otherwise.
        """
        if "assets" in self.data:
            if "thumbnail" in self.data["assets"]:
                if "type" in self.data["assets"]["thumbnail"]:
                    if (
                        "png" in self.data["assets"]["thumbnail"]["type"]
                        or "jpeg" in self.data["assets"]["thumbnail"]["type"]
                        or "jpg" in self.data["assets"]["thumbnail"]["type"]
                        or "webp" in self.data["assets"]["thumbnail"]["type"]
                    ):
                        return True
                    else:
                        return False
        return True

    def check_links_title_field(self) -> bool:
        """Checks if all links in a STAC collection or catalog have a 'title' field.
        The 'title' field is not required for the 'self' link.

        Returns:
            bool: True if all links have a 'title' field, False otherwise.
        """
        if self.asset_type == "COLLECTION" or self.asset_type == "CATALOG":
            for link in self.data["links"]:
                if "title" not in link and link["rel"] != "self":
                    return False
        return True

    def check_links_self(self) -> bool:
        """Checks whether the "self" link is present in the STAC collection or catalog or absent in STAC item.

        Returns:
            bool: True if the "self" link is present in STAC collection or catalog or absent in STAC item, False otherwise.
        """
        if self.asset_type == "ITEM":
            return True
        if self.asset_type == "COLLECTION" or self.asset_type == "CATALOG":
            for link in self.data["links"]:
                if "self" in link["rel"]:
                    return True
        return False

    def check_item_id_file_name(self) -> bool:
        if self.asset_type == "ITEM" and self.object_id != self.file_name:
            return False
        else:
            return True

    def check_catalog_file_name(self) -> bool:
        """Checks whether the filename of a Catalog or Collection conforms to the STAC specification.

        Returns:
            bool: True if the filename is valid, False otherwise.
        """
        if isinstance(self.item, str) and ".json" in self.item:
            if self.asset_type == "CATALOG" and "catalog.json" not in self.item:
                return False
            elif self.asset_type == "COLLECTION" and "collection.json" not in self.item:
                return False
            return True
        else:
            return True

    def create_best_practices_dict(self) -> Dict:
        """Creates a dictionary of best practices violations for the current STAC object. The violations are determined
        by a set of configurable linting rules specified in the config file.

        Returns:
            A dictionary of best practices violations for the current STAC object. The keys in the dictionary correspond
            to the linting rules that were violated, and the values are lists of strings containing error messages and
            recommendations for how to fix the violations.
        """
        best_practices_dict = {}
        config = self.config["linting"]
        max_links = self.config["settings"]["max_links"]
        max_properties = self.config["settings"]["max_properties"]

        # best practices - item ids should only contain searchable identifiers
        if (
            self.check_searchable_identifiers() == False
            and config["searchable_identifiers"] == True
        ):
            msg_1 = f"Item name '{self.object_id}' should only contain Searchable identifiers"
            msg_2 = "Identifiers should consist of only lowercase characters, numbers, '_', and '-'"
            best_practices_dict["searchable_identifiers"] = [msg_1, msg_2]

        # best practices - item ids should not contain ':' or '/' characters
        if self.check_percent_encoded() and config["percent_encoded"] == True:
            msg_1 = f"Item name '{self.object_id}' should not contain ':' or '/'"
            msg_2 = "https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#item-ids"
            best_practices_dict["percent_encoded"] = [msg_1, msg_2]

        # best practices - item ids should match file names
        if not self.check_item_id_file_name() and config["item_id_file_name"] == True:
            msg_1 = f"Item file names should match their ids: '{self.file_name}' not equal to '{self.object_id}"
            best_practices_dict["check_item_id"] = [msg_1]

        # best practices - collection and catalog file names should be collection.json and catalog.json
        if (
            self.check_catalog_file_name() == False
            and config["catalog_id_file_name"] == True
        ):
            msg_1 = f"Object should be called '{self.asset_type.lower()}.json' not '{self.file_name}.json'"
            best_practices_dict["check_catalog_id"] = [msg_1]

        # best practices - collections should contain summaries
        if self.check_summaries() == False and config["check_summaries"] == True:
            msg_1 = "A STAC collection should contain a summaries field"
            msg_2 = "It is recommended to store information like eo:bands in summaries"
            best_practices_dict["check_summaries"] = [msg_1, msg_2]

        # best practices - datetime fields should not be set to null
        if self.check_datetime_null() and config["null_datetime"] == True:
            msg_1 = "Please avoid setting the datetime field to null, many clients search on this field"
            best_practices_dict["datetime_null"] = [msg_1]

        # best practices - check unlocated items to make sure bbox field is not set
        if self.check_unlocated() and config["check_unlocated"] == True:
            msg_1 = "Unlocated item. Please avoid setting the bbox field when geometry is set to null"
            best_practices_dict["check_unlocated"] = [msg_1]

        # best practices - recommend items have a geometry
        if self.check_geometry_null() and config["check_geometry"] == True:
            msg_1 = "All items should have a geometry field. STAC is not meant for non-spatial data"
            best_practices_dict["null_geometry"] = [msg_1]

        # check to see if there are too many links
        if (
            self.check_bloated_links(max_links=max_links)
            and config["bloated_links"] == True
        ):
            msg_1 = f"You have {len(self.data['links'])} links. Please consider using sub-collections or sub-catalogs"
            best_practices_dict["bloated_links"] = [msg_1]

        # best practices - check for bloated metadata in properties
        if (
            self.check_bloated_metadata(max_properties=max_properties)
            and config["bloated_metadata"] == True
        ):
            msg_1 = f"You have {len(self.data['properties'])} properties. Please consider using links to avoid bloated metadata"
            best_practices_dict["bloated_metadata"] = [msg_1]

        # best practices - ensure thumbnail is a small file size ["png", "jpeg", "jpg", "webp"]
        if (
            not self.check_thumbnail()
            and self.asset_type == "ITEM"
            and config["check_thumbnail"] == True
        ):
            msg_1 = "A thumbnail should have a small file size ie. png, jpeg, jpg, webp"
            best_practices_dict["check_thumbnail"] = [msg_1]

        # best practices - ensure that links in catalogs and collections include a title field
        if not self.check_links_title_field() and config["links_title"] == True:
            msg_1 = (
                "Links in catalogs and collections should always have a 'title' field"
            )
            best_practices_dict["check_links_title"] = [msg_1]

        # best practices - ensure that links in catalogs and collections include self link
        if not self.check_links_self() and config["links_self"] == True:
            msg_1 = "A link to 'self' in links is strongly recommended"
            best_practices_dict["check_links_self"] = [msg_1]

        return best_practices_dict

    def create_best_practices_msg(self) -> List[str]:
        """
        Generates a list of best practices messages based on the results of the 'create_best_practices_dict' method.

        Returns:
            A list of strings, where each string contains a best practice message. Each message starts with the
            'STAC Best Practices:' base string and is followed by a specific recommendation. Each message is indented
            with four spaces, and there is an empty string between each message for readability.
        """
        best_practices = list()
        base_string = "STAC Best Practices: "
        best_practices.append(base_string)

        for _, v in self.create_best_practices_dict().items():
            for value in v:
                best_practices.extend(["    " + value])
            best_practices.extend([""])

        return best_practices
