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

@pytest.fixture
def add_backpack_to_cart(log_in_to_saucedemo):
    page = log_in_to_saucedemo
    # on the inventory page, click one of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    # click on the cart button
    page.locator(".shopping_cart_link").click()
    return page

@pytest.fixture
def add_backpack_and_bike_light_to_cart(log_in_to_saucedemo):
    page = log_in_to_saucedemo
    # on the inventory page, click two of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    # click on the cart button
    page.locator(".shopping_cart_link").click()
    return page


