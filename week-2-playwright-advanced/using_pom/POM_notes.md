# Page Object Model (POM)

## 1. Purpose of POM

POM is a design pattern used in UI automation to make tests cleaner, more readable, and easier to maintain. It solves three major problems:

- **Duplication:** repeated selectors and flows across tests  
- **Fragility:** UI changes break many tests at once  
- **Noise:** tests become long and focused on mechanics instead of behaviour  

POM centralises selectors and interactions into dedicated page classes so tests can focus on *what* is being tested, not *how* to click through the UI.


## 2. Core Concept

Treat each page of the application as a **class**.

Each page class:
- represents one screen/page  
- stores selectors  
- provides reusable actions  
- exposes UI state for assertions  

Tests interact with these classes instead of raw selectors.

## 3. Benefits

- **Cleaner tests:** tests read like behaviour, not click scripts  
- **Centralised selectors:** update in one place when UI changes  
- **Reusable flows:** login, add to cart, checkout become simple method calls  
- **Maintainability:** large suites stay organised and predictable  
- **Onboarding:** new contributors understand the structure quickly  


## 4. Structure of a Page Class

A page class contains three components:

**Constructor:**
- Receives the Playwright `page` object  
- Stores it  
- Defines selectors as attributes  

**Action methods:**
- Perform interactions  
- Examples: `login()`, `add_item()`, `open_cart()`

**State accessors:**
- Return UI state for tests to assert  
- Examples: `cart_count()`, `error_message()`, `is_loaded()`

**Important:** Page objects do **not** contain assertions or test logic.

## 5. What Belongs in POM
- Selectors for that page  
- Reusable actions  
- Methods that expose UI state  
- Clear, intention‑focused method names  

## 6. What Does NOT Belong in POM
- Assertions  
- Test logic or branching  
- Fixture logic  
- Hard‑coded test data  
- Navigation unrelated to the page  
- Complex conditional behaviour  

POM represents the UI — not the testing strategy.

## 7. How Tests Use Page Objects
General pattern:

1. Test receives a `page` (usually from a fixture)  
2. Test instantiates the relevant page class  
3. Test calls methods on the page class to perform actions  
4. Test asserts on returned values or visible state  

This keeps tests short, readable, and behaviour‑focused.

## 8. How POM Interacts With Fixtures
Fixtures prepare **starting state**.  
Page objects perform **interactions**.  
Tests perform **assertions**.

Example flow:

```
fixture → returns page
test → creates LoginPage(page)
test → calls login_page.login()
test → creates InventoryPage(page)
test → asserts inventory_page.is_loaded()
```

Fixtures and POM complement each other but serve different roles.

## 9. Naming Conventions
Use clear, consistent names:

- Page classes: `LoginPage`, `InventoryPage`, `CartPage`  
- Action methods: verbs (`login()`, `add_item()`, `sort_by_price()`)  
- Accessors: descriptive (`cart_count()`, `error_message()`)

## 10. Applied Example: saucedemo.com Cart Page

In the `using_pom` folder, you can see how I have converted the tests from the `adding_fixtures` folder to use the POM design pattern. 

For example, in `test_cart_page_with_fixtures.py`, there was significant repetition across tests, including:

- Raw locators for removing specific items (`[data-test='remove-sauce-labs-backpack']`, `[data-test='remove-sauce-labs-bike-light']`)
- Locators for cart items, item names, and item prices repeated in every test
- Manual item count and name checks scattered throughout

Using POM, I created a `CartPage` class consisting of a constructor, action methods, and state accessors.

The constructor receives the Playwright `page` object and defines all locators as attributes, including locators for cart items, inventory item names and prices, "Remove" buttons, the "Continue Shopping" button, and the "Checkout" button.

I then defined action methods for repeated interactions: `remove_backpack()`, `remove_bike_light()`, `continue_shopping()`, and `checkout()`. Finally, I defined accessors for retrieving item count (`get_item_count()`), item names (`get_item_names()`), item prices (`get_item_prices()`), and the page title (`get_title_text()`).

Converting the tests to use `CartPage` shifted the focus from *how* to locate and click elements to *what* is actually being tested. For example:

**Before:**
```python
add_backpack_and_bike_light_to_cart.locator("[data-test='remove-sauce-labs-backpack']").click()
assert add_backpack_and_bike_light_to_cart.locator(".cart_item").count() == 2
assert add_backpack_and_bike_light_to_cart.locator(".inventory_item_name").nth(0).inner_text() == "Sauce Labs Backpack"
```

**After:**
```python
cart.remove_backpack()
assert cart.get_item_count() == 2
assert cart.get_item_names()[0] == "Sauce Labs Backpack"
```

The after version reads like a plain English description of the test scenario. This is exactly what POM is designed to achieve.

## 11. Summary
POM turns each page into a class that exposes clean, reusable actions and state.  
Tests become shorter, clearer, and easier to maintain.  
Fixtures prepare state; POM performs interactions; tests assert behaviour.  
This structure is the foundation of professional UI automation.
