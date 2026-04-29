"""Tests for the stac-check CLI."""

import json
import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from stac_check.cli import is_item_collection
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
    """Test recursive validation."""
    test_dir = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/catalog-with-bad-item.json"
    )
    result = runner.invoke(cli_main, [test_dir, "--recursive"])
    assert result.exit_code == 0
    assert "Assets Checked" in result.output


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
            assert "Passed: True" in content
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
            "--output can only be used with --collections, --item-collection, or --recursive"
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
    assert "FastJSONSchema" in result.output


def test_cli_fast_validation_item_collection(runner):
    """Test --fast flag with an item collection."""
    test_file = os.path.join(
        os.path.dirname(__file__), "../sample_files/1.0.0/feature_collection.json"
    )
    result = runner.invoke(cli_main, [test_file, "--fast"])
    assert result.exit_code == 0
    assert "FastJSONSchema" in result.output
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


def test_cli_fast_validation_skips_best_practices(runner):
    """Test that --fast flag skips best practices validation."""
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
