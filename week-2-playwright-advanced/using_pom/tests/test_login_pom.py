from playwright.sync_api import expect
from ..pages.login_page import LoginPage

# Baseline checks (raw page, no POM)
def test_pom_visibility_of_error(page):
    page.goto("https://www.saucedemo.com/")
    error = page.locator("[data-test='error']")
    expect(error).not_to_be_visible()

def test_pom_visibility_of_login_button(page):
    page.goto("https://www.saucedemo.com/")
    expect(page.locator("#login-button")).to_be_visible()

def test_pom_login_button_enabled(page):
    page.goto("https://www.saucedemo.com/")
    expect(page.locator("#login-button")).to_be_enabled()

def test_pom_page_title(page):
    page.goto("https://www.saucedemo.com/")
    expect(page).to_have_title("Swag Labs")

def test_pom_username_placeholder_text(page):
    page.goto("https://www.saucedemo.com/")
    username_input = page.locator("#user-name")
    expect(username_input).to_have_attribute("placeholder", "Username")

def test_pom_password_placeholder_text(page):
    page.goto("https://www.saucedemo.com/")
    password_input = page.locator("#password")
    expect(password_input).to_have_attribute("placeholder", "Password")

def test_pom_login_button_text(page):
    page.goto("https://www.saucedemo.com/")
    button = page.locator("#login-button")
    expect(button).to_contain_text("Login")

def test_pom_response_code(page):
    response = page.goto("https://www.saucedemo.com/")
    assert response.status == 200

# Successful login (fixture + POM)
def test_pom_url_after_login(log_in_to_saucedemo):
    expect(log_in_to_saucedemo).to_have_url("https://www.saucedemo.com/inventory.html")

# Failed login (POM)
def test_pom_invalid_credentials(page):
    page.goto("https://www.saucedemo.com/")
    login = LoginPage(page)
    login.login("invalid_user", "invalid_password")
    expect(login.error_message).to_contain_text(
        "Epic sadface: Username and password do not match any user in this service"
    )

def test_pom_empty_username_text(page):
    page.goto("https://www.saucedemo.com/")
    login = LoginPage(page)
    login.login("", "secret_sauce")
    expect(login.error_message).to_contain_text("Epic sadface: Username is required")

def test_pom_empty_password_text(page):
    page.goto("https://www.saucedemo.com/")
    login = LoginPage(page)
    login.login("standard_user", "")
    expect(login.error_message).to_contain_text("Epic sadface: Password is required")
