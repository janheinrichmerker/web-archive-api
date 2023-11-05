[![PyPi](https://img.shields.io/pypi/v/web-archive-api?style=flat-square)](https://pypi.org/project/web-archive-api/)
[![CI](https://img.shields.io/github/actions/workflow/status/heinrichreimer/web-archive-api/ci.yml?branch=main&style=flat-square)](https://github.com/heinrichreimer/web-archive-api/actions/workflows/ci.yml)
[![Code coverage](https://img.shields.io/codecov/c/github/heinrichreimer/web-archive-api?style=flat-square)](https://codecov.io/github/heinrichreimer/web-archive-api/)
[![Python](https://img.shields.io/pypi/pyversions/web-archive-api?style=flat-square)](https://pypi.org/project/web-archive-api/)
[![Issues](https://img.shields.io/github/issues/heinrichreimer/web-archive-api?style=flat-square)](https://github.com/heinrichreimer/web-archive-api/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/heinrichreimer/web-archive-api?style=flat-square)](https://github.com/heinrichreimer/web-archive-api/commits)
[![Downloads](https://img.shields.io/pypi/dm/web-archive-api?style=flat-square)](https://pypi.org/project/web-archive-api/)
[![License](https://img.shields.io/github/license/heinrichreimer/web-archive-api?style=flat-square)](LICENSE)

# 🗃️ web-archive-api

Unified, type-safe access to web archive APIs.

## Installation
Install the package from PyPI:

```shell
pip install web-archive-api
```

## Usage
Web archives offer two main APIs: the [CDX API](#cdx-api) to list available captures and the [Memento API](#memento-api) to download individual captures.

### CDX API

TODO

### Memento API

TODO

## Development

To build this package and contribute to its development you need to install the `build`, and `setuptools` and `wheel` packages:

```shell
pip install build setuptools wheel
```

(On most systems, these packages are already pre-installed.)

### Installation

Install package and test dependencies:

```shell
pip install -e .[tests]
```

### Testing

Verify your changes against the test suite to verify.

```shell
flake8 web_archive_api  # Code format
mypy web_archive_api    # Static typing
pylint web_archive_api  # LINT errors
bandit -c pyproject.toml -r web_archive_api  # Security
pytest web_archive_api  # Unit tests
```

Please also add tests for your newly developed code.

### Build wheels

Wheels for this package can be built with:

```shell
python -m build
```

## Support

If you hit any problems using this package, please file an [issue](https://github.com/heinrichreimer/web-archive-api/issues/new).
We're happy to help!

## License

This repository is released under the [MIT license](LICENSE).
