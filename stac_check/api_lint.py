from dataclasses import dataclass
from typing import Dict, List, Optional
from urllib.parse import urlparse, urlunparse

from stac_validator.utilities import fetch_and_parse_file

from stac_check.lint import Linter


@dataclass
class ApiLinter:
    """
    General Linter for paginated STAC endpoints or static files (item collections, collections, etc).

    Args:
        source (str): URL or file path of the STAC endpoint or static file (e.g. /items, /collections, or local JSON).
        object_list_key (str): Key in response containing list of objects (e.g. "features", "collections").
        id_key (str): Key in each object for unique ID (default: "id").
        pages (int): Number of pages to fetch (default: 1).
        headers (dict): Optional headers for HTTP requests.
    """

    def __init__(
        self,
        source: str,
        object_list_key: str,
        id_key: str = "id",
        pages: int = 1,
        headers: Optional[Dict] = None,
    ):
        self.source = source
        self.object_list_key = object_list_key
        self.id_key = id_key
        self.pages = pages
        self.headers = headers or {}
        # self.valid_stac = None

    def _fetch_and_parse(self, url: str) -> Dict:
        return fetch_and_parse_file(url, self.headers)

    def iterate_objects(self):
        """
        Generator that yields (object_dict, object_url) for each object in the endpoint,
        following pagination if necessary.
        """
        stac_file = self.source
        page = 1
        seen_ids = set()

        def get_base_url(url):
            parsed = urlparse(url)
            return urlunparse(parsed._replace(query="", fragment=""))

        while stac_file:
            response = self._fetch_and_parse(stac_file)
            objects = response.get(self.object_list_key, [])
            for obj in objects:
                obj_id = obj.get(self.id_key)
                base_url = get_base_url(stac_file)
                obj_url = f"{base_url}/{obj_id}" if obj_id else base_url
                # Only yield if not seen before (protects against duplicates from bad APIs)
                if obj_id not in seen_ids:
                    seen_ids.add(obj_id)
                    yield obj, obj_url
            # Pagination: look for 'next' link
            next_link = None
            for link in response.get("links", []):
                if link.get("rel") == "next":
                    next_link = link.get("href")
                    break
            if next_link and next_link != stac_file:
                stac_file = next_link
                page += 1
            else:
                break

    def lint_all(self) -> List[Dict]:
        """
        Lints all objects in the (possibly paginated) endpoint.
        Returns a list of flat dicts per object, matching the message structure of Linter.
        Ensures only one result per asset URL.
        """
        results_by_url = {}
        for obj, obj_url in self.iterate_objects():
            try:
                linter = Linter(obj)
                msg = dict(linter.message)
                msg["path"] = obj_url
                msg["best_practices"] = linter.best_practices_msg
                msg["geometry_errors"] = linter.geometry_errors_msg
                # Store the original object to allow recreation of Linter instance later
                msg["original_object"] = obj
                results_by_url[obj_url] = msg
            except Exception as e:
                results_by_url[obj_url] = {
                    "path": obj_url,
                    "valid_stac": False,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "best_practices": [],
                    "geometry_errors": [],
                    "version": None,
                    "schema": [],
                    "recommendation": None,
                    "error_verbose": None,
                    "failed_schema": None,
                    "original_object": obj,  # Still include the original object even if validation failed
                }
        return list(results_by_url.values())

    def print_lint_results(self):
        """
        Prints the lint results for all objects in the endpoint.
        """
        for result in self.lint_all():
            print(result)


# Example usage:
# For item collections:
# linter = ApiLinter(
#     source="https://stac.geobon.org/collections/chelsa-clim/items",
#     object_list_key="features",
#     id_key="id",
#     pages=2,
#     headers={}
# )
# linter.print_lint_results()
#
# For collections endpoint:
# linter = ApiLinter(
#     source="https://stac.geobon.org/collections",
#     object_list_key="collections",
#     id_key="id",
#     pages=1,
#     headers={}
# )
# linter.print_lint_results()

# linter = ApiLinter(
#     source="https://stac.geobon.org/collections/chelsa-clim/items",
#     object_list_key="features",
#     id_key="id",
#     pages=2,
#     headers={}
# )
# linter.print_lint_results()
