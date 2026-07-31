from playwright.sync_api import expect


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
    expect(page.locator(".inventory_item_name").nth(0)).to_have_text(
        "Sauce Labs Backpack"
    )
    expect(page.locator(".inventory_item_name").nth(1)).to_have_text(
        "Sauce Labs Bike Light"
    )
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
