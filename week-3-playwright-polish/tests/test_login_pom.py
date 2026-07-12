from playwright.sync_api import expect
import pytest
from pages.login_page import LoginPage

# ---- Baseline checks (raw page, no POM) ------

@pytest.mark.smoke
def test_visibility_of_error(page):
    # This test checks that the error message is not visible on the login page when it first loads.
    page.goto("/")
    error = page.locator("[data-test='error']")
    expect(error).not_to_be_visible()

@pytest.mark.smoke
def test_visibility_of_login_button(page):
    # This test checks that the login button is visible on the login page when it first loads.
    page.goto("/")
    expect(page.locator("#login-button")).to_be_visible()

@pytest.mark.smoke
def test_login_button_enabled(page):
    # This test checks that the login button is enabled on the login page when it first loads.
    page.goto("/")
    expect(page.locator("#login-button")).to_be_enabled()

@pytest.mark.smoke
def test_page_title(page):
    # This test checks that the page title is "Swag Labs" when the login page first loads.
    page.goto("/")
    expect(page).to_have_title("Swag Labs")

@pytest.mark.smoke
def test_username_placeholder_text(page):
    # This test checks that the username input field has the correct placeholder text when the login page first loads.
    page.goto("/")
    username_input = page.locator("#user-name")
    expect(username_input).to_have_attribute("placeholder", "Username")

@pytest.mark.smoke
def test_password_placeholder_text(page):
    # This test checks that the password input field has the correct placeholder text when the login page first loads.
    page.goto("/")
    password_input = page.locator("#password")
    expect(password_input).to_have_attribute("placeholder", "Password")

@pytest.mark.smoke
def test_login_button_text(page):
    # This test checks that the login button has the correct text when the login page first loads.
    page.goto("/")
    button = page.locator("#login-button")
    expect(button).to_contain_text("Login")

@pytest.mark.smoke
def test_response_code(page):
    # This test checks that the response code is 200 when the login page first loads.
    response = page.goto("/")
    assert response.status == 200

# ---- Successful login (fixture + POM) ------

def test_url_after_login(log_in_to_saucedemo):
    # This test checks that the URL is correct after a successful login using the log_in_to_saucedemo fixture, which uses the LoginPage POM to perform the login action.
    expect(log_in_to_saucedemo).to_have_url("/inventory.html")

# ---- Failed login (POM) ------

def test_invalid_credentials(page):
    # This test checks that the error message is displayed when invalid credentials are used to log in using the LoginPage POM.
    login = LoginPage(page)
    login.navigate()
    login.login_with_invalid_credentials()
    expect(login.error_message).to_contain_text(
        "Epic sadface: Username and password do not match any user in this service"
    )

def test_empty_username_text(page):
    # This test checks that the error message is displayed when the username field is left empty during login using the LoginPage POM.
    login = LoginPage(page)
    login.navigate()
    login.login_with_empty_username()
    expect(login.error_message).to_contain_text("Epic sadface: Username is required")

def test_empty_password_text(page):
    # This test checks that the error message is displayed when the password field is left empty during login using the LoginPage POM.
    login = LoginPage(page)
    login.navigate()
    login.login_with_empty_password()
    expect(login.error_message).to_contain_text("Epic sadface: Password is required")
