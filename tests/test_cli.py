"""Tests for the stac-check CLI."""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

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
    with patch("stac_check.cli.ApiLinter") as mock_api_linter, patch(
        "stac_check.cli.Linter"
    ) as mock_linter:
        # Mock ApiLinter instance
        mock_api_instance = MagicMock()
        mock_api_instance.lint_all.return_value = [{"valid_stac": True}]
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
        )


def test_cli_item_collection(runner):
    """Test --item-collection flag with mock."""
    with patch("stac_check.cli.ApiLinter") as mock_api_linter, patch(
        "stac_check.cli.Linter"
    ) as mock_linter:
        # Mock ApiLinter instance
        mock_api_instance = MagicMock()
        mock_api_instance.lint_all.return_value = [{"valid_stac": True}]
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
    with patch("stac_check.cli.Linter") as mock_linter, patch(
        "stac_check.cli.importlib.import_module"
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
