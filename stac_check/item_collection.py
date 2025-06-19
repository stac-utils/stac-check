from typing import Dict

from stac_validator.utilities import fetch_and_parse_file

from stac_check.lint import Linter


def validate_item_collection_dict(stac_file: str, item_collection: Dict) -> None:
    """
    Validate the contents of a STAC Item Collection.

    Args:
        stac_file (str): The URL or path to the STAC collection
        item_collection (dict): The dictionary representation of the item collection.
    """
    original_stac_file = stac_file  # Keep the original collection URL
    for item in item_collection["features"]:
        # For reporting, construct the item URL, but do NOT mutate stac_file
        if isinstance(original_stac_file, str) and "id" in item:
            base_url = original_stac_file.split("?")[0]
            item_url = f"{base_url}/{item['id']}"
        else:
            item_url = original_stac_file

        try:
            linter = Linter(item)
            best_practices = linter.best_practices_msg
            geometry_errors = linter.geometry_errors_msg
            structured_lint = linter.message if hasattr(linter, "message") else {}
            # Ensure the item_url is always included in the path
            if isinstance(structured_lint, dict):
                structured_lint["path"] = item_url
            print(
                {
                    "lint_best_practices": best_practices,
                    "lint_geometry_errors": geometry_errors,
                    "lint_structured": structured_lint,
                }
            )
        except Exception as e:
            print({"lint_error": str(e)})


def validate_item_collection(stac_file: str, pages: int, headers: Dict) -> None:
    """
    Validate a STAC Item Collection with optional pagination.

    Raises:
        URLError, JSONDecodeError, ValueError, TypeError, FileNotFoundError,
        ConnectionError, exceptions.SSLError, OSError, KeyError, HTTPError,
        jsonschema.exceptions.ValidationError, Exception: Various errors
        during fetching or parsing.
    """
    page = 1
    print(f"processing page {page}")
    item_collection = fetch_and_parse_file(str(stac_file), headers)
    validate_item_collection_dict(stac_file=stac_file, item_collection=item_collection)

    try:
        if pages is not None:
            for _ in range(pages - 1):
                if "links" in item_collection:
                    for link in item_collection["links"]:
                        if link["rel"] == "next":
                            page += 1
                            print(f"processing page {page}")
                            next_link = link["href"]
                            stac_file = next_link
                            item_collection = fetch_and_parse_file(
                                str(stac_file), headers
                            )
                            validate_item_collection_dict(
                                stac_file=stac_file, item_collection=item_collection
                            )
                            break
    except Exception as e:
        print(f"Validating the item collection failed on page {page}: {str(e)}")


validate_item_collection("https://stac.geobon.org/collections/chelsa-clim/items", 2, {})
