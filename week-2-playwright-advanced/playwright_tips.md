# Notes: Playwright Tips

1. Use Locators Wisely
Avoid brittle XPaths. Instead, use Playwright's locator() function with id, text, or role when possible.

```
page.locator("text=Login")
page.locator("[data-testid='search-bar']")
```

In UI automation tests, unstable selectors are one of the biggest reasons for flaky tests.
That's where Playwright locators come in: a powerful concept that allows you to identify elements like a real user would, using roles, labels, text, and accessibility attributes rather than brittle CSS or XPath selectors.

Locators  in Playwright are element identifiers that power its auto-waiting, retry-ability, and strict mode.
They make sure your tests wait for elements automatically, and interact with the right one, even as the DOM changes.

2. Test in headed mode during debugging

3. Auto-waiting is your friend!


