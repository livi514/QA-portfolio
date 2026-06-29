def test_locators(page):
    # navigate to the login page
    # page.goto() loads the specified URL in the browser
    # this is always the first step in a UI test, as we need to start from a known state
    page.goto("https://www.saucedemo.com/")
    # test various locators
    username_input = page.locator("#user-name")
    password_input = page.locator("#password")
    login_button = page.locator("#login-button")
    assert username_input.is_visible()
    assert password_input.is_visible()
    assert login_button.is_visible()
    # fill in the username and password fields
    # locator.fill() is used for typing into input fields
    # perfect for username and password fields
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # find the error message locator
    error = page.locator("[data-test='error']")
    # assert that no error message is visible 
    assert not error.is_visible()


    
