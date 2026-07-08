from playwright.sync_api import expect

# ---- Page load: baseline checks / initial state ------

# Baseline checks answer the question: "Does the page look right on arrival?"

def test_visibility_of_error(page):
    # This is known as a baseline check.
    # This establishes that the page starts in a clean state before any user interaction occurs.
    # In other words, when you navigate to the login page, and haven't interacted with it yet, 
    # there shouldn't be an error message.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # locate the error message 
    error = page.locator("[data-test='error']")
    # assert that the error message is not visible
    expect(error).not_to_be_visible()

def test_visibility_of_login_button(page):
    # What I'm testing:
    # I'm checking what elements are visible on page load.
    # One of the elements that should be visible is the login button.
    # This checks that the page rendered correctly.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # check visibility of login button
    expect(page.locator("#login-button")).to_be_visible()

def test_login_button_enabled(page):
    # The login button should be clickable on page load.
    # Some sites disable the button until fields are filled, this confirms saucedemo doesn't.
    # Using to_be_enabled() to check the button state.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # assert that the login button is enabled
    expect(page.locator("#login-button")).to_be_enabled()

def test_page_title(page):
    # The page should render with the correct title "Swag Labs" visible in the browser tab.
    # Using to_have_title() to check document.title.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # assert that the page title is as expected
    expect(page).to_have_title("Swag Labs")

def test_username_placeholder_text(page):
    # The page should render with an input field with the placeholder text "Username".
    # Using to_have_attribute to check the placeholder text.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # locate the username input field
    username_input = page.locator("#user-name")
    # assert that the username input field has the expected placeholder text
    expect(username_input).to_have_attribute("placeholder", "Username")

def test_password_placeholder_text(page):
    # The page should render with an input field with the placeholder text "Password".
    # Using to_have_attribute to check the placeholder text.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # locate the password input field
    password_input = page.locator("#password")
    # assert that the password input field has the expected placeholder text
    expect(password_input).to_have_attribute("placeholder", "Password")

def test_login_button_text(page):
    # The page should render with a button with the text "Login".
    # Using to_contain_text to check the text on the button.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # locate the login button
    button = page.locator("#login-button")
    # assert that the button contains the expected text
    expect(button).to_contain_text("Login")

def test_response_code(page):
    # The page should load correcly with the response code 200 OK.

    # navigate to the login page
    response = page.goto("https://www.saucedemo.com/") 
    # test response status code
    assert response.status == 200

# ---- Successful login  ------

def test_url_after_login(log_in_to_saucedemo):
    # This test checks that the user is redirected to the expected page (inventory.html) after successfully logging in with valid credentials.

    # assert that the current URL is as expected
    expect(log_in_to_saucedemo).to_have_url("https://www.saucedemo.com/inventory.html")

# ---- Failed login  ------

def test_invalid_credentials(page):
    # This test checks that the expected error message is displayed when invalid credentials are entered.
    # This includes an invalid username, invalid password, or both.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # enter invalid credentials
    page.locator("#user-name").fill("invalid_user")
    page.locator("#password").fill("invalid_password")
    # click the login button
    page.locator("#login-button").click()
    # locate the error message
    error = page.locator("[data-test='error']")
    # assert that the error message contains the expected text
    expect(error).to_contain_text("Epic sadface: Username and password do not match any user in this service")

def test_empty_username_text(page):
    # This test checks that the expected error is displayed when the username field is left empty.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # leave username field empty
    page.locator("#user-name").fill("")
    page.locator("#password").fill("secret_sauce")
    # click the login button
    page.locator("#login-button").click()
    # locate the error message
    error = page.locator("[data-test='error']")
    # assert that the error message contains the expected text
    expect(error).to_contain_text("Epic sadface: Username is required")

def test_empty_password_text(page):
    # This test checks that the expected error is displayed when the password field is left empty.

    # navigate to the login page
    page.goto("https://www.saucedemo.com/")
    # leave password field empty
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("")
    # click the login button
    page.locator("#login-button").click()
    # locate the error message
    error = page.locator("[data-test='error']")
    # assert that the error message contains the expected text
    expect(error).to_contain_text("Epic sadface: Password is required")