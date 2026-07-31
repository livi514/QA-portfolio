# QA Summer Roadmap - Week 3

## Introduction

Week 3 of my QA Roadmap was about making my tests production-ready. After two weeks of learning how to write and structure tests, this week shifted the focus from "does this pass?" to "can this be maintained?".

## What I did this week

Rather than adding new tests, this week was about polishing what I already had and setting things up properly.

I started with test configuration, setting up a `pyproject.toml` file to centralise settings like the base URL, number of parallel workers, and browser configuration. Previously these were either hardcoded or passed manually as CLI flags, and now they live in one place.

I also created a test data file (`test_data.py`) to centralise credentials, form inputs, and expected error messages. If any of these values change, there's now one place to update them rather than hunting through every test file.

Finally, I created a public repository for the saucedemo test suite, which brings together everything from weeks 1, 2, and 3. Getting it ready to share involved commenting every test with docstrings and Arrange → Act → Assert structure, writing a README and CONTRIBUTING.md, and setting up linting with pre-commit hooks.

## What I learned

### Test configuration

A `pyproject.toml` file lets you centralise pytest settings so they apply automatically on every run. The key options I configured were `testpaths`, `addopts` (browsers, parallel workers, base URL), and custom markers.

Using a base URL means tests use relative paths like `page.goto("/")` instead of hardcoding the full URL everywhere, so switching environments only requires changing one value.

### Test data files

Hardcoding test inputs directly in tests creates the same problem as hardcoding selectors: one change in the application means hunting through every test file. A test data file creates a single source of truth for inputs, the same way page objects do for selectors.

### What doesn't belong in a test data file

Selectors belong in page objects. Fixture logic belongs in `conftest.py`. Sensitive data like real passwords or API keys belongs in environment variables, not in a committed file.

## Key takeaway

The theme of week 3 was centralisation: configuration in one place, test data in one place, and a repo structured so that anyone can clone it and understand it without asking me anything. That's what makes a test suite maintainable rather than just functional.

## How to run the tests

For full setup and installation instructions, see the main [README](../README.md).

Ensure you are running commands from the `week-3-playwright-polish` folder. 

Use `cd week-3-playwright-polish` to navigate to the folder if necessary.

Run all tests:
```
pytest
```

Run smoke tests only:
```
pytest -m smoke
```

Run a specific test file:
```
pytest tests/test_login_pom.py
```

Run in headed mode (useful for debugging):
```
pytest --headed
```