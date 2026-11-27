from unittest import mock

from stac_check.lint import Linter


def _fake_get(url, headers=None, *args, **kwargs):
    """Simulate stac_check's native href checks: succeed for reachable
    hosts, fail otherwise."""
    if "storage.googleapis.com" in url:
        return 200
    raise OSError(f"Simulated network failure for {url}")


@mock.patch("stac_check.lint._http_head_status", side_effect=_fake_get)
def test_lint_assets_no_links(mock_get):
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file, assets=True, assets_open_urls=False)
    assert linter.message["version"] == "1.0.0"
    assert linter.message["path"] == file
    assert linter.message["valid_stac"] is True
    assert linter.message["validation_method"] == "stac-valid FastValidator"
    assert linter.message["assets_validated"] == {
        "format_valid": [
            "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic.tif",
            "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
            "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.tif",
            "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic_udm.tif",
            "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
            "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
        ],
        "format_invalid": [],
        "request_valid": [],
        "request_invalid": [],
    }


@mock.patch("stac_check.lint._http_head_status", side_effect=_fake_get)
def test_linter_bad_assets(mock_get):
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file, assets=True)
    asset_format_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg"
    ]
    asset_request_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
        "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
        "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
    ]
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert linter.invalid_asset_format == asset_format_errors
    assert linter.invalid_asset_request == asset_request_errors


@mock.patch("stac_check.lint._http_head_status", side_effect=_fake_get)
def test_linter_bad_links(mock_get):
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file, links=True)
    link_format_errors = ["http:/remotdata.io/catalog/20201211_223832_CS2/index.html"]
    # Relative link hrefs can't be resolved (the self/alternate link is
    # malformed) and are filtered out of the http-only display list; the
    # bogus "http://catalog/..." origin upstream fabricated is gone.
    link_request_errors = [
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html",
    ]
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert len(linter.invalid_link_format) > 0
    assert linter.invalid_link_format == link_format_errors
    assert linter.invalid_link_request == link_request_errors


@mock.patch("stac_check.lint._http_head_status", side_effect=_fake_get)
def test_linter_bad_links_assets(mock_get):
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file, assets=True, links=True)
    asset_format_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg"
    ]
    asset_request_errors = [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
        "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
        "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
    ]
    link_format_errors = [
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html",
    ]
    link_request_errors = [
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html",
    ]
    assert linter.version == "1.0.0"
    assert linter.valid_stac == True
    assert linter.asset_type == "ITEM"
    assert len(linter.invalid_link_format) > 0
    assert linter.invalid_asset_format == asset_format_errors
    assert linter.invalid_asset_request == asset_request_errors
    assert linter.invalid_link_format == link_format_errors
    assert linter.invalid_link_request == link_request_errors


@mock.patch("stac_check.lint._http_head_status", side_effect=_fake_get)
def test_linter_bad_links_assets_fast(mock_get):
    """--fast surfaces invalid assets/links too; the checks are
    engine-independent and no longer silently skipped."""
    file = "sample_files/1.0.0/core-item-bad-links.json"
    linter = Linter(file, assets=True, links=True, fast=True)
    assert linter.invalid_asset_format == [
        "https:/storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg"
    ]
    assert linter.invalid_link_format == [
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html"
    ]
    assert linter.invalid_link_request == [
        "http:/remotdata.io/catalog/20201211_223832_CS2/index.html"
    ]
