## STAC-CHECK Change Log

All notable changes to this project will be documented in this file.

The format is (loosely) based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

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

[Unreleased]: https://github.com/stac-utils/stac-check/compare/v1.11.1...main
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
