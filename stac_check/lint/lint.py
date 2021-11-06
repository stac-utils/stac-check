from stac_validator import stac_validator
from dataclasses import dataclass

@dataclass
class Linter:
    item: str

    def __post_init__(self):
        self.message = self.validate_file(self.item)
        self.asset_type = self.check_asset_type()
        self.version = self.check_version()
        self.validator_version = "2.3.0"
        self.update_msg = self.set_update_message()
        self.valid_stac = self.message["valid_stac"]
        self.error_type = self.check_error_type()
        self.error_msg = self.check_error_message()
        self.invalid_asset_format = self.check_asset_format(10)
        self.invalid_link_format = self.check_link_format(10)
        self.invalid_link_request = self.check_link_request(10)
        self.schema = self.check_schema()

    def validate_file(self, file):
        stac = stac_validator.StacValidate(file, links=True)
        stac.run()
        return stac.message[0]

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

    def check_asset_format(self, num_links):
        invalid_assets_format = []
        if "assets_validated" in self.message:
            for invalid_format_url in self.message["assets_validated"]["format_invalid"]:
                if invalid_format_url not in invalid_assets_format:
                    invalid_assets_format.append(invalid_format_url)
                num_links = num_links - 1
                if num_links == 0:
                    return invalid_assets_format
        return invalid_assets_format

    def check_link_format(self, num_links):
        invalid_links_format = []
        if "links_validated" in self.message:
            for invalid_format_url in self.message["links_validated"]["format_invalid"]:
                if invalid_format_url not in invalid_links_format:
                    invalid_links_format.append(invalid_format_url)
                num_links = num_links - 1
                if num_links == 0:
                    return invalid_links_format
        return invalid_links_format

    def check_link_request(self, num_links):
        invalid_links_request = []
        if "links_validated" in self.message:
            for invalid_request_url in self.message["links_validated"]["request_invalid"]:
                if invalid_request_url not in invalid_links_request and 'http' in invalid_request_url:
                    invalid_links_request.append(invalid_request_url)
                num_links = num_links - 1
                if num_links == 0:
                    return invalid_links_request
        return invalid_links_request

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

    
