import pytest

from stac_check.lint import Linter

# Check if stac-pydantic is available
try:
    import importlib

    importlib.import_module("stac_pydantic")
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False

# Test decorator for pydantic tests
pytest.mark.pydantic = pytest.mark.skipif(
    not PYDANTIC_AVAILABLE,
    reason="stac-pydantic is not installed. Run 'pip install -e .[dev]' to install test dependencies.",
)


@pytest.mark.pydantic
def test_lint_pydantic_validation_valid():
    """Test pydantic validation with a valid STAC item."""
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file, pydantic=True)

    assert linter.valid_stac is True
    assert linter.asset_type == "ITEM"
    assert any("stac-pydantic" in schema for schema in linter.message["schema"])
    assert linter.message["validation_method"] == "pydantic"


@pytest.mark.pydantic
def test_lint_pydantic_validation_invalid():
    """Test pydantic validation with an invalid STAC item (missing required fields)."""
    file = "sample_files/1.0.0/bad-item.json"
    linter = Linter(file, pydantic=True)

    assert linter.valid_stac is False
    assert "PydanticValidationError" in linter.message["error_type"]
    assert "id: Field required" in linter.message["error_message"]


def test_pydantic_fallback_without_import(monkeypatch):
    """Test that pydantic validation falls back to JSONSchema when stac-pydantic is not available."""
    # Skip this test if stac-pydantic is actually installed
    if PYDANTIC_AVAILABLE:
        pytest.skip("stac-pydantic is installed, skipping fallback test")

    # Test that pydantic=False works without stac-pydantic
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file, pydantic=False)
    assert linter.valid_stac is True
    assert linter.asset_type == "ITEM"
    assert linter.message["validation_method"] == "default"

    # Test that pydantic=True falls back to JSONSchema when stac-pydantic is not available
    linter = Linter(file, pydantic=True)
    assert linter.valid_stac is True
    assert linter.asset_type == "ITEM"
    assert linter.message["validation_method"] == "default"
