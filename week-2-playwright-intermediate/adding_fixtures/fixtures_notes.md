# Fixtures in Playwright

Playwright Test is based on the concept of test fixtures. 

Test fixtures are preliminary conditions or steps that are executed before running a test. They are used to establish the environment for each test, giving the test everything it needs and nothing else. Think of them as helpers that provide things you commonly need, so you don't have to create them from scratch every time.

## Fixture Scope

Fixtures have a **scope** that controls how often they run:

| Scope | Runs once per... |
|:------|:-----------------|
| `function` | test (default) |
| `class` | class |
| `module` | file |
| `session` | entire test run |

Function scope is the right choice for most UI tests, as it gives each test a clean, isolated state.

## Playwright's Built-in Fixture Hierarchy

Playwright manages three layers automatically when you use the `page` fixture:

```
browser  →  context  →  page
```

- **browser:** the browser application (Chrome, Firefox, etc). Slow to create, so shared across tests by default.
- **context:** equivalent to a fresh incognito window with its own cookies, storage, and session. Created fresh per test, which is where test isolation comes from.
- **page:** a tab within the context. Created fresh per test.

So when you write `def test_something(page)`, Playwright is silently reusing the browser, creating a new context, and creating a new page, giving you full isolation without any setup code.

REMEMBER: `browser` is session-scoped by default, while `context` and `page` are function-scoped.

## Fixture Scope — Practical Scenarios

**Scenario 1: You're writing a test suite with 50 tests. Every test needs to check the same read-only configuration file. What scope would you use for a fixture that loads that file, and why?**

Use **session scope**. Since the file is read-only, no test can modify it, so sharing it across the entire test run is safe. Recreating it for every test would be wasteful with no benefit, as the file content never changes, so there's nothing to isolate.

```python
@pytest.fixture(scope="session")
def config():
    with open("config.json") as f:
        return json.load(f)
```

---

**Scenario 2: Two tests run back to back. Test 1 logs in and adds 3 items to the cart. Test 2 expects the cart to be empty. Both use the `page` fixture. Will Test 2 fail because of Test 1?**

No. Each test gets a fresh **context**, which is equivalent to a new incognito window with its own cookies, storage, and session. Whatever Test 1 did to its page is completely invisible to Test 2. This is Playwright's built-in test isolation. It comes from the context, not the browser.

---

**Scenario 3: You want to test the same login flow on Chrome, Firefox, and WebKit. Which built-in Playwright fixture would you use to find out which browser is currently running?**

Use the **`browser_name`** fixture, which returns `"chromium"`, `"firefox"`, or `"webkit"` as a string. The `browser` fixture gives you the browser instance itself, not its name, so it wouldn't help here.

```python
def test_something(page, browser_name):
    if browser_name == "firefox":
        # handle firefox-specific behaviour
        pass
```

---

**Scenario 4: You write a fixture that navigates to a page and fills in a form. A teammate says "just make it session-scoped so it's faster." Why might that be a bad idea?**

A session-scoped fixture runs **once** for the entire test run, meaning all 50 tests share the same page state. If Test 3 submits the form, Test 4 will find the form already submitted, or on a completely different page, and fail. This is called **test pollution**: one test's actions contaminating another's state. The fix is to keep the fixture at **function scope** (the default), so every test starts fresh.

---

## Browser, Context, and Page

### The Analogy

Think of the three layers like this:

| Playwright | Real-world equivalent |
|:-----------|:----------------------|
| `browser` | The browser application (e.g. Chrome) running on your computer |
| `context` | A new incognito window — isolated cookies, storage, and login state |
| `page` | A tab within that incognito window |

### How they relate to each other

```
browser
  └── context (incognito window)
        └── page (tab)
        └── page (another tab, shares state with the first)
  └── context (another incognito window, isolated from the first)
        └── page
```

**Multiple pages within one context** share cookies, login state, and storage, just like two tabs in the same incognito window.

**Multiple contexts** are completely isolated from each other, just like two separate incognito windows.

### Why this matters for test isolation

When you use the `page` fixture, Playwright automatically:
1. Reuses the shared `browser` (session-scoped, expensive to create)
2. Creates a fresh `context` for the test (function-scoped, where isolation comes from)
3. Creates a fresh `page` within that context (function-scoped)

Each test gets its own context, so no test can interfere with another, even if they run in the same browser.

### When to use each fixture directly

**`page`:** the default choice. Use it for any test that needs a single browser tab.

**`context`:** use it when you need to create multiple pages yourself, for example testing how the site behaves when a user has it open in two tabs simultaneously.

**`browser`:** use it when you need direct control over the browser instance, for example creating multiple contexts with different configurations in the same test.

---

## Browser, Context, and Page — Practical Scenarios

**Scenario 1: You're testing a chat application where two users need to be logged in simultaneously, one as a sender and one as a receiver. Which fixture would you use?**

Use **two separate contexts**, one per user. Each context has its own cookies, storage, and login state, equivalent to two separate incognito windows. This means user A and user B are completely isolated from each other even within the same test, so logging in as one user doesn't affect the other.

---

**Scenario 2: You're testing whether a shopping cart syncs across tabs. A user adds an item in tab 1 and you want to verify it appears in tab 2 without logging in again. Which fixture would you use?**

Use the **`context`** fixture directly and create two pages within it. Since pages within the same context share cookies and login state, the user is automatically logged in across both tabs, exactly what you need to test cross-tab sync behaviour.

---

**Scenario 3: You're testing a banking app. You want to verify that two different users' accounts are completely isolated. Which fixture would you use to represent each user?**

Use **two separate contexts**, one per user. Pages within the same context share cookies and session data, so using separate pages wouldn't be enough, user A's session could leak into user B's. Separate contexts give each user a completely isolated environment.

---

**Scenario 4: A teammate writes a test using the `browser` fixture directly to create a page instead of using the `page` fixture. The test works fine, but you flag it in code review. What's your concern?**

The teammate is creating new pages within the same context, rather than creating a fresh context for each test. While the test works now, this lacks proper isolation, the state of one test could affect another, causing unpredictable failures in the future. The `page` fixture handles this correctly by automatically reusing the shared browser but creating a fresh context per test, which is where isolation comes from. There's no reason to reach for `browser` directly unless you specifically need to control context configuration.

---

## Applying this knowledge to my tests

### test_login_page_with_fixtures.py

**This file uses only function-scoped fixtures.**

Every test in this file falls into one of three groups: baseline checks, successful login, and failed login.

**Baseline checks** (`page` fixture) navigate to the login page and assert things such as the page title, button visibility, and placeholder text. They don't change any state, so technically they couldn't interfere with each other, but function scope is still the right choice for consistency and safety. If a future baseline check were to type in a field or interact with the page, it wouldn't unexpectedly affect the next test.

**Failed login tests** (`page` fixture) fill in credentials and click the login button, which triggers an error message. Each test covers a different failure scenario — invalid credentials, empty username, empty password. These must be isolated from each other because each test needs to start from a clean login form with no pre-existing error state.

**Successful login test** (`log_in_to_saucedemo` fixture) uses a custom fixture that chains from `page`, so it inherits function scope. Each run gets a fresh context, logs in, and returns an isolated logged-in page.

If `log_in_to_saucedemo` were session-scoped, it would run once and stay logged in for the entire test session. Baseline tests would land on the inventory page instead of the login form, and failed login tests would skip the login page entirely, causing widespread, unpredictable failures.

**The rule:** default to function scope unless you have a specific, justified reason to share state. The performance cost is negligible; the isolation benefit is significant.

### test_inventory_page_with_fixtures.py

Just like the login page tests described above, **this file uses only function-scoped fixtures**.

This is because each test requires a clean starting state.

The difference from the login file is what the clean state looks like:
- **Login file**: needs a clean, unathenticated page.
- **Inventory page**: needs a clean, authenticated page with an empty cart.

In order to set up the clean, authenticated page with an empty cart, all of the tests in this file use the log_in_to_saucedemo fixture.

Limiting the cart tests to function-scope ensures that the state doesn't leak between them and that the assertions to check the number of items in the cart do not fail.

While the sorting tests are read-only so they wouldn't interfere, keeping them function-scoped is still best practice, for the following reasons:
- **Consistency:** if all tests in the file are function-scoped, the behaviour is predictable and uniform. A developer reading the file doesn't need to think about which tests share state and which don't.
- **Future-proofing:** if someone later modifies a sorting test to also add an item to the cart (e.g. to test sorting after adding items), a session-scoped fixture would suddenly cause that test to bleed into others. Function scope prevents this problem before it starts.
- **The broader principle:** read-only doesn't necessarily mean side-effect free. A sorting test selects a drop-down option, which changes the page state. If that state were shared, the next test would start with the dropdown already set to a non-default value, which could subtly affect results. Any state that depends on the default state order (for example, checking the name of the first product on the page), could fail unexpectedly. Function scope prevents this by resettng the page between tests.

### test_cart_page_with_fixtures.py

**This file uses only function‑scoped fixtures**, which is essential because every test interacts with **mutable cart state**. Items are added, removed, persisted, and checked across navigation and logout/login flows. Any shared fixture would immediately cause cross‑test contamination.

The three fixtures used here each provide a clean, predictable starting point:

- **`log_in_to_saucedemo`** → logged‑in page with an empty cart  
- **`add_backpack_to_cart`** → logged‑in page with exactly one item  
- **`add_backpack_and_bike_light_to_cart`** → logged‑in page with exactly two items  

Because they all chain from `page`, they inherit Playwright’s built‑in isolation: a fresh context and a fresh page for every test.

**Empty cart tests:** `log_in_to_saucedemo` guarantees a fresh login and an empty cart. Even simple checks need function scope. If any previous test had added items, a shared fixture would break this immediately.

**Single‑item tests:** Tests that add or remove the backpack rely on `add_backpack_to_cart`. Function scope ensures the cart always starts with one item and never accumulates or loses items because of earlier tests.

Tests that verify **selective removal** or **persistence** use `add_backpack_and_bike_light_to_cart`. Function scope prevents any removal or navigation in one test from affecting the next.

**Navigation and logout/login tests:** Several tests click “Continue Shopping” or even log out and log back in. These actions significantly mutate page state. With a session‑scoped fixture, these mutations would permanently affect all subsequent tests. Function scope avoids this entirely.

**The broader principle:** Even tests that appear “read‑only” still click buttons, navigate, or change UI state. Keeping everything function‑scoped ensures consistent behaviour, no order-dependent failures, safe future modifications, and complete isolation of cart state.

### test_checkout_page_with_fixtures.py

**This file also uses only function‑scoped fixtures**, which is necessary because checkout behaviour depends entirely on the cart state set up before each test. The two fixtures used here are `log_in_to_saucedemo` and `add_backpack_and_bike_light_to_cart`. They each provide a clean, controlled starting point:

- **`log_in_to_saucedemo`** → logged‑in page with an empty cart  
- **`add_backpack_and_bike_light_to_cart`** → logged‑in page with exactly two items  

Because both fixtures chain from `page`, they inherit Playwright’s built‑in isolation: a fresh context and a fresh page for every test. This ensures that checkout behaviour is tested consistently, without interference from earlier tests that may have added, removed, or modified cart contents.

**Checkout with an empty cart:** The first test uses `log_in_to_saucedemo`, guaranteeing an authenticated page with an empty cart. This allows the test to document Saucedemo’s behaviour when checking out with no items. Function scope is essential here — if any previous test had added items, a shared fixture would cause this test to fail or produce misleading results.

**Checkout with items:** The second test uses `add_backpack_and_bike_light_to_cart`, which ensures the cart contains exactly two items before checkout begins. The test verifies that the checkout flow correctly displays item details, calculates totals, and completes the order. Function scope prevents earlier tests from altering the cart, which is critical for verifying tax and total calculations accurately.

**The broader principle:** Checkout tests rely heavily on the initial cart state. Even though both tests follow the same checkout steps, they require different starting conditions. Keeping fixtures function‑scoped ensures:
- predictable cart contents  
- no cross‑test contamination  
- accurate total and tax calculations  
- safe future modifications to test behaviour  

---

## Custom Fixtures (Playwright Python)

In Playwright’s Python implementation, custom fixtures are created using **pytest’s fixture system**. They live in `conftest.py`, which pytest automatically discovers, making the fixtures available across all test files. Fixtures let you centralise repeated setup steps, so your tests stay clean, readable, and consistent.

### How fixtures work  
- Fixtures are defined with `@pytest.fixture`.  
- They can depend on other fixtures (e.g., a cart fixture depends on the login fixture).  
- They return whatever object the test needs—typically a `page` or a page object.  
- They run once per test by default (**function scope**), which is ideal for UI tests because it guarantees isolation and prevents state leakage between tests.

### Summary of project fixtures  
- **`log_in_to_saucedemo`**  
  Logs in using valid credentials and returns a fresh, authenticated page. Used by any test that requires a logged‑in state.

- **`add_backpack_to_cart`**  
  Starts from a logged‑in page, adds exactly one item to the cart, and navigates to the cart page. Used for tests that require a single‑item cart.

- **`add_backpack_and_bike_light_to_cart`**  
  Adds two specific items to the cart and opens the cart page. Used for tests that verify multi‑item behaviour, removal logic, or checkout totals.

### Why function scope is correct  
All fixtures operate on **mutable page state** (login status, cart contents, navigation). Function scope ensures each test begins with a clean context and prevents cross‑test contamination—critical for reliable UI automation.

### Fixture Chaining

Fixture chaining is the practice of building one fixture on top of another. In Playwright Python, this works because pytest allows fixtures to **depend on other fixtures simply by listing them as parameters**. Each fixture receives the output of the fixture it depends on, creating a clean, modular setup pipeline.

### Why chaining matters  
- It keeps fixtures **focused**: each fixture does one job (login, add one item, add two items).  
- It avoids duplication: shared steps (like logging in) live in one place.  
- It ensures **consistent test state**: every fixture starts from a known, validated baseline.  
- It makes tests easier to read: tests describe *intent*, not setup details.

### How chaining works  
When a fixture depends on another fixture, pytest resolves them in order:

1. The dependency runs first (e.g., `log_in_to_saucedemo`).  
2. Its return value is passed into the next fixture (e.g., `add_backpack_to_cart`).  
3. The final fixture returns the fully prepared state to the test.

This creates a predictable sequence:

```
page → log_in_to_saucedemo → add_backpack_to_cart → test
```

Each step builds on the previous one, and because all fixtures are **function‑scoped**, the chain is rebuilt fresh for every test.

### In my project  

- **`log_in_to_saucedemo`**  
  Base fixture: provides an authenticated page.

- **`add_backpack_to_cart`**  
  Depends on the login fixture to guarantee the correct starting page.

- **`add_backpack_and_bike_light_to_cart`**  
  Also depends on the login fixture, ensuring both items are added from a clean state.

This structure keeps my cart tests reliable and prevents state leakage, while keeping the setup logic simple and reusable.

### How Playwright’s built‑in fixtures interact with my custom ones

Playwright provides built‑in fixtures such as `page`, `browser`, and `context`.

Custom fixtures typically chain from `page`, which ensures each test receives a fresh browser context and isolated state.

This is why function‑scoped custom fixtures remain safe and predictable.

### What fixtures should and should not do

Fixtures should:
- prepare state needed by multiple tests
- return objects required by tests (e.g., a logged‑in page or structured test data)
- remain small, predictable, and single‑purpose

Fixtures should not:
- contain assertions
- hide important test logic
- perform excessive navigation or unrelated actions
- be used for one‑off setup that only a single test requires

Keeping fixtures minimal and intention‑focused ensures that tests remain clear and failures are easy to diagnose.

