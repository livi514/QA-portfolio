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

Use **session scope**. Since the file is read-only, no test can modify it, so sharing it across the entire test run is safe. Recreating it for every test would be wasteful with no benefit — the file content never changes, so there's nothing to isolate.

```python
@pytest.fixture(scope="session")
def config():
    with open("config.json") as f:
        return json.load(f)
```

---

**Scenario 2: Two tests run back to back. Test 1 logs in and adds 3 items to the cart. Test 2 expects the cart to be empty. Both use the `page` fixture. Will Test 2 fail because of Test 1?**

No. Each test gets a fresh **context**, which is equivalent to a new incognito window with its own cookies, storage, and session. Whatever Test 1 did to its page is completely invisible to Test 2. This is Playwright's built-in test isolation — it comes from the context, not the browser.

---

**Scenario 3: You want to test the same login flow on Chrome, Firefox, and WebKit. Which built-in Playwright fixture would you use to find out which browser is currently running?**

Use the **`browser_name`** fixture, which returns `"chromium"`, `"firefox"`, or `"webkit"` as a string. The `browser` fixture gives you the browser instance itself, not its name — so it wouldn't help here.

```python
def test_something(page, browser_name):
    if browser_name == "firefox":
        # handle firefox-specific behaviour
        pass
```

---

**Scenario 4: You write a fixture that navigates to a page and fills in a form. A teammate says "just make it session-scoped so it's faster." Why might that be a bad idea?**

A session-scoped fixture runs **once** for the entire test run, meaning all 50 tests share the same page state. If Test 3 submits the form, Test 4 will find the form already submitted — or on a completely different page — and fail. This is called **test pollution**: one test's actions contaminating another's state. The fix is to keep the fixture at **function scope** (the default), so every test starts fresh.

---

## Browser, Context, and Page

### The Analogy

Think of the three layers like this:

| Playwright | Real-world equivalent |
|:-----------|:----------------------|
| `browser` | The Chrome application running on your computer |
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

Here are the polished notes first:

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

