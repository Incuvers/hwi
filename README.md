# IRIS Hardware Interface
[![ci](https://github.com/Incuvers/hwi/actions/workflows/ci.yml/badge.svg)](https://github.com/Incuvers/hwi/actions/workflows/ci.yml)
[![deploy](https://github.com/Incuvers/hwi/actions/workflows/image.yml/badge.svg)](https://github.com/Incuvers/hwi/actions/workflows/image.yml)
![img](/docs/img/Incuvers-black.png)

Updated: 2021-11

## Navigation
1. [Quickstart](#quickstart)
2. [Developer Team](#development-team)
3. [Licence](#license)

## Quickstart
This repository is built and controlled using the Makefile in the root in order to homogenize our dev environments. Run `make help` for more information on the available make targets. The source is intended to be built and developed on Ubuntu 20.04 or higher ARM64 systems.

Install `docker`, `docker-compose` and setup user permissions
```bash
sudo apt install docker.io docker-compose
sudo groupadd docker
sudo usermod -aG docker $USER
sudo reboot
```

### Authentication
Create a `.env` file from the sample env file
```bash
cp sample.env .env
```

### Docker Environment
Build the services for local development. Local source code is mounted to the `hwi` container for rapid development:
```bash
make dev
```

### Python Module
Or run the python module directly:
```bash
python3 -m hwi
```

### Unittest and Coverage
```bash
make unit
```
Unittest suite for the `monitor` app is located [here](/monitor/tests). This target uses unittest discovery to run the entire test suite. Alternatively you can execute a single test case by referencing the test case name:
```bash
make unit case=<NAME>
```
Where `<NAME>` is the name of the test case by its filename schema: `test_<NAME>.py`. For example the `<NAME>` of `test_cache.py` would be `cache`.

Code Coverage can be performed on the entire unittest suite:
```bash
make coverage
```
or by referencing a specific test case module:
```bash
make coverage case=<NAME>
```
Where `<NAME>` is the name of the test case by its filename schema: `test_<NAME>.py`. For example the `<NAME>` of `test_cache.py` would be `cache`. A cli code coverage report will be generated displaying the coverage per file as well as the lines which have not been covered. The coverage configuration for monitor can be found in the [.coveragerc](/.coveragerc) in root.

### Linting
```bash
make lint
```
This target requires `yamllint` (all `.yaml` files), `shellcheck` (binaries located under `bin/`)and `flake8` (python app codebase) to be installed and in your `$PATH`. The `yamllint` and `flake8` configuration for monitor can be found in the [.yamllint](/.yamllint) and [.flake8](/.flake8) in root respectively.

## Development Team
David Sean (CTO) (david@incuvers.com)\
Christian Sargusingh (christian@incuvers.com)

## Licence
Copyright © 2021 Incuvers Inc
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential
