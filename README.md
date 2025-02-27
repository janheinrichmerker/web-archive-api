[![PyPi](https://img.shields.io/pypi/v/web-archive-api?style=flat-square)](https://pypi.org/project/web-archive-api/)
[![CI](https://img.shields.io/github/actions/workflow/status/janheinrichmerker/web-archive-api/ci.yml?branch=main&style=flat-square)](https://github.com/janheinrichmerker/web-archive-api/actions/workflows/ci.yml)
[![Code coverage](https://img.shields.io/codecov/c/github/janheinrichmerker/web-archive-api?style=flat-square)](https://codecov.io/github/janheinrichmerker/web-archive-api/)
[![Python](https://img.shields.io/pypi/pyversions/web-archive-api?style=flat-square)](https://pypi.org/project/web-archive-api/)
[![Issues](https://img.shields.io/github/issues/janheinrichmerker/web-archive-api?style=flat-square)](https://github.com/janheinrichmerker/web-archive-api/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/janheinrichmerker/web-archive-api?style=flat-square)](https://github.com/janheinrichmerker/web-archive-api/commits)
[![Downloads](https://img.shields.io/pypi/dm/web-archive-api?style=flat-square)](https://pypi.org/project/web-archive-api/)
[![License](https://img.shields.io/github/license/janheinrichmerker/web-archive-api?style=flat-square)](LICENSE)

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

Then, install the package and test dependencies:

```shell
pip install -e .[tests]
```

You can now verify your changes against the test suite.

```shell
ruff check .                   # Code format and LINT
mypy .                         # Static typing
bandit -c pyproject.toml -r .  # Security
pytest .                       # Unit tests
```

Please also add tests for your newly developed code.

### Build wheels

Wheels for this package can be built with:

```shell
python -m build
```

## Support

If you hit any problems using this package, please file an [issue](https://github.com/janheinrichmerker/web-archive-api/issues/new).
We're happy to help!

## License

This repository is released under the [MIT license](LICENSE).
