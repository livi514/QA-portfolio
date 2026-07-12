# Test Configuration

## Configuration file formats

Many pytest settings can be set in a configuration file, which by convention resides in the root directory of your repository. Since this is a multi-week roadmap where each week is kept self-contained, I've placed my configuration file in the `week-3-playwright-polish` directory.

pytest supports several configuration file formats:

### `pytest.ini`

Takes precedence over other files (except `pyproject.toml`), even when empty. Only handles pytest configuration, nothing else.

```ini
# pytest.ini
[pytest]
minversion = 6.0
addopts = -ra -q
testpaths =
    tests
    integration
```

### `pyproject.toml`

The modern standard. Most Python projects use it as a single config file for everything: pytest, linting, packaging, and more. All pytest options go under `[tool.pytest.ini_options]`.

```toml
# pyproject.toml
[tool.pytest.ini_options]
minversion = "9.0"
addopts = ["-ra", "-q"]
testpaths = [
    "tests",
    "integration",
]
```

### Other supported formats

pytest also supports `tox.ini` and `setup.cfg`, though these are less common in modern projects.

### My choice: `pyproject.toml`

I chose `pyproject.toml` because it's the modern standard. It handles pytest configuration alongside any other tooling (linters, type checkers, etc.) in one place, while `pytest.ini` is more limited as it only handles pytest.

## Initialization: rootdir and configfile

pytest determines a `rootdir` for each test run based on the command line arguments and the location of the configuration file. Both are printed in the pytest header at startup.

pytest uses `rootdir` for two main purposes:

- **Constructing nodeids** — each test is assigned a unique identifier rooted at `rootdir`, including its full path, class name, function name, and parametrization.
- **Plugin storage** — plugins use `rootdir` as a stable location for test run state. For example, the cache plugin creates a `.pytest_cache` subdirectory here.


## Structure of `pyproject.toml`

`pyproject.toml` supports three top-level TOML tables:

- **`[build-system]`** — declares which build backend to use and its dependencies.
- **`[project]`** — specifies basic project metadata such as name, version, and dependencies.
- **`[tool]`** — contains tool-specific subtables, e.g. `[tool.pytest.ini_options]`, `[tool.black]`, `[tool.mypy]`.

## My `pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--browser chromium --browser firefox --browser webkit -2 auto --base-url https://www.saucedemo.com"
markers = [
    "smoke: quick baseline checks",
    "regression: full test suite",
]
```

**`testpaths`**  tells pytest where to look for tests. Without this, pytest searches the entire directory, which is slower and can pick up unwanted files.

**`addopts`**  - additional command line options applied automatically on every run:
- `--browser chromium/firefox/webkit` runs tests across all three browsers
- `-n auto` enables parallel execution using all available CPU cores (requires `pytest-xdist`)
- `--base-url` sets the base URL so tests can use relative paths like `page.goto("/")` instead of hardcoding the full URL everywhere

**`markers`** declares custom markers to avoid pytest warnings and documents their purpose.

## Test Markers

Markers allow you to tag tests so you can run specific subsets on demand.

### My marker: `smoke`

Smoke tests are quick baseline checks that verify the site is up and rendering correctly before running the full suite. They cover things like page load, element visibility, and correct titles — nothing that requires complex user interactions.

```toml
markers = [
    "smoke: quick baseline checks that verify the site is up and rendering correctly",
]
```

Apply a marker to a test like this:

```python
@pytest.mark.smoke
def test_page_title(page):
    page.goto("/")
    expect(page).to_have_title("Swag Labs")
```

### Running tests by marker

```
pytest -m smoke       # run only smoke tests (fast baseline check)
pytest                # run everything (full suite including smoke tests)
```

### Why not a `regression` marker?

A common mistake is marking all non-smoke tests as `regression`. But `regression` typically means "verify existing functionality hasn't broken", which is what running the full suite already does. Adding a `regression` marker is redundant because `pytest` with no flags runs everything anyway.

The useful distinction is between:
- **A fast subset** (smoke): run this first to catch obvious failures quickly
- **The full suite** (default): run this for thorough coverage
