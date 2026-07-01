from playwright.sync_api import expect

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
