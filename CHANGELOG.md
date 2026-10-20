# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI: test matrix over Python 3.9–3.13, distribution build
  check, and an advisory lint job
- Publication to PyPI via trusted publishing on `v*` tags, with a TestPyPI
  dry run available from the Actions tab; a GitHub release is created with
  the sdist and wheel attached
- Project URLs and keywords in the package metadata

### Changed
- Version is now read from `paleodatetime.__version__` only (previously
  duplicated in `pyproject.toml`)
- License declared as an SPDX expression; `setuptools>=77` required to build
- Ruff configuration moved to the `[tool.ruff.lint]` table

## [0.1.0] - 2026-01-21

### Added
- Initial release of PaleoDateTime library
- `PaleoDateTime` class for representing dates on geological timescales
  - Support for dates spanning millions of years (negative and positive)
  - Second-level precision (no microseconds/nanoseconds)
  - Datetime-like API compatible with Python's datetime conventions
  - ISO 8601-like formatting and parsing
  - Arithmetic operations (addition, subtraction with timedeltas)
  - Comparison operations (equality, ordering)
  - Leap year calculations using astronomical year numbering

- `PaleoTimeDelta` class for representing durations
  - Support for years, months, days, hours, minutes, seconds
  - Arithmetic operations (addition, subtraction, multiplication, division)
  - Comparison operations
  - String representations

- Custom exception classes
  - `PaleoDateTimeError` - Base exception
  - `PaleoDateTimeValueError` - Invalid values
  - `PaleoDateTimeFormatError` - Invalid format strings

- Comprehensive test suite with 93 tests
  - Unit tests for PaleoDateTime
  - Unit tests for PaleoTimeDelta
  - Integration tests for geological scenarios
  - Edge case testing

- Documentation and examples
  - Complete README with usage examples
  - Basic usage example script
  - Geological timescale example with mass extinctions

- Development tooling
  - Pixi configuration for package management
  - Pytest for testing
  - Black and Ruff for code formatting
  - MIT License

### Design Decisions
- Uses astronomical year numbering where year 0 exists and equals 1 BCE
- Maximum precision limited to seconds (sufficient for geological timescales)
- Proleptic Gregorian calendar for all date calculations
- No timezone support (geological time is absolute)
- Pure Python implementation with no external dependencies
