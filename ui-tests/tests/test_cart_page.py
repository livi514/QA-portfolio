from playwright.sync_api import expect
import pytest

def test_empty_cart_state(page):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # click the cart button 
    page.locator(".shopping_cart_link").click()
    # check that no elements are visible in the cart
    cart_item = page.locator(".cart_item")
    expect(cart_item).to_have_count(0)

def test_add_item_to_cart(page):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # on the inventory page, click one of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    # click on the cart button 
    page.locator(".shopping_cart_link").click()
    # check number of items in the cart
    cart_item = page.locator(".cart_item")
    expect(cart_item).to_have_count(1)
    # check name of item
    inventory_item_name = page.locator(".inventory_item_name")
    expect(inventory_item_name).to_have_text("Sauce Labs Backpack")
    # check the text on the 'Remove' button
    expect(page.locator("[data-test='remove-sauce-labs-backpack']")).to_have_text("Remove")

def test_remove_item_from_cart(page):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # on the inventory page, click one of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    # click on the cart button
    page.locator(".shopping_cart_link").click()
    # click on the 'Remove' button
    page.locator("[data-test='remove-sauce-labs-backpack']").click()
    # check that the backpack no longer appears in the cart
    expect(page.locator(".cart_item")).to_have_count(0)

def test_removing_item_doesnt_affect_others(page):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # on the inventory page, click two of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    # click on the cart button
    page.locator(".shopping_cart_link").click()
    # check number of items in the cart
    cart_item = page.locator(".cart_item")
    expect(cart_item).to_have_count(2)
    # check name of items
    inventory_item_name = page.locator(".inventory_item_name")
    expect(inventory_item_name.nth(0)).to_have_text("Sauce Labs Backpack")
    expect(inventory_item_name.nth(1)).to_have_text("Sauce Labs Bike Light")
    # click on 'Remove' button for the backpack
    page.locator("[data-test='remove-sauce-labs-backpack']").click()
    # check that the backpack no longer appears in the cart
    expect(page.locator(".cart_item")).to_have_count(1)
    # check that the bike light still appears in the cart
    expect(page.locator(".inventory_item_name")).to_have_text("Sauce Labs Bike Light")

def test_continue_shopping_button(page):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # on the inventory page, click one of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    # click on the cart button
    page.locator(".shopping_cart_link").click()
    # click on the 'Continue Shopping' button
    page.locator("[data-test='continue-shopping']").click()
    # check that the inventory page is displayed
    expect(page.locator(".title")).to_have_text("Products")

def test_persistence_with_continue_shopping_button(page):
    # This test verifies that clicking the 'Continue Shopping' button does not remove items from the cart.
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # on the inventory page, click two of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    # click on the cart button
    page.locator(".shopping_cart_link").click()
    # check number of items in the cart
    cart_item = page.locator(".cart_item")
    expect(cart_item).to_have_count(2)
    # click on the 'Continue Shopping' button
    page.locator("[data-test='continue-shopping']").click()
    # click on the cart button again
    page.locator(".shopping_cart_link").click()
    # check that the items are still in the cart
    expect(page.locator(".cart_item")).to_have_count(2)
    # check names of items 
    inventory_item_name = page.locator(".inventory_item_name")
    expect(inventory_item_name.nth(0)).to_have_text("Sauce Labs Backpack")
    expect(inventory_item_name.nth(1)).to_have_text("Sauce Labs Bike Light")

def test_cart_persists_after_logout_and_login(page):
    # This test verifies that items in the cart persist after logging out and logging back in.
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # on the inventory page, click two of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    # click on the cart button
    page.locator(".shopping_cart_link").click()
    # check number of items in the cart
    cart_item = page.locator(".cart_item")
    expect(cart_item).to_have_count(2)
    # log out by clicking on the menu button and then clicking 'Logout'
    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()
    # log back in
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    # click on the cart button again
    page.locator(".shopping_cart_link").click()
    # check that the items are still in the cart
    expect(page.locator(".cart_item")).to_have_count(2)

def test_checkout_with_empty_cart(page):
    # saucedemo allows checkout with an empty cart — this documents that behaviour.
    # a bug report should be raised if this is not the intended behaviour.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # click on the cart button
    page.locator(".shopping_cart_link").click()
    # check that the cart is empty
    expect(page.locator(".cart_item")).to_have_count(0)
    # click on the 'Checkout' button
    page.locator("[data-test='checkout']").click()
    # check that the checkout page is displayed
    expect(page.locator(".title")).to_have_text("Checkout: Your Information")
    # fill in the checkout information
    page.locator("[data-test='firstName']").fill("John")
    page.locator("[data-test='lastName']").fill("Doe")
    page.locator("[data-test='postalCode']").fill("12345")
    # click on the 'Continue' button
    page.locator("[data-test='continue']").click()
    # check that the checkout overview page is displayed
    expect(page.locator(".title")).to_have_text("Checkout: Overview")
    # click on the 'Finish' button
    page.locator("[data-test='finish']").click()
    # check that the checkout complete page is displayed
    expect(page.locator(".title")).to_have_text("Checkout: Complete!")

def test_checkout_with_items(page):
    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # fill in the username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # on the inventory page, click one of the "Add to cart" buttons
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    # click on the cart button
    page.locator(".shopping_cart_link").click()
    # check number of items in the cart
    cart_item = page.locator(".cart_item")
    expect(cart_item).to_have_count(2)
    # click on the 'Checkout' button
    page.locator("[data-test='checkout']").click()
    # check that the checkout page is displayed
    expect(page.locator(".title")).to_have_text("Checkout: Your Information")
    # fill in the checkout information
    page.locator("[data-test='firstName']").fill("John")
    page.locator("[data-test='lastName']").fill("Doe")
    page.locator("[data-test='postalCode']").fill("12345")
    # click on the 'Continue' button
    page.locator("[data-test='continue']").click()
    # check that the checkout overview page is displayed
    expect(page.locator(".title")).to_have_text("Checkout: Overview")
    # check that the items are displayed on the checkout overview page
    expect(page.locator(".cart_item")).to_have_count(2)
    expect(page.locator(".inventory_item_name").nth(0)).to_have_text("Sauce Labs Backpack")
    expect(page.locator(".inventory_item_name").nth(1)).to_have_text("Sauce Labs Bike Light")
    # check item total and tax calculations
    item_total = page.locator(".summary_subtotal_label").text_content()
    tax = page.locator(".summary_tax_label").text_content()
    total = page.locator(".summary_total_label").text_content()
    # extract the numeric values from the text
    item_total_value = float(item_total.split("$")[1])
    tax_value = float(tax.split("$")[1])
    total_value = float(total.split("$")[1])
    # check that the total is equal to item total + tax
    assert total_value == item_total_value + tax_value
    # click on the 'Finish' button
    page.locator("[data-test='finish']").click()
    # check that the checkout complete page is displayed
    expect(page.locator(".title")).to_have_text("Checkout: Complete!")
    


    
