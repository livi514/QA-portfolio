# Note: I copied the test cases from week 1, and decided to edit them to use fixtures instead of repeating the login steps in each test case.

from playwright.sync_api import expect
from conftest import perform_login

def test_empty_cart_state(log_in_to_saucedemo):
    # This test verifies that the cart is empty when the user first logs in.

    # click the cart button 
    log_in_to_saucedemo.locator(".shopping_cart_link").click()
    # check that no elements are visible in the cart
    cart_item = log_in_to_saucedemo.locator(".cart_item")
    expect(cart_item).to_have_count(0)

def test_add_item_to_cart(add_backpack_to_cart):
    # This test verifies that an item can be added to the cart and that the cart displays the correct information.

    # check number of items in the cart
    cart_item = add_backpack_to_cart.locator(".cart_item")
    expect(cart_item).to_have_count(1)
    # check name of item
    inventory_item_name = add_backpack_to_cart.locator(".inventory_item_name")
    expect(inventory_item_name).to_have_text("Sauce Labs Backpack")
    # check the text on the 'Remove' button
    expect(add_backpack_to_cart.locator("[data-test='remove-sauce-labs-backpack']")).to_have_text("Remove")

def test_remove_item_from_cart(add_backpack_to_cart):
    # This test verifies that an item can be removed from the cart and that the cart displays the correct information.

    # click on the 'Remove' button
    add_backpack_to_cart.locator("[data-test='remove-sauce-labs-backpack']").click()
    # check that the backpack no longer appears in the cart
    expect(add_backpack_to_cart.locator(".cart_item")).to_have_count(0)

def test_removing_item_doesnt_affect_others(add_backpack_and_bike_light_to_cart):
    # This test verifies that removing one item from the cart does not affect other items in the cart.

    # check number of items in the cart
    cart_item = add_backpack_and_bike_light_to_cart.locator(".cart_item")
    expect(cart_item).to_have_count(2)
    # check name of items
    inventory_item_name = add_backpack_and_bike_light_to_cart.locator(".inventory_item_name")
    expect(inventory_item_name.nth(0)).to_have_text("Sauce Labs Backpack")
    expect(inventory_item_name.nth(1)).to_have_text("Sauce Labs Bike Light")
    # click on 'Remove' button for the backpack
    add_backpack_and_bike_light_to_cart.locator("[data-test='remove-sauce-labs-backpack']").click()
    # check that the backpack no longer appears in the cart
    expect(add_backpack_and_bike_light_to_cart.locator(".cart_item")).to_have_count(1)
    # check that the bike light still appears in the cart
    expect(add_backpack_and_bike_light_to_cart.locator(".inventory_item_name")).to_have_text("Sauce Labs Bike Light")

def test_continue_shopping_button(add_backpack_to_cart):
    # This test verifies that clicking the 'Continue Shopping' button takes the user back to the inventory page.

    # click on the 'Continue Shopping' button
    add_backpack_to_cart.locator("[data-test='continue-shopping']").click()
    # check that the inventory page is displayed
    expect(add_backpack_to_cart.locator(".title")).to_have_text("Products")

def test_persistence_with_continue_shopping_button(add_backpack_and_bike_light_to_cart):
    # This test verifies that clicking the 'Continue Shopping' button does not remove items from the cart.

    # check number of items in the cart
    cart_item = add_backpack_and_bike_light_to_cart.locator(".cart_item")
    expect(cart_item).to_have_count(2)
    # click on the 'Continue Shopping' button
    add_backpack_and_bike_light_to_cart.locator("[data-test='continue-shopping']").click()
    # click on the cart button again
    add_backpack_and_bike_light_to_cart.locator(".shopping_cart_link").click()
    # check that the items are still in the cart
    expect(add_backpack_and_bike_light_to_cart.locator(".cart_item")).to_have_count(2)
    # check names of items 
    inventory_item_name = add_backpack_and_bike_light_to_cart.locator(".inventory_item_name")
    expect(inventory_item_name.nth(0)).to_have_text("Sauce Labs Backpack")
    expect(inventory_item_name.nth(1)).to_have_text("Sauce Labs Bike Light")

def test_cart_persists_after_logout_and_login(add_backpack_and_bike_light_to_cart):
    # This test verifies that items in the cart persist after logging out and logging back in.

    # check number of items in the cart
    cart_item = add_backpack_and_bike_light_to_cart.locator(".cart_item")
    expect(cart_item).to_have_count(2)
    # log out by clicking on the menu button and then clicking 'Logout'
    add_backpack_and_bike_light_to_cart.locator("#react-burger-menu-btn").click()
    add_backpack_and_bike_light_to_cart.locator("#logout_sidebar_link").click()
    # log back in
    perform_login(add_backpack_and_bike_light_to_cart)
    # click on the cart button again
    add_backpack_and_bike_light_to_cart.locator(".shopping_cart_link").click()
    # check that the items are still in the cart
    expect(add_backpack_and_bike_light_to_cart.locator(".cart_item")).to_have_count(2)
