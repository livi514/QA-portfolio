from playwright.sync_api import expect
from using_pom.pages.inventory_page import InventoryPage
from using_pom.pages.cart_page import CartPage
from using_pom.pages.checkout_page import CheckoutPage

def test_checkout_with_empty_cart(log_in_to_saucedemo):
    # saucedemo allows checkout with an empty cart — this documents that behaviour.
    # a bug report should be raised if this is not the intended behaviour.

    # navigate to the inventory page
    inventory = InventoryPage(log_in_to_saucedemo)
    inventory.wait_until_loaded()
    # check that the cart is empty 
    assert inventory.get_cart_count() == 0
    # click on the 'Cart' icon
    inventory.cart_icon.click()
    cart = CartPage(log_in_to_saucedemo)
    # check that the cart page is displayed
    assert cart.get_title_text() == "Your Cart"
    # click on the 'Checkout' button
    cart.checkout_button.click()
    checkout = CheckoutPage(log_in_to_saucedemo)
    # check that the checkout page is displayed
    assert checkout.get_title_text() == "Checkout: Your Information"
    # fill in the checkout information
    checkout.fill_information("John", "Doe", "12345")
    # check that the checkout overview page is displayed
    assert checkout.get_title_text() == "Checkout: Overview"
    # click on the 'Finish' button
    checkout.finish_button.click()
    # check that the checkout complete page is displayed
    assert checkout.get_title_text() == "Checkout: Complete!"

def test_checkout_with_items(add_backpack_and_bike_light_to_cart):
    # This test verifies that the checkout process works correctly when items are in the cart.
    
    cart = CartPage(add_backpack_and_bike_light_to_cart)
    # check number of items in the cart
    assert cart.get_item_count() == 2
    # click on the 'Checkout' button
    cart.checkout_button.click()
    checkout = CheckoutPage(add_backpack_and_bike_light_to_cart)
    # check that the checkout page is displayed
    assert checkout.get_title_text() == "Checkout: Your Information"
    # fill in the checkout information
    checkout.fill_information("John", "Doe", "12345")
    # check that the checkout overview page is displayed
    assert checkout.get_title_text() == "Checkout: Overview"
    # check that the items are displayed on the checkout overview page
    assert checkout.get_cart_item_count() == 2
    assert checkout.get_item_names() == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    # check item total and tax calculations
    item_total = checkout.item_total_label.text_content()
    tax = checkout.tax_label.text_content()
    total = checkout.total_label.text_content()
    # extract the numeric values from the text
    item_total_value = float(item_total.split("$")[1])
    tax_value = float(tax.split("$")[1])
    total_value = float(total.split("$")[1])
    # check that the total is equal to item total + tax
    assert total_value == item_total_value + tax_value
    # click on the 'Finish' button
    checkout.finish_button.click()
    # check that the checkout complete page is displayed
    assert checkout.get_title_text() == "Checkout: Complete!"