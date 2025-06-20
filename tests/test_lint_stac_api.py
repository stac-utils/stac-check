from unittest import mock

import pytest

from stac_check.api_lint import ApiLinter
from stac_check.display_messages import (
    cli_message,
    collections_message,
    item_collection_message,
)


@pytest.fixture
def item_collection_url():
    """URL for a real STAC API item collection endpoint."""
    return "https://stac.geobon.org/collections/chelsa-clim/items"


@pytest.fixture
def collections_url():
    """URL for a real STAC API collections endpoint."""
    return "https://stac.geobon.org/collections"


@pytest.fixture
def invalid_url():
    """URL for a non-existent endpoint to test error handling."""
    return "https://example.com/not-a-real-endpoint"


def test_item_collection_validation(item_collection_url):
    """Test item collection validation with a real STAC API endpoint."""
    linter = ApiLinter(
        source=item_collection_url,
        object_list_key="features",
        id_key="id",
        pages=1,
    )

    results = linter.lint_all()

    # Verify we got results
    assert len(results) > 0
    # Check that items are valid STAC
    assert all(result["valid_stac"] for result in results)
    # Check that we have original objects
    assert all("original_object" in result for result in results)

    # Check specific fields in the results
    for result in results:
        assert "path" in result
        assert "version" in result
        assert "schema" in result
        assert "asset_type" in result
        assert result["asset_type"] == "ITEM"


def test_item_collection_with_pages(item_collection_url):
    """Test item collection validation with pages parameter."""
    # Test with 1 page
    linter_1page = ApiLinter(
        source=item_collection_url,
        object_list_key="features",
        id_key="id",
        pages=1,
    )
    results_1page = linter_1page.lint_all()

    # Test with 2 pages
    linter_2pages = ApiLinter(
        source=item_collection_url,
        object_list_key="features",
        id_key="id",
        pages=2,
    )
    results_2pages = linter_2pages.lint_all()

    # Verify we got more results with 2 pages than with 1 page
    # This assumes the API returns paginated results
    assert len(results_2pages) >= len(results_1page)

    # Check that the pages parameter was respected
    assert linter_1page.pages == 1
    assert linter_2pages.pages == 2


def test_collections_validation(collections_url):
    """Test collections validation with a real STAC API endpoint."""
    linter = ApiLinter(
        source=collections_url,
        object_list_key="collections",
        id_key="id",
        pages=1,
    )

    results = linter.lint_all()

    # Verify we got results
    assert len(results) > 0
    # Check that we have original objects
    assert all("original_object" in result for result in results)
    # Check that all collections have an ID
    assert all("id" in result["original_object"] for result in results)

    # Check specific fields in the results
    for result in results:
        assert "path" in result
        assert "version" in result
        assert "schema" in result


def test_api_linter_initialization(item_collection_url, collections_url):
    """Test that the ApiLinter can be initialized with different parameters."""
    # Test with item collection
    item_linter = ApiLinter(
        source=item_collection_url,
        object_list_key="features",
        id_key="id",
        pages=1,
    )
    assert item_linter.object_list_key == "features"
    assert item_linter.pages == 1
    assert item_linter.id_key == "id"
    assert item_linter.source == item_collection_url

    # Test with collections
    collections_linter = ApiLinter(
        source=collections_url,
        object_list_key="collections",
        id_key="id",
        pages=2,
    )
    assert collections_linter.object_list_key == "collections"
    assert collections_linter.pages == 2
    assert collections_linter.id_key == "id"
    assert collections_linter.source == collections_url

    # Test with custom headers
    headers = {"X-Custom-Header": "test-value"}
    linter_with_headers = ApiLinter(
        source=collections_url,
        object_list_key="collections",
        id_key="id",
        pages=1,
        headers=headers,
    )
    assert linter_with_headers.headers == headers


def test_error_handling_with_individual_items():
    """Test that ApiLinter handles errors with individual items gracefully."""
    # Create a mock that returns a valid response but with an item that will cause an error
    with mock.patch("stac_check.api_lint.fetch_and_parse_file") as mock_fetch:
        # Return a response with a malformed item that will cause an exception during validation
        mock_fetch.return_value = {
            "features": [
                {
                    "id": "valid-item",
                    "type": "Feature",
                    "geometry": {},
                    "properties": {},
                },
                # This item is missing required fields and will cause validation to fail
                {"id": "invalid-item"},
            ]
        }

        linter = ApiLinter(
            source="https://example.com/items",
            object_list_key="features",
            id_key="id",
            pages=1,
        )

        # This should not raise an exception
        results = linter.lint_all()

        # Should return results for both items
        assert len(results) == 2

        # Find the invalid item result
        invalid_result = next(r for r in results if r["path"].endswith("invalid-item"))

        # Check that it was marked as invalid
        assert invalid_result["valid_stac"] is False
        # Should have an error type
        assert "error_type" in invalid_result
        # Should have an error message
        assert "error_message" in invalid_result


def test_item_collection_message_display(item_collection_url):
    """Test that item_collection_message correctly displays validation results."""
    linter = ApiLinter(
        source=item_collection_url,
        object_list_key="features",
        id_key="id",
        pages=1,
    )

    results = linter.lint_all()

    # Mock click.secho to verify it's called with the right arguments
    with mock.patch("stac_check.display_messages.click.secho") as mock_secho:
        item_collection_message(linter, results, cli_message_func=cli_message)

        # Verify that click.secho was called with expected title
        # The actual title in the code is "Item Collection: Validate all assets in a feature collection"
        mock_secho.assert_any_call(
            "Item Collection: Validate all assets in a feature collection", bold=True
        )
        # Verify that pages info was displayed - the format is "Pages = 1" not "Pages: 1"
        mock_secho.assert_any_call("Pages = 1")


def test_collections_message_display(collections_url):
    """Test that collections_message correctly displays validation results."""
    linter = ApiLinter(
        source=collections_url,
        object_list_key="collections",
        id_key="id",
        pages=1,
    )

    results = linter.lint_all()

    # Mock click.secho to verify it's called with the right arguments
    with mock.patch("stac_check.display_messages.click.secho") as mock_secho:
        collections_message(linter, results, cli_message_func=cli_message)

        # Verify that click.secho was called with expected title
        mock_secho.assert_any_call(
            "Collections: Validate all collections in a STAC API", bold=True
        )
        # Verify that pages info was displayed - the format is "Pages = 1" not "Pages: 1"
        mock_secho.assert_any_call("Pages = 1")


def test_api_linter_with_custom_id_key(collections_url):
    """Test ApiLinter with a custom ID key."""
    # Use a custom ID key
    linter = ApiLinter(
        source=collections_url,
        object_list_key="collections",
        id_key="custom_id",  # Non-standard ID key
        pages=1,
    )

    # Should still work even with a non-standard ID key
    results = linter.lint_all()
    assert len(results) > 0
