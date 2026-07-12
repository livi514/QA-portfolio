# QA Summer Roadmap - Week 2

## 1. Introduction 

Week 2 of my QA Roadmap focused on expanding my knowledge of Playwright for Python, and improving the clarity and conciseness of my code. I achieved this using two key concepts in test automation: fixtures, to centralise set up code within a conftest.py file, and using the Page Object Model, to centralise selectors and UI interactions in page classes. Restructuring my tests to use these features, helped me to focus them on what is being tested, rather than how to set up the environment or click through the UI. 

## 2. What I tested

This week, rather than adding new tests, I focused on restructuring the saucedemo.com test suite from week 1, converting it to use fixtures and POM.

## 3. What I learned this week 

- Fixtures (summarise theory + add example from my work - don't need loads of detail as I have a separate file for fixtures notes)
- POM (summarise theory + add example from work - again, keep it concise, I have a separate file for detailed POM notes)

### Fixtures

Test fixtures are preliminary conditions or steps that are executed before running a test. They are used to establish the environment for each test, giving the test everything it needs and nothing else. 

I explored fixture scopes (function, class, module, and session), and how Playwright manages three layers automatically when you use the page fixture: browser → context → page. This means that when you write def test_something(page), Playwright is silently reusing the browser, creating a new context, and creating a new page, giving you full isolation without any setup code.

My own tests only used function-scoped fixtures, providing full isolation between tests. For example, the cart page tests needed to be completely isolated from each other, as they interacted with mutable cart state.

As well as using Playwright's built-in fixtures, I defined my own in a conftest.py file. I identified the most commonly repeated setup steps: logging in and adding items to the cart. I then extracted these into custom fixtures.

For example, I created this custom fixture to manage setting up a logged-in environment:
```
def perform_login(page):
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

@pytest.fixture
def log_in_to_saucedemo(page):
    perform_login(page)
    # Wait for navigation to inventory page
    page.wait_for_url("**/inventory.html")
    return page
```

I then used it in tests such as this:
```
def test_number_of_products(log_in_to_saucedemo):
    # This test checks that the inventory page renders with the expected number of inventory items (6).

    # assert that there are 6 products on the inventory page
    expect(log_in_to_saucedemo.locator(".inventory_item")).to_have_count(6)
```

Any updates to this logic now only need to be made in one place.

### Page Object Model

## 4. Key takeaways from this week 

Abstraction — tests should express intent, not implementation details
Single source of truth — centralising setup and selectors means changes propagate from one place

## 5. How to run the tests

For full setup and installation instructions, see the main README.

Run all tests: `pytest`

Run a specific test file: `pytest ui-tests/tests/test_login_page.py`

Run tests in headed mode (useful for debugging): `pytest --headed`