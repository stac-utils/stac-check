import importlib.metadata
import importlib.resources
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

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
        assets_open_urls (bool): Whether to open assets URLs when validating assets. Defaults to True.
        headers (dict): HTTP headers to include in the requests.
        pydantic (bool, optional): A boolean value indicating whether to use pydantic validation. Defaults to False.

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
        geometry_errors_msg (str): A string representing geometry-related error messages for the STAC JSON file.

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

        check_bbox_antimeridian(self) -> bool:
            Checks if a bbox that crosses the antimeridian is correctly formatted.

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

        create_geometry_errors_msg(self) -> List[str]:
            Creates a message with geometry-related error messages for the STAC JSON file.
    """

    item: Union[str, Dict]
    config_file: Optional[str] = None
    assets: bool = False
    links: bool = False
    recursive: bool = False
    max_depth: Optional[int] = None
    assets_open_urls: bool = True
    headers: Dict = field(default_factory=dict)
    pydantic: bool = False

    def __post_init__(self):
        # Check if pydantic validation is requested but not installed
        if self.pydantic:
            try:
                importlib.import_module("stac_pydantic")
            except ImportError:
                import warnings

                warnings.warn(
                    "stac-pydantic is not installed. Pydantic validation will be disabled. "
                    "Install it with: pip install stac-check[pydantic]",
                    UserWarning,
                    stacklevel=2,
                )
                self.pydantic = False

        self.data = self.load_data(self.item)
        self.message = self.validate_file(self.item)
        self.config = self.parse_config(self.config_file)
        self.asset_type = (
            self.message["asset_type"] if "asset_type" in self.message else ""
        )
        self.version = self.message["version"] if "version" in self.message else ""
        self.validator_version = importlib.metadata.distribution(
            "stac-validator"
        ).version
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
        self.geometry_errors_msg = self.create_geometry_errors_msg()

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
            config_file_path = importlib.resources.files("stac_check").joinpath(
                "stac-check.config.yml"
            )
            with importlib.resources.as_file(config_file_path) as path:
                with open(path) as f:
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
                resp = requests.get(file, headers=self.headers)
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
            stac = StacValidate(
                file,
                links=self.links,
                assets=self.assets,
                assets_open_urls=self.assets_open_urls,
                headers=self.headers,
                pydantic=self.pydantic,
            )
            stac.run()
        elif isinstance(file, dict):
            stac = StacValidate(
                assets_open_urls=self.assets_open_urls,
                headers=self.headers,
                pydantic=self.pydantic,
            )
            stac.validate_dict(file)
        else:
            raise ValueError("Input must be a file path or STAC dictionary.")

        message = stac.message[0]
        return message

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
                stac = StacValidate(
                    file,
                    recursive=True,
                    max_depth=self.max_depth,
                    assets_open_urls=self.assets_open_urls,
                    headers=self.headers,
                    pydantic=self.pydantic,
                )
                stac.run()
            else:
                stac = StacValidate(
                    recursive=True,
                    max_depth=self.max_depth,
                    assets_open_urls=self.assets_open_urls,
                    headers=self.headers,
                    pydantic=self.pydantic,
                )
                stac.validate_dict(file)
            return stac.message
        else:
            return "Recursive validation is disabled."

    def set_update_message(self) -> str:
        """Returns a message for users to update their STAC version.

        Returns:
            A string containing a message for users to update their STAC version.
        """
        if self.version != "1.1.0":
            return f"Please upgrade from version {self.version} to version 1.1.0!"
        else:
            return "Thanks for using STAC version 1.1.0!"

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
            return (
                self.data.get("geometry") is None and self.data.get("bbox") is not None
            )
        else:
            return False

    def check_geometry_null(self) -> bool:
        """Checks if a STAC item has a null geometry property.

        Returns:
            bool: A boolean indicating whether the geometry property is null (True) or not (False).
        """
        if "geometry" in self.data:
            return self.data.get("geometry") is None
        else:
            return False

    def check_bbox_matches_geometry(
        self,
    ) -> Union[bool, Tuple[bool, List[float], List[float], List[float]]]:
        """Checks if the bbox of a STAC item matches its geometry.

        This function verifies that the bounding box (bbox) accurately represents
        the minimum bounding rectangle of the item's geometry. It only applies to
        items with non-null geometry of type Polygon or MultiPolygon.

        Returns:
            Union[bool, Tuple[bool, List[float], List[float], List[float]]]:
                - True if the bbox matches the geometry or if the check is not applicable
                  (e.g., null geometry or non-polygon type).
                - When there's a mismatch: a tuple containing (False, calculated_bbox, actual_bbox, differences)
        """
        # Skip check if geometry is null or bbox is not present
        if (
            "geometry" not in self.data
            or self.data.get("geometry") is None
            or "bbox" not in self.data
            or self.data.get("bbox") is None
        ):
            return True

        geometry = self.data.get("geometry")
        bbox = self.data.get("bbox")

        # Only process Polygon and MultiPolygon geometries
        geom_type = geometry.get("type")
        if geom_type not in ["Polygon", "MultiPolygon"]:
            return True

        # Extract coordinates based on geometry type
        coordinates = []
        if geom_type == "Polygon":
            # For Polygon, use the exterior ring (first element)
            if len(geometry.get("coordinates", [])) > 0:
                coordinates = geometry.get("coordinates")[0]
        elif geom_type == "MultiPolygon":
            # For MultiPolygon, collect all coordinates from all polygons
            for polygon in geometry.get("coordinates", []):
                if len(polygon) > 0:
                    coordinates.extend(polygon[0])

        # If no valid coordinates, skip check
        if not coordinates:
            return True

        # Calculate min/max from coordinates
        lons = [coord[0] for coord in coordinates]
        lats = [coord[1] for coord in coordinates]

        calc_bbox = [min(lons), min(lats), max(lons), max(lats)]

        # Allow for differences that would be invisible when rounded to 6 decimal places
        # 1e-6 would be exactly at the 6th decimal place, so use 5e-7 to be just under that threshold
        epsilon = 5e-7
        differences = [abs(bbox[i] - calc_bbox[i]) for i in range(4)]

        if any(diff > epsilon for diff in differences):
            # Return False along with the calculated bbox, actual bbox, and the differences
            return (False, calc_bbox, bbox, differences)

        return True

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

    def check_geometry_coordinates_definite_errors(
        self,
    ) -> Union[bool, Tuple[bool, List]]:
        """Checks if the coordinates in a geometry contain definite errors.

        This function checks for coordinates that definitely violate the GeoJSON specification:

        1. Latitude values (second element) exceed ±90 degrees
        2. Longitude values (first element) exceed ±180 degrees

        This check focuses on definite errors rather than potential/likely errors.
        For checking potential errors (likely reversed coordinates), use check_geometry_coordinates_order().

        Returns:
            Union[bool, Tuple[bool, List]]:
                - If no errors: True
                - If errors found: (False, list_of_invalid_coordinates)
        """
        if "geometry" not in self.data or self.data.get("geometry") is None:
            return True

        geometry = self.data.get("geometry")
        invalid_coords = []

        # Function to check a single coordinate pair for definite errors
        def is_within_valid_ranges(coord):
            if len(coord) < 2:
                return True  # Not enough elements to check

            lon, lat = coord[0], coord[1]

            # Check if latitude (second value) is outside the valid range
            if abs(lat) > 90:
                invalid_coords.append((lon, lat, "latitude > ±90°"))
                return False

            # Check if longitude (first value) is outside the valid range
            if abs(lon) > 180:
                invalid_coords.append((lon, lat, "longitude > ±180°"))
                return False

            return True

        # Function to recursively check all coordinates in a geometry
        def check_coordinates(coords):
            if isinstance(coords, list):
                if coords and isinstance(coords[0], (int, float)):
                    # This is a single coordinate
                    return is_within_valid_ranges(coords)
                else:
                    # This is a list of coordinates or a list of lists of coordinates
                    return all(check_coordinates(coord) for coord in coords)
            return True

        result = check_coordinates(geometry.get("coordinates", []))

        if result:
            return True
        else:
            return (False, invalid_coords)

    def check_geometry_coordinates_order(self) -> bool:
        """Checks if the coordinates in a geometry may be in the incorrect order.

        This function uses a heuristic to detect coordinates that are likely in the wrong order
        (latitude, longitude instead of longitude, latitude). It looks for cases where:
        - The first value (supposed to be longitude) is > 90 degrees
        - The second value (supposed to be latitude) is < 90 degrees
        - The first value is more than twice the second value

        For checking definite errors (values outside valid ranges), use check_geometry_coordinates_definite_errors().

        Returns:
            bool: True if coordinates appear to be in the correct order, False if they may be reversed.
        """
        if "geometry" not in self.data or self.data.get("geometry") is None:
            return True

        geometry = self.data.get("geometry")

        # Function to check if a single coordinate pair is likely in the correct order
        def is_likely_correct_order(coord):
            if len(coord) < 2:
                return True  # Not enough elements to check

            lon, lat = coord[0], coord[1]

            # Heuristic: If the supposed longitude is > 90 and the supposed latitude is < 90,
            # and the longitude is more than twice the latitude, it's likely in the correct order
            if abs(lon) > 90 and abs(lat) < 90 and abs(lon) > abs(lat) * 2:
                return False

            return True

        # Function to recursively check all coordinates in a geometry
        def check_coordinates(coords):
            if isinstance(coords, list):
                if coords and isinstance(coords[0], (int, float)):
                    # This is a single coordinate
                    return is_likely_correct_order(coords)
                else:
                    # This is a list of coordinates or a list of lists of coordinates
                    return all(check_coordinates(coord) for coord in coords)
            return True

        return check_coordinates(geometry.get("coordinates", []))

    def check_bbox_antimeridian(self) -> bool:
        """
        Checks if a bbox that crosses the antimeridian is correctly formatted.

        According to the GeoJSON spec, when a bbox crosses the antimeridian (180°/-180° longitude),
        the minimum longitude (bbox[0]) should be greater than the maximum longitude (bbox[2]).
        This method checks if this convention is followed correctly.

        Returns:
            bool: True if the bbox is valid (either doesn't cross antimeridian or crosses it correctly),
                  False if it incorrectly crosses the antimeridian.
        """
        if "bbox" not in self.data:
            return True

        bbox = self.data.get("bbox")

        # Extract the 2D part of the bbox (ignoring elevation if present)
        if len(bbox) == 4:  # 2D bbox [west, south, east, north]
            west, _, east, _ = bbox
        elif len(bbox) == 6:  # 3D bbox [west, south, min_elev, east, north, max_elev]
            west, _, _, east, _, _ = bbox

        # Check if the bbox appears to cross the antimeridian
        # This is the case when west > east in a valid bbox that crosses the antimeridian
        # For example: [170, -10, -170, 10] crosses the antimeridian correctly
        # But [-170, -10, 170, 10] is incorrectly belting the globe

        # Invalid if bbox "belts the globe" (too wide)
        if west < east and (east - west) > 180:
            return False
        # Otherwise, valid (normal or valid antimeridian crossing)
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
        linting_config = self.config["linting"]
        geometry_validation_config = self.config["geometry_validation"]
        max_links = self.config["settings"]["max_links"]
        max_properties = self.config["settings"]["max_properties"]

        # best practices - item ids should only contain searchable identifiers
        if (
            self.check_searchable_identifiers() == False
            and linting_config["searchable_identifiers"] == True
        ):
            msg_1 = f"Item name '{self.object_id}' should only contain Searchable identifiers"
            msg_2 = "Identifiers should consist of only lowercase characters, numbers, '_', and '-'"
            best_practices_dict["searchable_identifiers"] = [msg_1, msg_2]

        # best practices - item ids should not contain ':' or '/' characters
        if self.check_percent_encoded() and linting_config["percent_encoded"] == True:
            msg_1 = f"Item name '{self.object_id}' should not contain ':' or '/'"
            msg_2 = "https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#item-ids"
            best_practices_dict["percent_encoded"] = [msg_1, msg_2]

        # best practices - item ids should match file names
        if (
            not self.check_item_id_file_name()
            and linting_config["item_id_file_name"] == True
        ):
            msg_1 = f"Item file names should match their ids: '{self.file_name}' not equal to '{self.object_id}"
            best_practices_dict["check_item_id"] = [msg_1]

        # best practices - collection and catalog file names should be collection.json and catalog.json
        if (
            self.check_catalog_file_name() == False
            and linting_config["catalog_id_file_name"] == True
        ):
            msg_1 = f"Object should be called '{self.asset_type.lower()}.json' not '{self.file_name}.json'"
            best_practices_dict["check_catalog_id"] = [msg_1]

        # best practices - collections should contain summaries
        if (
            self.asset_type == "COLLECTION"
            and self.check_summaries() == False
            and linting_config["check_summaries"] == True
        ):
            msg_1 = "A STAC collection should contain a summaries field"
            msg_2 = "It is recommended to store information like eo:bands in summaries"
            best_practices_dict["check_summaries"] = [msg_1, msg_2]

        # best practices - datetime fields should not be set to null
        if self.check_datetime_null() and linting_config["null_datetime"] == True:
            msg_1 = "Please avoid setting the datetime field to null, many clients search on this field"
            best_practices_dict["datetime_null"] = [msg_1]

        # best practices - check unlocated items to make sure bbox field is not set
        if self.check_unlocated() and linting_config["check_unlocated"] == True:
            msg_1 = "Unlocated item. Please avoid setting the bbox field when geometry is set to null"
            best_practices_dict["check_unlocated"] = [msg_1]

        # best practices - recommend items have a geometry
        if self.check_geometry_null() and linting_config["check_geometry"] == True:
            msg_1 = "All items should have a geometry field. STAC is not meant for non-spatial data"
            best_practices_dict["null_geometry"] = [msg_1]

        # best practices - check if bbox matches geometry
        bbox_check_result = self.check_bbox_matches_geometry()
        bbox_mismatch = False

        if isinstance(bbox_check_result, tuple):
            bbox_mismatch = not bbox_check_result[0]
        else:
            bbox_mismatch = not bbox_check_result

        if (
            bbox_mismatch
            and geometry_validation_config.get("check_bbox_geometry_match", True)
            == True
        ):
            if isinstance(bbox_check_result, tuple):
                # Unpack the result
                _, calc_bbox, actual_bbox, differences = bbox_check_result

                # Format the bbox values for display
                calc_bbox_str = ", ".join([f"{v:.6f}" for v in calc_bbox])
                actual_bbox_str = ", ".join([f"{v:.6f}" for v in actual_bbox])

                # Create a more detailed message about which coordinates differ
                coordinate_labels = [
                    "min longitude",
                    "min latitude",
                    "max longitude",
                    "max latitude",
                ]
                mismatch_details = []

                # Use the same epsilon threshold as in check_bbox_matches_geometry
                epsilon = 5e-7

                for i, (diff, label) in enumerate(zip(differences, coordinate_labels)):
                    if diff > epsilon:
                        mismatch_details.append(
                            f"{label}: calculated={calc_bbox[i]:.6f}, actual={actual_bbox[i]:.6f}, diff={diff:.7f}"
                        )

                msg_1 = "The bbox field does not match the bounds of the geometry. The bbox should be the minimum bounding rectangle of the geometry."
                msg_2 = f"Calculated bbox from geometry: [{calc_bbox_str}]"
                msg_3 = f"Actual bbox in metadata: [{actual_bbox_str}]"

                messages = [msg_1, msg_2, msg_3]
                if mismatch_details:
                    messages.append("Mismatched coordinates:")
                    messages.extend(mismatch_details)
                else:
                    # If we got here but there are no visible differences at 6 decimal places,
                    # add a note explaining that the differences are too small to matter
                    messages.append(
                        "Note: The differences are too small to be visible at 6 decimal places and can be ignored."
                    )

                best_practices_dict["bbox_geometry_mismatch"] = messages
            else:
                msg_1 = "The bbox field does not match the bounds of the geometry. The bbox should be the minimum bounding rectangle of the geometry."
                best_practices_dict["bbox_geometry_mismatch"] = [msg_1]

        # check to see if there are too many links
        if (
            self.check_bloated_links(max_links=max_links)
            and linting_config["bloated_links"] == True
        ):
            msg_1 = f"You have {len(self.data['links'])} links. Please consider using sub-collections or sub-catalogs"
            best_practices_dict["bloated_links"] = [msg_1]

        # best practices - check for bloated metadata in properties
        if (
            self.check_bloated_metadata(max_properties=max_properties)
            and linting_config["bloated_metadata"] == True
        ):
            msg_1 = f"You have {len(self.data['properties'])} properties. Please consider using links to avoid bloated metadata"
            best_practices_dict["bloated_metadata"] = [msg_1]

        # best practices - ensure thumbnail is a small file size ["png", "jpeg", "jpg", "webp"]
        if (
            not self.check_thumbnail()
            and self.asset_type == "ITEM"
            and linting_config["check_thumbnail"] == True
        ):
            msg_1 = "A thumbnail should have a small file size ie. png, jpeg, jpg, webp"
            best_practices_dict["check_thumbnail"] = [msg_1]

        # best practices - ensure that links in catalogs and collections include a title field
        if not self.check_links_title_field() and linting_config["links_title"] == True:
            msg_1 = (
                "Links in catalogs and collections should always have a 'title' field"
            )
            best_practices_dict["check_links_title"] = [msg_1]

        # best practices - ensure that links in catalogs and collections include self link
        if not self.check_links_self() and linting_config["links_self"] == True:
            msg_1 = "A link to 'self' in links is strongly recommended"
            best_practices_dict["check_links_self"] = [msg_1]

        # best practices - ensure that geometry coordinates are in the correct order
        if (
            not self.check_geometry_coordinates_order()
            and geometry_validation_config["geometry_coordinates_order"] == True
        ):
            msg_1 = "Geometry coordinates may be in the wrong order (required order: longitude, latitude)"
            best_practices_dict["geometry_coordinates_order"] = [msg_1]

        # best practices - check if geometry coordinates contain definite errors
        definite_errors_result = self.check_geometry_coordinates_definite_errors()

        # Check if we have a separate config entry for definite errors, otherwise use the same as order check
        config_key = "geometry_coordinates_definite_errors"
        if config_key not in geometry_validation_config:
            config_key = "geometry_coordinates_order"

        if (
            isinstance(definite_errors_result, tuple)
            and not definite_errors_result[0]
            and geometry_validation_config[config_key]
        ):
            # We have definite errors with invalid coordinates
            _, invalid_coords = definite_errors_result

            # Base message
            msg_1 = "Geometry coordinates contain invalid values that violate the GeoJSON specification (latitude must be between -90 and 90, longitude between -180 and 180)"

            # Add details about invalid coordinates (limit to first 5 to avoid excessive output)
            messages = [msg_1]
            for i, (lon, lat, reason) in enumerate(invalid_coords[:5]):
                messages.append(f"Invalid coordinate: [{lon}, {lat}] - {reason}")

            if len(invalid_coords) > 5:
                messages.append(
                    f"...and {len(invalid_coords) - 5} more invalid coordinates"
                )

            best_practices_dict["geometry_coordinates_definite_errors"] = messages
        elif definite_errors_result is False and geometry_validation_config[config_key]:
            # Simple case (backward compatibility)
            msg_1 = "Geometry coordinates contain invalid values that violate the GeoJSON specification (latitude must be between -90 and 90, longitude between -180 and 180)"
            best_practices_dict["geometry_coordinates_definite_errors"] = [msg_1]

        # Check if a bbox that crosses the antimeridian is correctly formatted
        if not self.check_bbox_antimeridian() and geometry_validation_config.get(
            "check_bbox_antimeridian", True
        ):
            # Get the bbox values to include in the error message
            bbox = self.data.get("bbox", [])

            if len(bbox) == 4:  # 2D bbox [west, south, east, north]
                west, _, east, _ = bbox
            elif (
                len(bbox) == 6
            ):  # 3D bbox [west, south, min_elev, east, north, max_elev]
                west, _, _, east, _, _ = bbox

            msg_1 = f"BBox crossing the antimeridian should have west longitude > east longitude (found west={west}, east={east})"
            msg_2 = f"Current bbox format appears to be belting the globe instead of properly crossing the antimeridian. Bbox: {bbox}"

            best_practices_dict["check_bbox_antimeridian"] = [msg_1, msg_2]

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

        best_practices_dict = self.create_best_practices_dict()

        # Filter out geometry-related errors as they will be displayed separately
        geometry_keys = [
            "geometry_coordinates_order",
            "geometry_coordinates_definite_errors",
            "check_bbox_antimeridian",
            "check_bbox_geometry_match",
        ]
        filtered_dict = {
            k: v for k, v in best_practices_dict.items() if k not in geometry_keys
        }

        for _, v in filtered_dict.items():
            for value in v:
                best_practices.extend(["    " + value])
            best_practices.extend([""])

        return best_practices

    def create_geometry_errors_msg(self) -> List[str]:
        """
        Generates a list of geometry-related error messages based on the results of the 'create_best_practices_dict' method.

        This separates geometry coordinate validation errors from other best practices for clearer presentation.

        Returns:
            A list of strings, where each string contains a geometry error message. Each message starts with the
            'Geometry Validation Errors [BETA]:' base string and is followed by specific details. Each message is indented
            with four spaces, and there is an empty string between each message for readability.
        """
        # Check if geometry validation is enabled
        geometry_config = self.config.get("geometry_validation", {})
        if not geometry_config.get("enabled", True):
            return []  # Geometry validation is disabled

        geometry_errors = list()
        base_string = "Geometry Validation Errors [BETA]: "
        geometry_errors.append(base_string)

        best_practices_dict = self.create_best_practices_dict()

        # Extract only geometry-related errors
        geometry_keys = [
            "geometry_coordinates_order",
            "geometry_coordinates_definite_errors",
            "check_bbox_antimeridian",
            "check_bbox_geometry_match",
        ]
        geometry_dict = {
            k: v for k, v in best_practices_dict.items() if k in geometry_keys
        }

        if not geometry_dict:
            return []  # No geometry errors found

        for _, v in geometry_dict.items():
            for value in v:
                geometry_errors.extend(["    " + value])
            geometry_errors.extend([""])

        return geometry_errors
