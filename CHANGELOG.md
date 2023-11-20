# Changelog

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
