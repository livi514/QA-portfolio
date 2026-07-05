from playwright.sync_api import expect

def test_checkout_with_empty_cart(log_in_to_saucedemo):
    # saucedemo allows checkout with an empty cart — this documents that behaviour.
    # a bug report should be raised if this is not the intended behaviour.

    # click on the cart button
    log_in_to_saucedemo.locator(".shopping_cart_link").click()
    # check that the cart is empty
    expect(log_in_to_saucedemo.locator(".cart_item")).to_have_count(0)
    # click on the 'Checkout' button
    log_in_to_saucedemo.locator("[data-test='checkout']").click()
    # check that the checkout page is displayed
    expect(log_in_to_saucedemo.locator(".title")).to_have_text("Checkout: Your Information")
    # fill in the checkout information
    log_in_to_saucedemo.locator("[data-test='firstName']").fill("John")
    log_in_to_saucedemo.locator("[data-test='lastName']").fill("Doe")
    log_in_to_saucedemo.locator("[data-test='postalCode']").fill("12345")
    # click on the 'Continue' button
    log_in_to_saucedemo.locator("[data-test='continue']").click()
    # check that the checkout overview page is displayed
    expect(log_in_to_saucedemo.locator(".title")).to_have_text("Checkout: Overview")
    # click on the 'Finish' button
    log_in_to_saucedemo.locator("[data-test='finish']").click()
    # check that the checkout complete page is displayed
    expect(log_in_to_saucedemo.locator(".title")).to_have_text("Checkout: Complete!")

def test_checkout_with_items(log_in_to_saucedemo):
    # on the inventory page, click one of the "Add to cart" buttons
    log_in_to_saucedemo.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    log_in_to_saucedemo.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    # click on the cart button
    log_in_to_saucedemo.locator(".shopping_cart_link").click()
    # check number of items in the cart
    cart_item = log_in_to_saucedemo.locator(".cart_item")
    expect(cart_item).to_have_count(2)
    # click on the 'Checkout' button
    log_in_to_saucedemo.locator("[data-test='checkout']").click()
    # check that the checkout page is displayed
    expect(log_in_to_saucedemo.locator(".title")).to_have_text("Checkout: Your Information")
    # fill in the checkout information
    log_in_to_saucedemo.locator("[data-test='firstName']").fill("John")
    log_in_to_saucedemo.locator("[data-test='lastName']").fill("Doe")
    log_in_to_saucedemo.locator("[data-test='postalCode']").fill("12345")
    # click on the 'Continue' button
    log_in_to_saucedemo.locator("[data-test='continue']").click()
    # check that the checkout overview page is displayed
    expect(log_in_to_saucedemo.locator(".title")).to_have_text("Checkout: Overview")
    # check that the items are displayed on the checkout overview page
    expect(log_in_to_saucedemo.locator(".cart_item")).to_have_count(2)
    expect(log_in_to_saucedemo.locator(".inventory_item_name").nth(0)).to_have_text("Sauce Labs Backpack")
    expect(log_in_to_saucedemo.locator(".inventory_item_name").nth(1)).to_have_text("Sauce Labs Bike Light")
    # check item total and tax calculations
    item_total = log_in_to_saucedemo.locator(".summary_subtotal_label").text_content()
    tax = log_in_to_saucedemo.locator(".summary_tax_label").text_content()
    total = log_in_to_saucedemo.locator(".summary_total_label").text_content()
    # extract the numeric values from the text
    item_total_value = float(item_total.split("$")[1])
    tax_value = float(tax.split("$")[1])
    total_value = float(total.split("$")[1])
    # check that the total is equal to item total + tax
    assert total_value == item_total_value + tax_value
    # click on the 'Finish' button
    log_in_to_saucedemo.locator("[data-test='finish']").click()
    # check that the checkout complete page is displayed
    expect(log_in_to_saucedemo.locator(".title")).to_have_text("Checkout: Complete!")