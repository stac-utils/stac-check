## STAC-CHECK Change Log

All notable changes to this project will be documented in this file.

The format is (loosely) based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

### Added

- Added sponsors and supporters section with logos ([#122](https://github.com/stac-utils/stac-check/pull/122))
- Added check to verify that bbox matches item's polygon geometry ([#123](https://github.com/stac-utils/stac-check/pull/123))

### Updated

- Improved README with table of contents, better formatting, stac-check logo, and enhanced documentation ([#122](https://github.com/stac-utils/stac-check/pull/122))
- Enhanced Contributing guidelines with step-by-step instructions ([#122](https://github.com/stac-utils/stac-check/pull/122))

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

[Unreleased]: https://github.com/stac-utils/stac-check/compare/v1.6.0...main
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
