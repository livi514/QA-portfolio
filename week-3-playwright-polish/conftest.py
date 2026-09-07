import pytest
from pages.login_page import LoginPage
from test_data import VALID_USER


def perform_login(page):
    login = LoginPage(page)
    login.navigate()
    login.login(VALID_USER["username"], VALID_USER["password"])


@pytest.fixture
def log_in_to_saucedemo(page):
    perform_login(page)
    # Wait for navigation to inventory page
    page.wait_for_url("**/inventory.html", timeout=60000)
    page.locator("span.title").wait_for(state="visible", timeout=60000)
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
