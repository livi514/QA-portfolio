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

## **5. What Belongs in POM**
- Selectors for that page  
- Reusable actions  
- Methods that expose UI state  
- Clear, intention‑focused method names  

## **6. What Does NOT Belong in POM**
- Assertions  
- Test logic or branching  
- Fixture logic  
- Hard‑coded test data  
- Navigation unrelated to the page  
- Complex conditional behaviour  

POM represents the UI — not the testing strategy.

## **7. How Tests Use Page Objects**
General pattern:

1. Test receives a `page` (usually from a fixture)  
2. Test instantiates the relevant page class  
3. Test calls methods on the page class to perform actions  
4. Test asserts on returned values or visible state  

This keeps tests short, readable, and behaviour‑focused.

## **8. How POM Interacts With Fixtures**
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

## **9. Naming Conventions**
Use clear, consistent names:

- Page classes: `LoginPage`, `InventoryPage`, `CartPage`  
- Action methods: verbs (`login()`, `add_item()`, `sort_by_price()`)  
- Accessors: descriptive (`cart_count()`, `error_message()`)  

This makes tests read like a story.

## **10. Folder Structure (Recommended)**
```
pages/
    login_page.py
    inventory_page.py
    cart_page.py

tests/
    test_login_pom.py
    test_inventory_pom.py
    test_cart_pom.py

conftest.py
data/
    users.json
```

This is the standard industry layout for POM‑based Playwright projects.

## **11. Summary**
POM turns each page into a class that exposes clean, reusable actions and state.  
Tests become shorter, clearer, and easier to maintain.  
Fixtures prepare state; POM performs interactions; tests assert behaviour.  
This structure is the foundation of professional UI automation.
