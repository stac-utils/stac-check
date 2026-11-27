## STAC-CHECK Change Log

All notable changes to this project will be documented in this file.

The format is (loosely) based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

## [v2.0.0] - 2026-11-26

### Changed

- **Single validation engine**: the legacy `StacValidate` (jsonschema) engine has been removed; all validation now runs through `FastValidator` (fastjsonschema) from stac-valid. `validation_method`/`validator_engine` report `"stac-valid FastValidator"` and `error_type` reports `"FastValidationError"` instead of `"JSONSchemaValidationError"`
- `--fast` is redefined as "validation only": it skips linting and geometry checks for maximum speed in every mode
- Linting and geometry checks now run by default in every mode, including per object during `--recursive`
- `--max-depth` is now honored in recursive mode (objects at or beyond the limit are not validated); it was previously ignored in fast mode. Depth-capped objects are also no longer fetched at all — upstream previously prefetched every linked collection and its items pages before the cap was applied
- `--pydantic` is now backed by `stac-pydantic` directly via the `stac-check[pydantic]` extra rather than `stac-valid[pydantic]`
- Recursive display no longer re-fetches and re-validates every asset; per-asset linting runs on the documents already loaded during the walk, removing quadratic remote-fetch behavior on large catalogs
- Recursive validation of in-memory dictionaries validates only the document itself (child links cannot be resolved without a base path) and warns
- Local FeatureCollection files passed to `--collections`/`--item-collection` are always validated in a single batched pass; `--fast` only controls whether per-item linting runs
- STAC API `{"collections": [...]}` endpoint responses are now auto-detected like item collections, so `stac-check <url-or-file>` validates every collection without requiring `--collections`
- STAC API catalogs extension responses (`{"catalogs": [...]}`) are supported via auto-detection and a new `--catalogs` flag
- `--links`/`--assets` checks are implemented natively: relative link hrefs resolve against the document URL with proper `urljoin` semantics, requests are streamed with timeouts, and `--headers` are honored
- Validation messages no longer include `failed_schema`, `recommendation`, or `error_verbose`; the `errors` list carries `{error_message, affected_items, count}` entries instead
- Multi-asset modes (`--recursive`, `--collections`, `--item-collection`) now print a header and validation summary by default; per-asset detail requires `--verbose`. The summary's failed-asset list now includes each asset's error message, and geometry linting findings are flagged with a count of affected assets and a hint to re-run with `--verbose` for details. The summary also shows total and average-per-object validation timing in every multi-asset mode, not just `--fast`

### Removed

- Support for STAC versions older than 1.0.0: pre-1.0 documents now fail fast with a clear `UnsupportedVersionError` instead of a cryptic schema fetch error
- The `--fast-linting` CLI flag and `Linter`'s `fast_linting` parameter (linting is the default; use `--fast` to skip it), along with the `stac_check.fast_validator_wrapper` module (`validate_collection_fast` and `extract_schemas` moved to `stac_check.api_lint`)

### Fixed

- `--assets`/`--links` checks now run in every mode (they were silently skipped in fast mode)
- Malformed self/alternate links no longer fabricate bogus resolved URLs (e.g. `http://catalog/collection.json`) in link checks
- Local `{"collections": [...]}` files passed to `--collections` are validated per collection instead of being treated as a single object
- `--recursive` on remote STAC APIs now descends the whole API (root → `rel=data` collections → `rel=items` features) instead of validating only the landing page; local/catalog files keep the `child`/`item` walk. `rel="catalogs"` (catalogs extension) and `rel="collections"` links on catalogs are now traversed too, so sub-catalogs and their collections are reachable
- `--recursive` on remote APIs now follows `rel="next"` pagination on collections/items list responses — previously only the first page of each list was validated (stac-valid never follows `next`). `--pages` now also applies to `--recursive` as a per-list page cap (default one page per list, `--pages 0` for all pages), and a note is printed when a list is cut short by the cap. `--pages 0` now also means "all pages" for the `--collections`/`--item-collection`/`--catalogs` list modes, which previously had no way to follow every page
- Items extracted from remote `items` pages during `--recursive` now get linting, geometry checks, `--verbose` detail, and `--pydantic` re-validation like every other object — they were previously skipped because their synthetic `items-page#id` result paths had no loaded document to attach
- Recursive validation now prints live progress on stderr (objects validated, list pages being fetched) so long remote walks no longer appear frozen, and the summary's "Assets Checked" line shows a per-type breakdown (catalogs, collections, items)
- `--collections --fast` no longer crashes aggregating FastValidator's float timing fields, and uses the same compact fast-mode summary as `--item-collection --fast`
- `--item-collection` no longer reports objects as valid when validation fails at the file level (e.g. pre-1.0 STAC versions, load errors) — the failure message is applied to every item
- Missing files and non-JSON input now exit 1 with a clean error message instead of an unhandled traceback
- `--collections`/`--item-collection` no longer silently succeed validating nothing: a response containing the other list shape errors with a flag suggestion, an empty list warns that nothing was validated, and a bare STAC object passed to either flag is validated as itself
- Extension schemas declaring an older JSON Schema dialect (e.g. draft-07 schemas like Portolan using the tuple form of `items`) no longer crash validation: extension schemas are compiled by fastjsonschema under their own semantics instead of the legacy engine's hardcoded 2020-12 resolver ([#159](https://github.com/stac-utils/stac-check/issues/159))

## [v1.15.1] - 2026-11-26

### Fixed

- Fixed `--recursive` (non-fast) understating the assets checked when the run fails: `validate_all` now keeps every validated object instead of only the failures by enabling `trace_recursion` on `StacValidate` (its per-object JSON output is suppressed unless `--verbose` is passed)
- Fixed `--recursive` (non-fast) aborting the catalog walk at the first invalid `item` link; all linked objects are now validated and reported

### Updated

- Updated stac-valid dependency to >=4.6.4,<5

## [v1.15.0] - 2026-11-26

### Fixed

- Fixed fast mode (`--fast`) reporting objects as valid without validating them when linting dictionaries, e.g. `--fast` combined with `--collections` or `--item-collection` on remote endpoints
- Fixed tests hanging indefinitely by mocking `urlopen` in asset/link request tests
- Fixed `--recursive --fast` re-fetching and re-validating every asset while displaying results, negating the speedup on large catalogs
- Fixed `--headers` being ignored in fast mode; headers are now applied to FastValidator's HTTP session and forwarded to linter instances in `--collections`/`--item-collection --fast` mode
- Fixed `--recursive --fast` fetching and validating the root document twice; the recursive result is reused for the root message
- Fixed `--recursive --fast-linting` silently dropping linting and geometry checks; they now run per object on already-loaded documents
- Fixed pre-1.0 catalogs carrying a `license` field being misclassified as collections in `--recursive --fast`
- Fixed crash when displaying best practices in fallback result messages (`click.echo` called with `fg`)
- Fixed Dockerfile `CMD` pointing to a nonexistent `stac_check` executable (now `stac-check`) and added a `.dockerignore` so `COPY . .` skips `.venv`, `.git`, and build artifacts
- Fixed `--recursive --fast` showing a misleading empty summary when the root document fails to load
- Fixed `--recursive --fast` on remote catalogs: worked around upstream FastValidator bugs that mangled `https://` child URLs via `os.path.normpath` and rejected pre-1.0 documents lacking a `type` field
- Fixed `--fast` reporting an empty STAC version for file/URL inputs, always prompting to upgrade to version 1.1.0
- Fixed percent-encoded identifier check flagging non-Item objects whose ids contain `:`
- Fixed `--recursive` exiting 0 when only child objects fail validation; the exit code now reflects all validated objects

### Changed

- `--fast` now applies to `--recursive` validation via FastValidator (`--max-depth` is not supported in fast mode)
- `--fast-linting` now runs and displays geometry validation checks (previously they were computed but discarded); `--fast` still skips them for maximum performance
- Switched development workflow, CI, and Docker builds to `uv` with a committed `uv.lock`; the `docs` extra now requires Python >=3.11
- Docker image is now based on Python 3.12 so the `docs` extra installs, and `make docs` exits with a clear error on Python 3.10

### Updated

- Updated stac-valid dependency to >=4.6.2,<5

### Removed

- Support for Python 3.9

## [v1.14.0] - 2025-05-02

### Added

- Added `--fast-linting` flag for fast validation with best practices linting (skips geometry checks) ([#152](https://github.com/stac-utils/stac-check/pull/152))
- Pull request template ([#153](https://github.com/stac-utils/stac-check/pull/153))

## [v1.13.0] - 2026-04-29

### Added

- Support for stac-valid FastValidator validation method with --fast flag to validate items, item collections ([#150](https://github.com/stac-utils/stac-check/pull/150))

### Updated

- Updated publish script to use pyproject.toml instead of setup.py ([#149](https://github.com/stac-utils/stac-check/pull/149))

## [v1.12.0] - 2026-04-28

### Added

- Support for stac-validator v4 (pip install stac-valid~=4.2.0)([#143](https://github.com/stac-utils/stac-check/pull/143))
- pyproject.toml configuration file ([#143](https://github.com/stac-utils/stac-check/pull/143))
- Dependabot configuration for automated dependency updates ([#143](https://github.com/stac-utils/stac-check/pull/143))

### Changed

- Updated dependencies and build system to use pyproject.toml ([#143](https://github.com/stac-utils/stac-check/pull/143))
- Allowed automatic check for validating item collections without needing to specify --item-collection flag ([#143](https://github.com/stac-utils/stac-check/pull/143))

## [v1.11.1] - 2025-07-29

### Updated

- Updated stac-validator dependency to v3.10.1 ([#140](https://github.com/stac-utils/stac-check/pull/140))
- Updated Github Actions and documentation dependencies ([#139](https://github.com/stac-utils/stac-check/pull/139))

### Removed

- Removed pdoc-generated documentation files and references as the project now uses Sphinx exclusively for documentation. ([#141](https://github.com/stac-utils/stac-check/pull/141))

## [v1.11.0] - 2025-06-22

### Added

- Results summary for options that produce numerous results, ie. --collections, --item-collection, --recursive ([#138](https://github.com/stac-utils/stac-check/pull/138))
- Support for --verbose flag to show verbose results summary ([#138](https://github.com/stac-utils/stac-check/pull/138))
- Added `--output`/`-o` option to save validation results to a file ([#138](https://github.com/stac-utils/stac-check/pull/138))
- Tests for CLI options ([#138](https://github.com/stac-utils/stac-check/pull/138))

## [v1.10.1] - 2025-06-21

### Fixed

- Fixed issue where pages parameter was being added to the wrong Linter ([#137](https://github.com/stac-utils/stac-check/pull/137))

## [v1.10.0] - 2025-06-20

### Added

- Created api_lint.py module to handle API linting ([#135](https://github.com/stac-utils/stac-check/pull/135))
- Added support for --item-collection flag to validate item collection responses ([#135](https://github.com/stac-utils/stac-check/pull/135))
- Added support for --collections flag to validate collections responses ([#135](https://github.com/stac-utils/stac-check/pull/135))
- Added support for --pages flag to limit the number of pages to validate ([#135](https://github.com/stac-utils/stac-check/pull/135))


### Changed

- Refactored display messages into a dedicated module for better code organization and maintainability ([#135](https://github.com/stac-utils/stac-check/pull/135))
- Organized test files, added v1.0.0 recursion test ([#135](https://github.com/stac-utils/stac-check/pull/135))

## [v1.9.1] - 2025-06-16

### Added

- Added display of failed schema information in the validation output ([#134](https://github.com/stac-utils/stac-check/pull/134)) 
- Added recommendation messages to guide users when validation fails ([#134](https://github.com/stac-utils/stac-check/pull/134))
- Added disclaimer about schema-based STAC validation being an initial indicator of validity only ([#134](https://github.com/stac-utils/stac-check/pull/134))

### Changed

- Updated validation output to show "Passed" instead of "Valid" for accuracy ([#134](https://github.com/stac-utils/stac-check/pull/134))


## [v1.9.0] - 2025-06-13

### Added

- Added support for --verbose flag to show verbose error messages ([#132](https://github.com/stac-utils/stac-check/pull/132))

### Changed

- Updated stac-validator to v3.9.0 ([#132](https://github.com/stac-utils/stac-check/pull/132))
- Improved cli output, message formatting ([#132](https://github.com/stac-utils/stac-check/pull/132))

## [v1.8.0] - 2025-06-11

### Changed

- Made `stac-pydantic` an optional dependency ([#129](https://github.com/stac-utils/stac-check/pull/129))
  - `stac-validator` is now installed without the `[pydantic]` extra by default
  - Added `stac-check[pydantic]` extra for users who need pydantic validation
  - Added graceful fallback to JSONSchema validation when pydantic is not available
  - Updated tests to handle both scenarios (with and without pydantic installed)
  - Added helpful warning messages when pydantic is requested but not installed

- Migrated documentation from Read the Docs to GitHub Pages ([#128](https://github.com/stac-utils/stac-check/pull/128))
  - Updated documentation build system to use Sphinx with sphinx_rtd_theme
  - Added support for Markdown content in documentation using myst-parser
  - Updated README with instructions for building documentation locally
  - Added GitHub Actions workflow for automatic documentation deployment

## [v1.7.0] - 2025-06-01

### Added

- Added validation for bounding boxes that cross the antimeridian (180°/-180° longitude) ([#121](https://github.com/stac-utils/stac-check/pull/121))
  - Checks that bbox coordinates follow the GeoJSON specification for antimeridian crossing
  - Detects and reports cases where a bbox incorrectly "belts the globe" instead of properly crossing the antimeridian
  - Provides clear error messages to help users fix incorrectly formatted bboxes
- Added sponsors and supporters section with logos ([#122](https://github.com/stac-utils/stac-check/pull/122))
- Added check to verify that bbox matches item's polygon geometry ([#123](https://github.com/stac-utils/stac-check/pull/123))
- Added configuration documentation to README ([#124](https://github.com/stac-utils/stac-check/pull/124))
- Added validation for geometry coordinates order to detect potentially reversed lat/lon coordinates ([#125](https://github.com/stac-utils/stac-check/pull/125))
  - Checks that coordinates follow the GeoJSON specification with [longitude, latitude] order
  - Uses heuristics to identify coordinates that may be reversed or contain errors
  - Provides nuanced error messages acknowledging the uncertainty in coordinate validation
- Added validation for definite geometry coordinate errors ([#125](https://github.com/stac-utils/stac-check/pull/125))
  - Detects coordinates with latitude values exceeding ±90 degrees
  - Detects coordinates with longitude values exceeding ±180 degrees
  - Returns detailed information about invalid coordinates
- Added dedicated geometry validation configuration section ([#125](https://github.com/stac-utils/stac-check/pull/125))
  - Created a new `geometry_validation` section in the configuration file
  - Added a master enable/disable switch for all geometry validation checks
  - Reorganized geometry validation options into the new section
  - Separated geometry validation errors in CLI output with a [BETA] label
  - Added detailed documentation for geometry validation features
- Added `--pydantic` option for validating STAC objects using stac-pydantic models, providing enhanced type checking and validation ([#126](https://github.com/stac-utils/stac-check/pull/126))

### Enhanced

- Improved bbox validation output to show detailed information about mismatches between bbox and geometry bounds, including which specific coordinates differ and by how much ([#126](https://github.com/stac-utils/stac-check/pull/126))

### Fixed

- Fixed collection summaries check incorrectly showing messages for Item assets ([#121](https://github.com/stac-utils/stac-check/pull/127))

### Updated

- Improved README with table of contents, better formatting, stac-check logo, and enhanced documentation ([#122](https://github.com/stac-utils/stac-check/pull/122))
- Enhanced Contributing guidelines with step-by-step instructions ([#122](https://github.com/stac-utils/stac-check/pull/122))

### Removed 

- Support for Python 3.8 ([#121](https://github.com/stac-utils/stac-check/pull/121))

## [v1.6.0] - 2025-03-14

### Added

- Test for Python 3.13 in workflow ([#120](https://github.com/stac-utils/stac-check/pull/120))

### Fixed

- Prevented `KeyError` in `check_unlocated()` when `bbox` is unset ([#104](https://github.com/stac-utils/stac-check/pull/119))

### Updated

- Updated stac-validator to v3.6.0 ([#120](https://github.com/stac-utils/stac-check/pull/120))

## [v1.5.0] - 2025-01-17

### Added

- Allow to provide HTTP headers ([#114](https://github.com/stac-utils/stac-check/pull/114))
- Configure whether to open URLs when validating assets ([#114](https://github.com/stac-utils/stac-check/pull/114))

### Changed

- No longer use the deprecated pkg-resources package.
  It has been replaced with importlib from the Python standard library
  ([#112](https://github.com/stac-utils/stac-check/pull/112))

### Updated

- Updated stac-validator to v3.5.0 and other dependecies as well ([#116](https://github.com/stac-utils/stac-check/pull/116))

## [v1.4.0] - 2024-10-09

### Added

- Added pre-commit config ([#111](https://github.com/stac-utils/stac-check/pull/111))
- Added publish.yml to automatically publish new releases to PyPI ([#111](https://github.com/stac-utils/stac-check/pull/111))

### Changed

- Updated stac-validator dependency to ensure STAC v1.1.0 compliance ([#111](https://github.com/stac-utils/stac-check/pull/111))

## [v1.3.3] - 2023-11-17

### Changed

- Development dependencies removed from runtime dependency list
  ([#109](https://github.com/stac-utils/stac-check/pull/109))

## [v1.3.2] - 2023-03-23

### Added

- Ability to lint dictionaries https://github.com/stac-utils/stac-check/pull/94
- Docstrings and pdoc api documents

### Fixed

- Fixed the check_catalog_file_name() method to only work on static catalogs https://github.com/stac-utils/stac-check/pull/94
- Jsonschema version to use a released version https://github.com/stac-utils/stac-check/pull/105

## [v1.3.1] - 2022-10-05

### Changed

- Changed pin on stac-validator to >=3.1.0 from ==3.2.0

## [v1.3.0] - 2022-09-20

### Added

- recursive mode lints assets https://github.com/stac-utils/stac-check/pull/84

### Changed

- recursive mode swaps pystac for stac-validator https://github.com/stac-utils/stac-check/pull/84

### Fixed

- fix catalog file name check https://github.com/stac-utils/stac-check/pull/83

## [v1.2.0] - 2022-04-26

### Added

- Option to include a configuration file to ignore selected checks

### Changed

- Change name from stac_check to stac-check in setup for cli

### Fixed

- Fix thumbnail size check

## [v1.1.2] - 2022-03-03

### Changed

- Make it easier to export linting messages
- Set stac-validator version to 2.4.0

### Fixed

- Fix self-link test

## [v1.0.1] - 2022-02-20

### Changed

- Update readme
- Reorganized code for version 1.0.0 release

## [v0.2.0] - 2022-02-02 - 2022-02-19

### Added

- Import main validator as stac-validator was updated to 2.3.0
- Added best practices docuument to repo
- Recommend 'self' link in links
- Check catalogs and collections use 'catalog.json' or 'collection.json' as a file name
- Check that links in collections and catalogs have a title field
- Recommend that eo:bands or similar information is provided in collection summaries
- Check for small thumbnail image file type

## [v0.1.3] - 2022-01-23

### Added

- Check for bloated metadata, too many fields in properties
- Check for geometry field, recommend that STAC not be used for non-spatial data

### Changed

- Changed bloated links check to a boolean to mirror bloated metadata

## [v0.1.2] - 2022-01-17 - 2022-01-22

### Added

- Check for null datetime
- Check for unlocated items, bbox should be set to null if geometry is

## [v0.1.1] - 2021-11-26 - 2021-12-12

### Added

- Added github actions to test and push to pypi
- Added makefile, dockerfile

### Changed

- Removed pipenv

## [v0.1.0] - 2021-11-26 - 2021-12-05

### Added

- Best practices - searchable identifiers - lowercase, numbers, '\_' or '-'
  for id names
  https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#searchable-identifiers
- Best practices ensure item ids don't contain ':' or '/' characters
  https://github.com/radiantearth/stac-spec/blob/master/best-practices.md#item-ids
- Best practices check for item ids to see if they match file names
- Add url support, check for valid urls, validate urls
- Add pystac validate_all to new cli option -> recursive
- Update pystac from 0.5.6 to 1.1.0
- Move stac-validator 2.3.0 into repository
- Best practices check for too many links in object
- Best practices check for summaries in collections
- Validation from stac-validator 2.3.0
- Links and assets validation checks

[Unreleased]: https://github.com/stac-utils/stac-check/compare/v2.0.0...main
[v2.0.0]: https://github.com/stac-utils/stac-check/compare/v1.15.1...v2.0.0
[v1.15.1]: https://github.com/stac-utils/stac-check/compare/v1.15.0...v1.15.1
[v1.15.0]: https://github.com/stac-utils/stac-check/compare/v1.14.0...v1.15.0
[v1.14.0]: https://github.com/stac-utils/stac-check/compare/v1.13.0...v1.14.0
[v1.13.0]: https://github.com/stac-utils/stac-check/compare/v1.12.0...v1.13.0
[v1.12.0]: https://github.com/stac-utils/stac-check/compare/v1.11.1...v1.12.0
[v1.11.1]: https://github.com/stac-utils/stac-check/compare/v1.11.0...v1.11.1
[v1.11.0]: https://github.com/stac-utils/stac-check/compare/v1.10.1...v1.11.0
[v1.10.1]: https://github.com/stac-utils/stac-check/compare/v1.10.0...v1.10.1
[v1.10.0]: https://github.com/stac-utils/stac-check/compare/v1.9.1...v1.10.0
[v1.9.1]: https://github.com/stac-utils/stac-check/compare/v1.9.0...v1.9.1
[v1.9.0]: https://github.com/stac-utils/stac-check/compare/v1.8.0...v1.9.0
[v1.8.0]: https://github.com/stac-utils/stac-check/compare/v1.7.0...v1.8.0
[v1.7.0]: https://github.com/stac-utils/stac-check/compare/v1.6.0...v1.7.0
[v1.6.0]: https://github.com/stac-utils/stac-check/compare/v1.5.0...v1.6.0
[v1.5.0]: https://github.com/stac-utils/stac-check/compare/v1.4.0...v1.5.0
[v1.4.0]: https://github.com/stac-utils/stac-check/compare/v1.3.3...v1.4.0
[v1.3.3]: https://github.com/stac-utils/stac-check/compare/v1.3.2...v1.3.3
[v1.3.2]: https://github.com/stac-utils/stac-check/compare/v1.3.1...v1.3.2
[v1.3.1]: https://github.com/stac-utils/stac-check/compare/v1.3.0...v1.3.1
[v1.3.0]: https://github.com/stac-utils/stac-check/compare/v1.2.0...v1.3.0
[v1.2.0]: https://github.com/stac-utils/stac-check/compare/v1.1.2...v1.2.0
[v1.1.2]: https://github.com/stac-utils/stac-check/compare/v1.0.1...v1.1.2
[v1.0.1]: https://github.com/stac-utils/stac-check/compare/v0.2.0...v1.0.1
[v0.2.0]: https://github.com/stac-utils/stac-check/compare/v0.1.3...v0.2.0
[v0.1.3]: https://github.com/stac-utils/stac-check/compare/v0.1.2...v0.1.3
[v0.1.2]: https://github.com/stac-utils/stac-check/compare/v0.1.1...v0.1.2
[v0.1.1]: https://github.com/stac-utils/stac-check/compare/v0.1.0...v0.1.1
[v0.1.0]: https://github.com/stac-utils/stac-check/releases/tag/v0.1.0
