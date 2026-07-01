from playwright.sync_api import expect
import pytest

def test_add_and_remove_item_from_cart(page):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # on the inventory page, click one of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    # number of items in cart should equal 1
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
    expect(page.locator("[data-test='remove-sauce-labs-backpack']")).to_have_text("Remove")
    # remove item from cart
    page.locator("[data-test='remove-sauce-labs-backpack']").click()
    # check that the cart badge disappears
    expect(page.locator(".shopping_cart_badge")).not_to_be_visible()
    # check that the text on the button updates to "Add to cart"
    expect(page.locator("[data-test='add-to-cart-sauce-labs-backpack']")).to_have_text("Add to cart")

def test_add_two_items_to_cart(page):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # add backpack to cart
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    # add bike light to cart
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    # number of items in cart should equal 2
    expect(page.locator(".shopping_cart_badge")).to_have_text("2")
    # backpack and bike light buttons should have "Remove" text
    expect(page.locator("[data-test='remove-sauce-labs-backpack']")).to_have_text("Remove")
    expect(page.locator("[data-test='remove-sauce-labs-bike-light']")).to_have_text("Remove")

@pytest.mark.parametrize("sort_value, expected_order", [
    ("az", "ascending"),
    ("za", "descending"),
])

def test_sort_by_name(page, sort_value, expected_order):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # select ordering
    page.locator(".product_sort_container").select_option(sort_value)
    # check ordering
    names = page.locator(".inventory_item_name").all_text_contents()
    if expected_order == "ascending":
        assert names == sorted(names)
    else:
        assert names == sorted(names, reverse=True)

@pytest.mark.parametrize("sort_value, expected_order", [
    ("lohi", "ascending"),
    ("hilo", "descending")
])

def test_sort_by_price(page, sort_value, expected_order):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # select ordering
    page.locator(".product_sort_container").select_option(sort_value)
    # check ordering
    raw_prices = page.locator(".inventory_item_price").all_text_contents()
    prices = [float(price_text.replace("$", "")) for price_text in raw_prices]
    if (expected_order == "ascending"):
        assert prices == sorted(prices)
    else:
        assert prices == sorted(prices, reverse=True)


