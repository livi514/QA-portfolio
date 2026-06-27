def test_login_error(page):
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "invalid_user")
    page.fill("#password", "wrong_password")
    page.click("#login-button")

    error = page.locator("[data-test='error']")
    assert error.is_visible()
    assert "Epic sadface" in error.text_content()


