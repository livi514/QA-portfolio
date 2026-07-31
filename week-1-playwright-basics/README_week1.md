# QA Summer Roadmap - Week 1

## Introduction

Week 1 of my QA Summer Roadmap focuses on learning the fundamentals of Playwright for Python, building confidence with browser automation, and writing my first structured UI test suite using pytest and Playwright’s built‑in fixtures.

This week was all about understanding how Playwright works, how UI tests should be structured, and how to write reliable, readable tests that assert real behaviour.

Before starting the week, my goals were simple: install Playwright, read the intro docs, learn key features such as locators and assertions, write a few tests on a demo site, and summarise what I've learned in a README. 

However, this week became much more than just writing a few unit tests using a new tool. In fact, it reshaped how I think about QA.

## What I Tested

### Login Page (test_login_page.py)

I started with baseline checks: verifying that the page loads correctly before any user interaction occurs. 
This included checking that no error message is visible on arrival, that the login button is visible, enabled, and displays the correct text, that the expected page title is shown, that the username and password fields display the correct placeholder text, and that the server returns a 200 OK response.

I then tested the login logic itself, covering both successful and unsuccessful journeys. For successful logins, I verified that valid credentials redirect the user to the inventory page. For failed logins, I tested several distinct failure scenarios: invalid credentials, an empty username field, and an empty password field, each of which produces a different error message.

### Inventory Page (test_inventory_page.py)

I verified that the inventory page renders with the expected number of products (6), and tested the add-to-cart and remove-from-cart interactions,  checking that the cart badge, button text, and item count all update correctly. I also wrote two parametrised tests to verify the sorting functionality, covering both name-based sorting (A–Z and Z–A) and price-based sorting (low to high and high to low).

### Cart Page (test_cart_page.py)

I tested the cart page across a range of scenarios: an empty cart state, adding and removing individual items, and verifying that removing one item does not affect others. I also wrote two state persistence tests: verifying that cart contents are preserved when navigating back to the inventory page, and that they persist after logging out and back in as the same user. The latter behaviour was documented as observed and flagged for review, as it may not be the intended design.

### Checkout (test_checkout_page.py)

I tested the full checkout flow with items in the cart, verifying correct navigation through each step and that the order total correctly reflects the sum of item costs and tax. I also discovered that saucedemo permits checkout with an empty cart: this was documented as observed behaviour rather than assumed to be intentional.

## What I Learned This Week 

### Playwright Fundamentals

Though I have prior experience with Python and pytest, I had never used Python with Playwright before, and I haven't explored browser automation before starting this roadmap. Something new to me this week was automating browser actions like clicking buttons, filling forms, and navigating between pages. Previously, I had only done this through manual testing. However, Playwright made this straightforward, and seeing tests replicate real user journeys automatically was a genuinely useful shift in how I think about testing.

I also learned about expect(), Playwright's built-in assertion library. Unlike a plain Python assert, which evaluates a condition once and immediately passes or fails, expect() uses auto-retrying. Playwright runs a check in the background repeatedly until the condition passes or a timeout is reached. This makes tests far more resilient to timing issues and page load delays.

### Locator Strategies
I explored different ways to locate elements on a page and learned that not all locators are equally reliable. ID selectors (#id) are simple and readable, but [data-test="..."] attribute selectors are the most stable choice for UI testing , as they're specifically intended for test automation and are less likely to change when the UI is restyled or restructured. I also used CSS class selectors for targeting repeated elements like lists of products.

### Assertions
I practised a wide range of assertions this week, including visibility checks, text content, URL changes, page title, element count, HTML attributes, and enabled/disabled state. I also learned the difference between to_be_visible() and to_have_count(0). Both can express "this element isn't here", but the latter is more precise when you're verifying an empty state rather than just absence from view.

### Test Structure
I followed the Arrange → Act → Assert pattern throughout: setting up the page state, performing the user action, then verifying the outcome. This gave my tests a consistent, predictable shape that makes them easier to read and debug. I also learned about pytest.mark.parametrize, which allowed me to run the same test logic with multiple inputs. This was particularly useful for testing the four sorting options on Saucedemo's inventory page without duplicating code.

## Key Takeaways from this week 

Not all of my takeaways are directly related to learning Playwright. In fact, the most important things I learned this week, are more about mindset than any specific tool.

### The importance of quality over quantity

Before writing a test, you need to think about whether the logic has already been checked, or if it can be combined with an existing test. I've learnt a lot of new strategies for keeping my test suites concise.

### The importance of organising tests based on the functionality they are testing

Throughout this week, I went from one big file of random assertions grouped by Playwright feature, to separate files per page/feature that was being tested. While grouping my tests by assertions initially helped me to understand the concepts I was learning, re-organising them based on the feature being tested made them better align with how QA is done in the workplace, and helped me to identify any features or functionality that was yet to be tested. By the end of the week, I had tested key functionality such as ensuring the right elements were displayed, checking that buttons navigated to the correct page, checking state persistence, and checking access control.

## How to Run the Tests

For full setup and installation instructions, see the main README.

Ensure you are running commands from the `week-1-playwright-basics` folder. 

Use `cd week-1-playwright-basics` to navigate to the folder if necessary.

Run all tests: `pytest`

Run a specific test file: `pytest tests/test_login_page.py`

Run tests in headed mode (useful for debugging): `pytest --headed`
