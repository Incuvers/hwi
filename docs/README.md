# Documentation

Modified: 2021-11

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