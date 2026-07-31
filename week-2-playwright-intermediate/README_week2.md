# QA Summer Roadmap - Week 2

## 1. Introduction

Week 2 of my QA Roadmap focused on expanding my knowledge of Playwright for Python, and improving the clarity and conciseness of my code. I achieved this using two key concepts in test automation: fixtures, to centralise set up code within a `conftest.py` file, and the Page Object Model, to centralise selectors and UI interactions in page classes. Restructuring my tests to use these features helped me to focus them on what is being tested, rather than how to set up the environment or click through the UI.

## 2. What I Tested

This week, rather than adding new tests, I focused on restructuring the saucedemo.com test suite from week 1, converting it to use fixtures and POM.

## 3. What I Learned This Week

### Fixtures

Test fixtures are preliminary conditions or steps that are executed before running a test. They are used to establish the environment for each test, giving the test everything it needs and nothing else.

I explored fixture scopes (function, class, module, and session), and how Playwright manages three layers automatically when you use the `page` fixture: browser → context → page. This means that when you write `def test_something(page)`, Playwright is silently reusing the browser, creating a new context, and creating a new page, giving you full isolation without any setup code.

My own tests only used function-scoped fixtures, providing full isolation between tests. For example, the cart page tests needed to be completely isolated from each other, as they interacted with mutable cart state.

As well as using Playwright's built-in fixtures, I defined my own in a `conftest.py` file. I identified the most commonly repeated setup steps: logging in and adding items to the cart. I then extracted these into custom fixtures.

For example, I created this custom fixture to manage setting up a logged-in environment:

```python
def perform_login(page):
    page.goto("/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

@pytest.fixture
def log_in_to_saucedemo(page):
    perform_login(page)
    page.wait_for_url("**/inventory.html")
    return page
```

I then used it in tests such as this:

```python
def test_number_of_products(log_in_to_saucedemo):
    # assert that there are 6 products on the inventory page
    expect(log_in_to_saucedemo.locator(".inventory_item")).to_have_count(6)
```

Fixtures can also chain from each other. For example, `add_backpack_to_cart` takes `log_in_to_saucedemo` as a parameter, so it automatically inherits the logged-in state without repeating any login logic.

### Page Object Model

POM is a design pattern used in UI automation to make tests cleaner, more readable, and easier to maintain. POM centralises selectors and interactions into dedicated page classes so tests can focus on what is being tested, rather than how to click through the UI.

I created a page class for each saucedemo.com page (login, inventory, cart, checkout) as well as for the menu, in order to centralise logout logic. Each page class consists of three components: a constructor, action methods, and state accessors.

For example, this is the constructor in the `LoginPage` class:

```python
def __init__(self, page):
    self.page = page
    self.username_input = page.locator("#user-name")
    self.password_input = page.locator("#password")
    self.login_button = page.locator("#login-button")
    self.error_message = page.locator("[data-test='error']")
```

It also contains action methods, such as:

```python
def fill_username(self, username):
    self.username_input.fill(username)
```

And state accessors:

```python
def get_error_message(self):
    return self.error_message.inner_text()
```

After defining the page classes, I converted my tests to use POM. For example:

**Before:**
```python
def test_invalid_credentials(page):
    page.goto("/")
    page.locator("#user-name").fill("invalid_user")
    page.locator("#password").fill("invalid_password")
    page.locator("#login-button").click()
    error = page.locator("[data-test='error']")
    expect(error).to_contain_text("Epic sadface: Username and password do not match any user in this service")
```

**After:**
```python
def test_invalid_credentials(page):
    login = LoginPage(page)
    login.navigate()
    login.login_with_invalid_credentials()
    expect(login.error_message).to_contain_text(
        "Epic sadface: Username and password do not match any user in this service"
    )
```

## 4. Key Takeaways From This Week

The biggest shift this week was writing tests that read like specifications rather than click-through instructions.

### Abstraction

Using custom fixtures and POM makes tests more readable and concise, focusing them on what needs to be tested rather than the details of how to set up the environment or locate a particular element. Tests should express intent, not implementation details. Custom fixtures and POM help achieve this through abstraction.

### Single Source of Truth

By centralising setup code in custom fixtures, and centralising locators and UI interactions in page classes, you create a single source of truth. Any updates needed to account for changes in the environment setup or UI interactions now only need to be made in one place, so changes propagate efficiently across the entire suite.

## 5. How to Run the Tests

For full setup and installation instructions, see the main [README](../README.md).

Ensure you are running commands from the `week-2-playwright-intermediate` folder.

Use `cd week-2-playwright-intermediate` to navigate to the folder if necessary.

Run all tests:
```
pytest
```

Run a specific test file:
```
pytest using_pom/tests/test_login_pom.py
```

Run tests in headed mode (useful for debugging):
```
pytest --headed
```