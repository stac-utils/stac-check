from stac_validator import stac_validator

class Linter:
    def __init__(self, item):
        self.item = item

    def parse_file(self):
        info = self.validate_file(self.item)
        return info

    def validate_file(self, file):
        stac = stac_validator.StacValidate(file)
        stac.run()
        return stac.message[0]["valid_stac"]
