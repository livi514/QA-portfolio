import re
from playwright.sync_api import expect
import pytest

def test_number_of_products(log_in_to_saucedemo):
    # This test checks that the inventory page renders with the expected number of inventory items (6).

    # assert that there are 6 products on the inventory page
    expect(log_in_to_saucedemo.locator(".inventory_item")).to_have_count(6)

def test_add_and_remove_item_from_cart(log_in_to_saucedemo):
    # on the inventory page, click one of the "Add to cart" buttons
    log_in_to_saucedemo.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    # number of items in cart should equal 1
    expect(log_in_to_saucedemo.locator(".shopping_cart_badge")).to_have_text("1")
    expect(log_in_to_saucedemo.locator("[data-test='remove-sauce-labs-backpack']")).to_have_text("Remove")
    # remove item from cart
    log_in_to_saucedemo.locator("[data-test='remove-sauce-labs-backpack']").click()
    # check that the cart badge disappears
    expect(log_in_to_saucedemo.locator(".shopping_cart_badge")).not_to_be_visible()
    # check that the text on the button updates to "Add to cart"
    expect(log_in_to_saucedemo.locator("[data-test='add-to-cart-sauce-labs-backpack']")).to_have_text("Add to cart")

def test_add_two_items_to_cart(log_in_to_saucedemo):   
    # add backpack to cart
    log_in_to_saucedemo.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    # add bike light to cart
    log_in_to_saucedemo.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    # number of items in cart should equal 2
    expect(log_in_to_saucedemo.locator(".shopping_cart_badge")).to_have_text("2")
    # backpack and bike light buttons should have "Remove" text
    expect(log_in_to_saucedemo.locator("[data-test='remove-sauce-labs-backpack']")).to_have_text("Remove")
    expect(log_in_to_saucedemo.locator("[data-test='remove-sauce-labs-bike-light']")).to_have_text("Remove")

@pytest.mark.parametrize("sort_value, expected_order", [
    ("az", "ascending"),
    ("za", "descending"),
])

def test_sort_by_name(log_in_to_saucedemo, sort_value, expected_order):
    # select ordering
    log_in_to_saucedemo.locator(".product_sort_container").select_option(sort_value)
    # check ordering
    names = log_in_to_saucedemo.locator(".inventory_item_name").all_text_contents()
    if expected_order == "ascending":
        assert names == sorted(names)
    else:
        assert names == sorted(names, reverse=True)

@pytest.mark.parametrize("sort_value, expected_order", [
    ("lohi", "ascending"),
    ("hilo", "descending")
])

def test_sort_by_price(log_in_to_saucedemo, sort_value, expected_order):
    # select ordering
    log_in_to_saucedemo.locator(".product_sort_container").select_option(sort_value)
    # check ordering
    raw_prices = log_in_to_saucedemo.locator(".inventory_item_price").all_text_contents()
    prices = [float(price_text.replace("$", "")) for price_text in raw_prices]
    if (expected_order == "ascending"):
        assert prices == sorted(prices)
    else:
        assert prices == sorted(prices, reverse=True)

def test_url_after_clicking_cart(log_in_to_saucedemo):
    # This test checks that the user is redirected to the expected page (cart) after clicking the cart button.

    # click the cart button 
    log_in_to_saucedemo.locator(".shopping_cart_link").click()
    expect(log_in_to_saucedemo).to_have_url(re.compile("cart"))
