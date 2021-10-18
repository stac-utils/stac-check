from stac_validator import stac_validator

class Linter:
    def __init__(
        self, 
        item = str
    ):
        self.item = item
        self.version = ""
        self.message = {}
        self.validator_version = "2.3.0"
        self.schema = []
        self.update_msg = ""
        self.asset_type = ""
        self.valid_stac = False
        self.link_format = []

    def parse_file(self):
        self.message = self.validate_file(self.item)
        self.check_version()
        self.check_link_format()
        self.schema = self.message["schema"]
        if "asset_type" in self.message:
            self.asset_type = self.message["asset_type"]
        self.valid_stac = self.message["valid_stac"]
 
    def check_version(self):
        self.version = self.message["version"]
        if self.version != "1.0.0":
            self.update_msg = f"Please upgrade from version {self.version} to version 1.0.0!"
        else:
            self.update_msg = "Thanks for using STAC version 1.0.0!"

    def check_link_format(self):
        if "links_validated" in self.message:
            self.link_format = self.message["links_validated"]["format_invalid"]

    def validate_file(self, file):
        stac = stac_validator.StacValidate(file, links=True)
        stac.run()
        return stac.message[0]

    
