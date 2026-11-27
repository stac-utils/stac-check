"""Tests for the stac-check CLI."""

import json
import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from stac_check.cli import detect_api_response_type, is_item_collection
from stac_check.cli import main as cli_main


@pytest.fixture
def runner():
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_cli_help(runner):
    """Test the CLI help output."""
    result = runner.invoke(cli_main, ["--help"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output


def test_cli_version(runner):
    """Test the --version flag."""
    result = runner.invoke(cli_main, ["--version"])
    assert result.exit_code == 0
    # The version output is in the format: main, version X.Y.Z
    assert "version" in result.output


def test_cli_validate_local_file(runner):
    """Test validating a local file."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
    )
    result = runner.invoke(cli_main, [test_file])
    assert result.exit_code == 0
    assert "Passed: True" in result.output


def test_cli_validate_recursive(runner):
    """Recursive validation exits non-zero when a child object fails."""
    test_dir = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/catalog-with-bad-item.json"
    )
    result = runner.invoke(cli_main, [test_dir, "--recursive"])
    assert result.exit_code == 1
    assert "Assets Checked" in result.output


def test_cli_validate_recursive_fast(runner):
    """--recursive --fast detects, displays, and fails on child errors."""
    test_dir = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/catalog-with-bad-item.json"
    )
    result = runner.invoke(cli_main, [test_dir, "--recursive", "--fast"])
    assert result.exit_code == 1
    assert "Validation method: stac-valid FastValidator" in result.output
    assert "Failed: 1/3" in result.output
    assert "must contain" in result.output


def test_cli_output_to_file(runner):
    """Test output to file with --output flag."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
    )
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        output_file = tmp.name

    try:
        result = runner.invoke(
            cli_main, [test_file, "--recursive", "--output", output_file]
        )
        assert result.exit_code == 0
        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            content = f.read()
            # Without --verbose the output file holds the summary only
            assert "Passed: 1/1" in content
            assert "Asset 1:" not in content
    finally:
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_cli_collections(runner):
    """Test --collections flag with mock."""
    with (
        patch("stac_check.cli.ApiLinter") as mock_api_linter,
        patch("stac_check.cli.Linter") as mock_linter,
    ):
        # Mock ApiLinter instance
        mock_api_instance = MagicMock()
        mock_api_instance.lint_all.return_value = [{"valid_stac": True}]
        mock_api_instance.total_time = 0.0
        mock_api_instance.schemas_checked = []
        mock_api_instance.fast = False
        mock_api_linter.return_value = mock_api_instance

        # Mock Linter instance used for display
        mock_linter_instance = MagicMock()
        mock_linter.return_value = mock_linter_instance

        result = runner.invoke(
            cli_main,
            ["https://example.com/collections", "--collections", "--pages", "1"],
        )

        assert result.exit_code == 0
        mock_api_linter.assert_called_once_with(
            source="https://example.com/collections",
            object_list_key="collections",
            pages=1,
            headers={},
            verbose=False,
            fast=False,
        )


def test_cli_item_collection(runner):
    """Test --item-collection flag with mock."""
    with (
        patch("stac_check.cli.ApiLinter") as mock_api_linter,
        patch("stac_check.cli.Linter") as mock_linter,
    ):
        # Mock ApiLinter instance
        mock_api_instance = MagicMock()
        mock_api_instance.lint_all.return_value = [{"valid_stac": True}]
        mock_api_instance.total_time = 0.0
        mock_api_instance.schemas_checked = []
        mock_api_instance.fast = False
        mock_api_linter.return_value = mock_api_instance

        # Mock Linter instance used for display
        mock_linter_instance = MagicMock()
        mock_linter.return_value = mock_linter_instance

        result = runner.invoke(
            cli_main, ["https://example.com/items", "--item-collection", "--pages", "2"]
        )

        assert result.exit_code == 0
        mock_api_linter.assert_called_once_with(
            source="https://example.com/items",
            object_list_key="features",
            pages=2,
            headers={},
            verbose=False,
            fast=False,
        )


def test_cli_output_without_required_flags(runner):
    """Test that --output requires --collections, --item-collection, or --recursive."""
    with tempfile.NamedTemporaryFile() as tmp:
        result = runner.invoke(
            cli_main, ["https://example.com/catalog.json", "--output", tmp.name]
        )
        assert result.exit_code == 1
        assert (
            "--output can only be used with --collections, --item-collection, --catalogs, or --recursive"
            in result.output
        )


def test_cli_verbose_flag(runner):
    """Test that --verbose flag is passed correctly."""
    with patch("stac_check.cli.Linter") as mock_linter:
        mock_instance = MagicMock()
        mock_linter.return_value = mock_instance

        test_file = os.path.join(
            os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
        )
        result = runner.invoke(cli_main, [test_file, "--verbose"])

        assert result.exit_code == 0
        mock_linter.assert_called_once()
        assert mock_linter.call_args[1]["verbose"] is True


def test_cli_headers(runner):
    """Test that custom headers are passed correctly."""
    with patch("stac_check.cli.Linter") as mock_linter:
        mock_instance = MagicMock()
        mock_linter.return_value = mock_instance

        test_file = os.path.join(
            os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
        )
        # The header format is: --header KEY VALUE (space-separated, not colon-separated)
        result = runner.invoke(
            cli_main,
            [
                test_file,
                "--header",
                "Authorization",
                "Bearer token",
                "--header",
                "X-Custom",
                "value",
            ],
        )

        assert result.exit_code == 0
        mock_linter.assert_called_once()
        # The headers should be passed as a dictionary to the Linter
        headers = mock_linter.call_args[1]["headers"]
        assert isinstance(headers, dict)
        assert headers.get("Authorization") == "Bearer token"
        assert headers.get("X-Custom") == "value"


def test_cli_pydantic_flag(runner):
    """Test that the --pydantic flag is passed correctly."""
    with (
        patch("stac_check.cli.Linter") as mock_linter,
        patch("stac_check.cli.importlib.import_module"),
    ):
        mock_instance = MagicMock()
        mock_linter.return_value = mock_instance

        test_file = os.path.join(
            os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
        )

        # Test with --pydantic flag
        result = runner.invoke(cli_main, [test_file, "--pydantic"])

        assert result.exit_code == 0
        mock_linter.assert_called_once()
        # Check that pydantic=True was passed to Linter
        assert mock_linter.call_args[1]["pydantic"] is True

        # Test without --pydantic flag (should default to False)
        mock_linter.reset_mock()
        result = runner.invoke(cli_main, [test_file])

        assert result.exit_code == 0
        mock_linter.assert_called_once()
        assert mock_linter.call_args[1]["pydantic"] is False


def test_is_item_collection_with_valid_file():
    """Test is_item_collection with a valid item collection file."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/feature_collection.json"
    )
    assert is_item_collection(test_file) is True


def test_is_item_collection_with_regular_item():
    """Test is_item_collection with a regular item file."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
    )
    assert is_item_collection(test_file) is False


def test_is_item_collection_with_collection():
    """Test is_item_collection with a collection file."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/collection.json"
    )
    assert is_item_collection(test_file) is False


def test_is_item_collection_with_invalid_file():
    """Test is_item_collection with a non-existent file."""
    assert is_item_collection("/nonexistent/file.json") is False


def test_is_item_collection_with_empty_features():
    """Test is_item_collection with a FeatureCollection that has no features."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump({"type": "FeatureCollection", "features": []}, tmp)
        tmp_path = tmp.name

    try:
        assert is_item_collection(tmp_path) is False
    finally:
        os.unlink(tmp_path)


def test_is_item_collection_with_mock_url():
    """Test is_item_collection with a mocked URL."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "properties": {}}],
    }

    with (
        patch("stac_check.cli.requests.get", return_value=mock_response),
        patch("stac_check.cli.is_valid_url", return_value=True),
    ):
        assert is_item_collection("https://example.com/items") is True


def test_cli_auto_detect_item_collection(runner):
    """Test that the CLI automatically detects and validates item collections."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/feature_collection.json"
    )
    result = runner.invoke(cli_main, [test_file])

    assert result.exit_code == 0
    # Should automatically detect and show item collection validation
    assert "Item Collection" in result.output or "Assets Checked" in result.output


def test_detect_api_response_type_collections():
    """A collections endpoint response is detected as 'collections'."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/collections.json"
    )
    assert detect_api_response_type(test_file) == "collections"


def test_detect_api_response_type_item_collection():
    """A FeatureCollection is detected as 'item_collection'."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/feature_collection.json"
    )
    assert detect_api_response_type(test_file) == "item_collection"


def test_detect_api_response_type_single_object():
    """A regular STAC object returns None."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
    )
    assert detect_api_response_type(test_file) is None


def test_detect_api_response_type_empty_collections():
    """An empty collections list is not auto-detected."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump({"collections": [], "links": []}, tmp)
        tmp_path = tmp.name

    try:
        assert detect_api_response_type(tmp_path) is None
    finally:
        os.unlink(tmp_path)


def test_detect_api_response_type_collections_mock_url():
    """A mocked /collections URL response is detected as 'collections'."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "collections": [{"id": "test", "type": "Collection"}],
        "links": [],
    }

    with (
        patch("stac_check.cli.requests.get", return_value=mock_response),
        patch("stac_check.cli.is_valid_url", return_value=True),
    ):
        assert (
            detect_api_response_type("https://example.com/collections") == "collections"
        )


def test_cli_auto_detect_collections(runner):
    """Test that the CLI auto-detects a collections endpoint response."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/collections.json"
    )
    result = runner.invoke(cli_main, [test_file])

    assert "Collections: Validate all collections" in result.output
    assert "Assets Checked" in result.output
    # 28 collections in the fixture, not a single-object validation
    assert "28 Assets Checked" in result.output


def test_cli_missing_file_clean_error(runner):
    """A nonexistent file exits 1 with a clean error, not a traceback."""
    result = runner.invoke(cli_main, ["/nonexistent/file.json"])

    assert result.exit_code == 1
    assert "file not found" in result.output
    assert "Traceback" not in result.output


def test_cli_invalid_json_clean_error(runner):
    """A non-JSON file exits 1 with a clean error, not a traceback."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp.write("this is not json")
        tmp_path = tmp.name

    try:
        result = runner.invoke(cli_main, [tmp_path])
        assert result.exit_code == 1
        assert "invalid JSON" in result.output
        assert "Traceback" not in result.output
    finally:
        os.unlink(tmp_path)


def test_cli_collections_flag_on_feature_collection_errors(runner):
    """--collections on a FeatureCollection suggests --item-collection."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/feature_collection.json"
    )
    result = runner.invoke(cli_main, [test_file, "--collections"])

    assert result.exit_code == 1
    assert "did you mean --item-collection" in result.output


def test_cli_item_collection_flag_on_collections_errors(runner):
    """--item-collection on a collections response suggests --collections."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/collections.json"
    )
    result = runner.invoke(cli_main, [test_file, "--item-collection"])

    assert result.exit_code == 1
    assert "did you mean --collections" in result.output


def test_cli_empty_object_list_warns(runner):
    """An empty list response warns instead of reporting Passed: 0/0."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump({"type": "FeatureCollection", "features": []}, tmp)
        tmp_path = tmp.name

    try:
        result = runner.invoke(cli_main, [tmp_path, "--item-collection"])
        assert result.exit_code == 0
        assert "nothing was validated" in result.output
    finally:
        os.unlink(tmp_path)


def test_cli_item_collection_pre_1_0_fails(runner):
    """--item-collection reports file-level failures (e.g. unsupported
    STAC version) instead of marking the item valid."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/0.9.0/landsat8-sample.json"
    )
    result = runner.invoke(cli_main, [test_file, "--item-collection"])

    assert result.exit_code == 1
    assert "Failed: 1/1" in result.output
    assert "0.9.0 is not supported" in result.output


def test_cli_collections_flag_on_single_collection(runner):
    """--collections on a lone Collection validates the object itself."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/collection.json"
    )
    result = runner.invoke(cli_main, [test_file, "--collections"])

    assert "1 Assets Checked" in result.output


def test_detect_api_response_type_catalogs():
    """A catalogs endpoint response is detected as 'catalogs'."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/catalogs.json"
    )
    assert detect_api_response_type(test_file) == "catalogs"


def test_cli_auto_detect_catalogs(runner):
    """Test that the CLI auto-detects a catalogs endpoint response."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/catalogs.json"
    )
    result = runner.invoke(cli_main, [test_file])

    assert "Catalogs: Validate all catalogs" in result.output
    assert "Assets Checked" in result.output


def test_cli_catalogs_flag_on_collections_errors(runner):
    """--catalogs on a collections response suggests --collections."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/collections.json"
    )
    result = runner.invoke(cli_main, [test_file, "--catalogs"])

    assert result.exit_code == 1
    assert "did you mean --collections" in result.output


def test_cli_collections_flag_on_catalogs_errors(runner):
    """--collections on a catalogs response suggests --catalogs."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/catalogs.json"
    )
    result = runner.invoke(cli_main, [test_file, "--collections"])

    assert result.exit_code == 1
    assert "did you mean --catalogs" in result.output


def test_cli_auto_detect_respects_explicit_flag(runner):
    """Test that explicit --item-collection flag still works."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/feature_collection.json"
    )
    result = runner.invoke(cli_main, [test_file, "--item-collection"])

    assert result.exit_code == 0
    # Should validate as item collection
    assert "Item Collection" in result.output or "Assets Checked" in result.output


def test_cli_auto_detect_does_not_trigger_with_recursive(runner):
    """Test that auto-detection doesn't trigger when --recursive is used."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
    )
    with patch("stac_check.cli.Linter") as mock_linter:
        mock_instance = MagicMock()
        mock_instance.valid_stac = True
        mock_linter.return_value = mock_instance

        runner.invoke(cli_main, [test_file, "--recursive"])

        # Should use Linter, not ApiLinter (auto-detection disabled with --recursive)
        assert mock_linter.called


def test_cli_fast_validation_single_file(runner):
    """Test --fast flag with a single file."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
    )
    result = runner.invoke(cli_main, [test_file, "--fast"])
    assert result.exit_code == 0
    assert "stac-valid FastValidator" in result.output


def test_cli_fast_validation_item_collection(runner):
    """Test --fast flag with an item collection."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/feature_collection.json"
    )
    result = runner.invoke(cli_main, [test_file, "--fast"])
    assert result.exit_code == 0
    assert "stac-valid FastValidator" in result.output
    assert "Validation Summary" in result.output
    assert "Schemas checked:" in result.output


def test_cli_fast_validation_shows_timing(runner):
    """Test that --fast flag shows timing information."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/feature_collection.json"
    )
    result = runner.invoke(cli_main, [test_file, "--fast"])
    assert result.exit_code == 0
    assert "Timing Information" in result.output or "Validation Time" in result.output


def test_cli_fast_validation_passes_fast_flag(runner):
    """Test that --fast flag is passed to Linter for fast validation."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
    )
    with patch("stac_check.cli.Linter") as mock_linter:
        mock_instance = MagicMock()
        mock_instance.fast = True
        mock_instance.valid_stac = True
        mock_instance.best_practices_msg = []
        mock_instance.geometry_errors_msg = []
        mock_linter.return_value = mock_instance

        runner.invoke(cli_main, [test_file, "--fast"])

        # Verify Linter was called with fast=True
        assert mock_linter.called
        call_kwargs = mock_linter.call_args[1]
        assert call_kwargs.get("fast") is True


def test_cli_fast_linting_removed(runner):
    """--fast-linting was removed in 2.0.0 and is rejected as an unknown option."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/core-item.json"
    )
    result = runner.invoke(cli_main, [test_file, "--fast-linting"])

    assert result.exit_code != 0
    assert "No such option" in result.output
