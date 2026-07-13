# Test Data Files

## What are test data files?

Test data files centralise the inputs used by your tests, keeping them separate from your test logic. Instead of hardcoding values directly in tests, you define them once in a dedicated file and import them wherever needed.

## Why use test data files?

- **Single source of truth:** if a value changes (e.g. a test account password), you update it in one place rather than hunting through every test file.
- **Readability:** named constants like `VALID_USER` are more meaningful than raw strings like `"standard_user"`.
- **Separation of concerns:** test logic describes *what* is being tested; test data describes *what values* are used. Keeping them separate makes both easier to understand and maintain.
- **Reusability:** the same data can be shared across multiple test files without duplication.

## Common formats

| Format | Best for |
|:-------|:---------|
| Python file (`.py`) | Simple constants and dictionaries; easiest to import |
| JSON (`.json`) | Structured data; language-agnostic |
| YAML (`.yaml`) | Structured data with a more readable syntax |
| CSV (`.csv`) | Large datasets, especially for parametrized tests |

## Example: Python test data file

```python
# test_data.py

VALID_USER = {
    "username": "standard_user",
    "password": "secret_sauce"
}

INVALID_USER = {
    "username": "invalid_user",
    "password": "invalid_password"
}

CHECKOUT_INFO = {
    "first_name": "John",
    "last_name": "Doe",
    "postal_code": "12345"
}
```

## Using test data in tests

```python
from test_data import VALID_USER, CHECKOUT_INFO

def test_login(page):
    page.locator("#user-name").fill(VALID_USER["username"])
    page.locator("#password").fill(VALID_USER["password"])
    page.locator("#login-button").click()
```

Named constants make the intent clear, for example, `VALID_USER` immediately communicates *why* these credentials are being used, unlike a raw string.

## What belongs in a test data file?

- Login credentials
- Form inputs (names, addresses, postal codes)
- Expected values used in assertions (error messages, page titles)
- URLs or endpoint paths
- Any value that appears in more than one test

## What does NOT belong in a test data file?

- Selectors or locators (those belong in page objects)
- Fixture logic (that belongs in `conftest.py`)
- Assertions or test logic
- Sensitive data like real passwords or API keys (use environment variables instead)

## Sensitive data: environment variables

For any data that shouldn't be committed to a public repository (e.g. real passwords, API keys, tokens), use environment variables instead of a test data file:

```python
import os

PASSWORD = os.environ.get("TEST_PASSWORD")
```

This keeps sensitive data out of your codebase entirely.
