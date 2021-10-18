from stac_validator import stac_validator
from dataclasses import dataclass

@dataclass
class Linter:
    item: str

    def __post_init__(self):
        self.message = self.validate_file(self.item)
        self.version = self.check_version()
        self.link_format = self.check_link_format()
        self.asset_type = self.check_asset_type()
        self.validator_version = "2.3.0"
        self.schema = self.check_schema()
        self.update_msg = self.set_update_message()
        self.valid_stac = self.message["valid_stac"]
        self.error_type = self.check_error_type()
        self.error_msg = self.check_error_message()

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

    def check_link_format(self):
        if "links_validated" in self.message:
            return self.message["links_validated"]["format_invalid"]
        else:
            return []

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

    
