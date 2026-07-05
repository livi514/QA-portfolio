# conftest files are used for defining custom fixtures and hooks that can be shared across multiple test files in a test suite. They are automatically discovered by pytest and can be used to set up common test configurations, such as initializing the browser, logging in, or setting up test data.

import pytest

# for valid login credentials, we can create a fixture that performs the login steps and returns the logged-in page object. This fixture can then be used in multiple test cases that require a logged-in state.
def perform_login(page):
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

@pytest.fixture
def log_in_to_saucedemo(page):
    perform_login(page)
    return page
