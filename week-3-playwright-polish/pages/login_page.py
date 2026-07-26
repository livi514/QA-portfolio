from test_data import INVALID_USER, VALID_USER


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    # Navigation
    def navigate(self):
        self.page.goto("/")

    # Field-level actions
    def fill_username(self, username):
        self.username_input.fill(username)

    def fill_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    # Combined action
    def login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    # Common login scenarios
    def login_with_valid_credentials(self):
        self.login(VALID_USER["username"], VALID_USER["password"])

    def login_with_invalid_credentials(self):
        self.login(INVALID_USER["username"], INVALID_USER["password"])

    def login_with_empty_username(self):
        self.login("", VALID_USER["password"])

    def login_with_empty_password(self):
        self.login(VALID_USER["username"], "")

    # Accessors
    def get_error_message(self):
        return self.error_message.inner_text()

    def get_username_placeholder(self):
        return self.username_input.get_attribute("placeholder")

    def get_password_placeholder(self):
        return self.password_input.get_attribute("placeholder")

    # State helpers
    def is_error_visible(self):
        return self.error_message.is_visible()

    def is_login_button_enabled(self):
        return self.login_button.is_enabled()

    def is_login_button_visible(self):
        return self.login_button.is_visible()

    def is_on_inventory_page(self):
        return self.page.url.endswith("/inventory.html")
