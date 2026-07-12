# Test Configuration 

## Configuration file formats

Many pytest settings can be set in a configuration file, which by convention resides in the root directory of your repository (since this is a multi-week roadmap where each week is kept separate from the others, I've set up my configuration file in the week-3-playwright-polish directory).

A quick example of the configuration files supported by pytest:

### pytest.toml

`pytest.toml` files take precedence over other files, even when empty.

Alternatively, the hidden version `.pytest.toml` can be used.

```
# pytest.toml or .pytest.toml
[pytest]
minversion = "9.0"
addopts = ["-ra", "-q"]
testpaths = [
    "tests",
    "integration",
]
```

### pytest.ini

`pytest.ini` files take precedence over other files (except `pytest.toml` and `.pytest.toml`), even when empty.

Alternatively, the hidden version `.pytest.ini` can be used.

```
# pytest.ini or .pytest.ini
[pytest]
minversion = 6.0
addopts = -ra -q
testpaths =
    tests
    integration
```

### pyproject.toml

`pyproject.toml` files are supported for configuration.

```
# pyproject.toml
[tool.pytest]
minversion = "9.0"
addopts = ["-ra", "-q"]
testpaths = [
    "tests",
    "integration",
]
```

And many more file types!

### My choice:

I have chosen to use pyproject.toml as it's the modern statndard. Most Python projects use it as the single config file for everything (pytest, linting, packaging).

pytest.ini only handles pytest configuration, nothing else.

## Initialization: determining rootdir and configfile

pytest determines a `rootdir` for each test run which depends on the command line arguments (specified test files, paths), and on the existence of configuration files. The determined `rootdir` and `configfile` are printed as part of the pytest header during startup.

Here’s a summary of what pytest uses rootdir for:
- Construct nodeids during collection; each test is assigned a unique nodeid which is rooted at the rootdir and takes into account the full path, class name, function name and parametrization (if any).
- Is used by plugins as a stable location to store project/test run specific information; for example, the internal cache plugin creates a .pytest_cache subdirectory in rootdir to store its cross-test run state.

## Writing your `pyproject.toml`

`pyproject.toml` is a configuration file used by packaging tools, as well as other tools such as linters, type checkers, etc. There are three possible TOML tables in this file. 
- The [build-system] table is strongly recommended. It allows you to declare which build backend you use and which other dependencies are needed to build your project.
- The [project] table is the format that most build backends use to specify your project’s basic metadata, such as the dependencies, your name, etc.
- The [tool] table has tool-specific subtables, e.g., [tool.hatch], [tool.black], [tool.mypy]. 