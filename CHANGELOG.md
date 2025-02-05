# Changelog


## [1.3.0] - 2024-02-05

### Changed
- Dropped support for Python 3.8 and 3.9
- Added support for Python 3.12

### Fixed
- Fixed issue where `partial_json` modifications were mutating the class-level `default_json` attribute in `MockAPIResponse`, causing unexpected behavior in tests.

## [1.2.1] - 2024-05-22

### Changed
- Fix support for default json response in `MockAPIResponse`.

## [1.2.1] - 2024-05-22

### Added
- Support for handling exceptions in the mock API responses for `httpx`.

### Changed
- Supporting both class and instance types for `default_exc` in `MockAPIResponse`.

## [1.2.0] - 2024-03-11

### Added
- Added support for `httpx`.
- Deprecated `setup_api_mocks` fixture in favor of the new `setup_http_mocks`.

## [1.1.0] - 2023-11-20

### Added
- Implementing matchers in the MockSet class to enhance the tracking and management of multiple mock responses in tests.


## [1.0.0] - 2023-11-08

### Added
- Initial release of `multi_api_mocker`.
- Core functionality for creating and managing mock API responses with `MockAPIResponse` class.
- `MockSet` class for efficient access and management of multiple mock responses.
- Pytest fixture `setup_api_mocks` for easy integration and setup of mock responses in tests.
- Example subclasses for common API interactions such as `Commit`, `Fork`, `Push`, and `ForcePush`.
- Comprehensive test suite demonstrating usage of the library in various scenarios.
- Documentation for each component, detailing usage, examples, and integration steps.
- GitHub Actions workflow for automated testing and PyPI deployment.
- Pre-commit hooks configuration for code formatting and linting.
