from stac_validator import stac_validator

class Linter:
    def __init__(
        self, 
        item = str
    ):
        self.item = item
        self.message = self.validate_file(self.item)

    def parse_file(self):
        return self.message

    def validate_file(self, file):
        stac = stac_validator.StacValidate(file)
        stac.run()
        return stac.message

    
