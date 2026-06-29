def test_login_success(page):
    page.goto("https://www.saucedemo.com/")

    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    # After login, the URL should change
    assert page.url.endswith("/inventory.html")
