from stac_validator import stac_validator

class Linter:
    def __init__(
        self, 
        item = str
    ):
        self.item = item
        self.message = self.validate_file(self.item)
        self.validator_version = "2.3.0"

    def parse_file(self):
        info = {}
        info = self.check_version(info)
        info["stac_validator"] = self.message
        return info
 
    def check_version(self, info):
        if self.message["valid_stac"] and self.message["version"] != "1.0.0":
            info["update"] = f"Please upgrade from version {self.message['version']} to version 1.0.0!"
        else:
            info["update"] = "Thanks for using STAC version 1.0.0!"
        return info

    def validate_file(self, file):
        stac = stac_validator.StacValidate(file)
        stac.run()
        return stac.message[0]

    
