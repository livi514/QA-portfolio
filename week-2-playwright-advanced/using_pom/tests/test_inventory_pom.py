import re

import pytest
from playwright.sync_api import expect
from using_pom.pages.inventory_page import InventoryPage

# Inventory page baseline checks


def test_pom_inventory_page_title(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    expect(inventory.title).to_have_text("Products")


def test_pom_cart_icon_visible(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    expect(inventory.cart_icon).to_be_visible()


def test_pom_number_of_products(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    expect(inventory.product_names).to_have_count(6)


def test_pom_sort_dropdown_visible(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    expect(inventory.sort_dropdown).to_be_visible()


def test_pom_sort_dropdown_options(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    expect(inventory.sort_dropdown).to_have_text(
        "Name (A to Z)Name (Z to A)Price (low to high)Price (high to low)"
    )


def test_pom_sort_dropdown_default_value(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    expect(inventory.sort_dropdown).to_have_value("az")


def test_pom_cart_badge_not_visible(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    expect(inventory.cart_badge).not_to_be_visible()


def test_pom_product_names_visible(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    inventory.are_product_names_visible()


def test_pom_product_prices_visible(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    inventory.are_product_prices_visible()


# Adding and removing items from cart


def test_pom_add_and_remove_item_from_cart(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    inventory.add_backpack()
    expect(inventory.cart_badge).to_have_text("1")
    expect(inventory.backpack_remove_button).to_have_text("Remove")
    inventory.remove_backpack()
    expect(inventory.cart_badge).not_to_be_visible()
    expect(inventory.backpack_add_button).to_have_text("Add to cart")


def test_pom_add_two_items_to_cart(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    inventory.add_backpack()
    inventory.add_bike_light()
    expect(inventory.cart_badge).to_have_text("2")
    expect(inventory.backpack_remove_button).to_have_text("Remove")
    expect(inventory.bike_light_remove_button).to_have_text("Remove")


# Sorting tests


@pytest.mark.parametrize(
    "sort_value, expected_order",
    [
        ("az", "ascending"),
        ("za", "descending"),
    ],
)
def test_pom_sort_by_name(log_in_to_saucedemo, sort_value, expected_order):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    inventory.sort_by(sort_value)
    names = inventory.get_product_names()
    if expected_order == "ascending":
        assert names == sorted(names)
    else:
        assert names == sorted(names, reverse=True)


@pytest.mark.parametrize(
    "sort_value, expected_order", [("lohi", "ascending"), ("hilo", "descending")]
)
def test_pom_sort_by_price(log_in_to_saucedemo, sort_value, expected_order):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    inventory.sort_by(sort_value)
    raw_prices = inventory.get_product_prices()
    prices = [float(price.replace("$", "")) for price in raw_prices]
    if expected_order == "ascending":
        assert prices == sorted(prices)
    else:
        assert prices == sorted(prices, reverse=True)


# Navigation to cart page


def test_pom_url_after_clicking_cart(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    inventory.open_cart()
    expect(log_in_to_saucedemo).to_have_url(re.compile("cart"))
