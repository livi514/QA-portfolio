from playwright.sync_api import expect
from conftest import perform_login
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.menu_page import MenuPage
import pytest

@pytest.mark.smoke
def test_empty_cart_state(log_in_to_saucedemo):
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.open_cart()
    cart = CartPage(log_in_to_saucedemo)
    assert cart.get_item_count() == 0

def test_add_item_to_cart(add_backpack_to_cart):
    # This test verifies that an item can be added to the cart and that the cart displays the correct information.

    # check number of items in the cart
    cart = CartPage(add_backpack_to_cart)
    assert cart.get_item_count() == 1
    # check name of item
    assert cart.get_item_names()[0] == "Sauce Labs Backpack"
    # check the text on the 'Remove' button
    expect(cart.remove_backpack_button).to_have_text("Remove")

def test_remove_item_from_cart(add_backpack_to_cart):
    # This test verifies that an item can be removed from the cart and that the cart displays the correct information.

    # click on the 'Remove' button
    cart = CartPage(add_backpack_to_cart)
    cart.remove_backpack()
    # check that the backpack no longer appears in the cart
    assert cart.get_item_count() == 0

def test_removing_item_doesnt_affect_others(add_backpack_and_bike_light_to_cart):
    # This test verifies that removing one item from the cart does not affect other items in the cart.

    # check number of items in the cart
    cart = CartPage(add_backpack_and_bike_light_to_cart)
    assert cart.get_item_count() == 2
    # check name of items
    assert cart.get_item_names()[0] == "Sauce Labs Backpack"
    assert cart.get_item_names()[1] == "Sauce Labs Bike Light"
    # click on 'Remove' button for the backpack
    cart.remove_backpack()
    # check that the backpack no longer appears in the cart
    assert cart.get_item_count() == 1
    # check that the bike light still appears in the cart
    assert cart.get_item_names()[0] == "Sauce Labs Bike Light"

def test_continue_shopping_button(add_backpack_to_cart):
    # This test verifies that clicking the 'Continue Shopping' button takes the user back to the inventory page.

    cart = CartPage(add_backpack_to_cart)
    # click on the 'Continue Shopping' button
    cart.continue_shopping()
    # check that the inventory page is displayed
    inventory = InventoryPage(add_backpack_to_cart)
    expect(inventory.title).to_have_text("Products")

def test_persistence_with_continue_shopping_button(add_backpack_and_bike_light_to_cart):
    # This test verifies that clicking the 'Continue Shopping' button does not remove items from the cart.

    cart = CartPage(add_backpack_and_bike_light_to_cart)
    # check number of items in the cart
    assert cart.get_item_count() == 2
    # click on the 'Continue Shopping' button
    cart.continue_shopping()
    # click on the cart button again
    inventory = InventoryPage(add_backpack_and_bike_light_to_cart)
    inventory.open_cart()
    # check that the items are still in the cart
    assert cart.get_item_count() == 2
    # check names of items
    assert cart.get_item_names()[0] == "Sauce Labs Backpack"
    assert cart.get_item_names()[1] == "Sauce Labs Bike Light"

def test_cart_persists_after_logout_and_login(add_backpack_and_bike_light_to_cart):
    # This test verifies that items in the cart persist after logging out and logging back in.

    cart = CartPage(add_backpack_and_bike_light_to_cart)
    # check number of items in the cart
    assert cart.get_item_count() == 2
    # log out by clicking on the menu button and then clicking 'Logout'
    menu = MenuPage(add_backpack_and_bike_light_to_cart)
    menu.open_menu()
    menu.logout()
    # log back in
    perform_login(add_backpack_and_bike_light_to_cart)
    # click on the cart button again
    inventory = InventoryPage(add_backpack_and_bike_light_to_cart)
    inventory.open_cart()
    # check that the items are still in the cart
    assert cart.get_item_count() == 2
