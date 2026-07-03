# Fixtures in Playwright

Playwright Test is based on the concept of test fixtures. 

Fixtures are objects that help you set up your tests efficiently. They are used to establish the environment for each test, giving the test everything it needs and nothing else. Think of them as helpers that provide things you commonly need, so you don't have to create them from scratch every time.

Test fixtures are isolated between tests. With fixtures, you can group tedts based on their meaning, instead of their common setup.

## Examples

I've already used fixtures briefly during week 1, for example`page.goto()`. Now, in week 2, I will explore them in more detail.

Let's start with a simple example:

```
import { test, expect } from '@playwright/test';

test('basic test', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/Playwright/);
});
```

In the above code:
- The **page object** is a fixture provided by Playwright.
- It's automatically created for your test, and it represents a browser page that you can use to interact with the website.
- You didn't have to write code to open a browser or create a page. Playwright does this for you automatically using the page fixture.

Another example - Imagine you're testing a simple website, like a login page. Here's how page fixtures help:

```
import { test, expect } from '@playwright/test';
test('login page test', async ({ page }) => {
  
  await page.goto('https://example.com/login'); 
  await expect(page).toHaveURL(/login/); 
});
```

**Without fixtures**: you'd have to manually write code to launch a browser, open a new tab, etc.

**With fixtures**: Playwright prepared the page ready to go!

## Why are fixtures useful?

- **Improved efficiency:** You don't need to set up a browser or page yourself.
- **Consistency:** Every test gets the same fresh page to work with.
- **Cleanup:** Playwright automatically closes the browser after the test, so you don't have to.

## Other fixtures in Playwright

| Fixture      | Type               | Description                                      |
|:-------------|:-------------------|:-------------------------------------------------|
| page         | Page               | Isolated page for this test run                  |
| context      | BrowserContext     | Isolated context for this test run. The page fixture belongs to this context |
| browser      | Browser            | Browsers are shared across tests to optimise resources |
| browserName  | string             | The name of the browser currently running the test: chromium, firefox, or webkit |
| request      | APIRequestContext  | Isolated APIRequestContext instance for this test run |

## browser fixture

The browser fixture gives you access to the entire browser instance (e.g. Chrome, Firefox). You can use it to control the browser or launch multiple pages.

```
import { test, expect } from '@playwright/test';

test('check browser type', async ({ browser }) => {  
  // Open a new page manually using the browser fixture
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});
```

