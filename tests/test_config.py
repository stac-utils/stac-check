from stac_check.lint import Linter

def test_linter_config_file():
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file)

    # Use defualt config
    assert linter.config["linting"]["searchable_identifiers"] == True
    assert linter.create_best_practices_dict()["searchable_identifiers"] == [
        f"Item name '{linter.object_id}' should only contain Searchable identifiers",
        "Identifiers should consist of only lowercase characters, numbers, '_', and '-'"
    ]

    # Load config file
    linter = Linter(file, config_file="tests/test.config.yml")

    assert linter.config["linting"]["searchable_identifiers"] == False
    assert "searchable_identifiers" not in linter.create_best_practices_dict()

def test_linter_max_links():
    file = "sample_files/1.0.0/core-item-bloated.json"
    linter = Linter(file)

    assert linter.check_bloated_links() == True
    assert len(linter.data["links"]) > 20

    # Load config file
    linter = Linter(file, config_file="tests/test.config.yml")
    assert "bloated_links" not in linter.create_best_practices_dict()


    