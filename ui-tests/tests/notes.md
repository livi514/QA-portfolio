# Week 1 - Playwright Fundamentals 

## What is Playwright?
- Playwright Test is an end-to-end test framework for modern web apps.
- It bundles test runner, assertions, parallelization, and rich tooling.
- Playwright supports Chromium, WebKit, and Firefox on Windows, Linux, and macOS, locally or in CI, headless or header, with native mobile emulation for Chrome (Android) and Mobile Safari.
- Playwright supports programming languages like JavaScript, TypeScript, .NET, Python, C#, and Java, though its main API was originally written in Node.js.
- It was developed by Microsoft.

## Features of Playwright

- **Auto-wait**: Playwright waits for elements to be actionable prior to performing actions. It also has a rich set of introspection events. The combination of the two eliminates the need for artificial timeouts - the primary cause of flaky tests (tests which sometimes pass and sometimes fail, without any changes to the code or test itself).
- **Web-first assertions**: Playwright assertions are created specifically for the dynamic web. Checks are automatically retried until the necessary conditions are met.
- **Tracing**: Configure test retry strategy, capture execution trace, videos, screenshots, to eliminate flakes.
- Test scenarios can span multiple tabs, multiple origins, and multiple users. You can create scenarios with different contexts for different users and run them against your server, all in one test.
- **Trusted events**: Hover elements, interact with dynamic controls, produce trusted events. Playwright uses real browser input pipelines indistinguishable from the real user.
- **Test frames, pierce Shadow DOM**: Playwright selectors pierce shadow DOM and allow entering frames seamlessly.
- **Full isolation** Browser contexts - Playwright creates a browser context for each test. Browser context is equivalent to a brand new browser profile. This delivers full test isolation with zero overhead. Creating a new browser context onlhy takes a handful of milliseconds.
- **Log in once**: Save the authentication state of the context and reuse it in all the tests. This bypasses repetitive log-in operations in each test, yet delivers full isolation of independent tests.
- **Codegen**: Generate tests by recording your actions. Save them into any language.
- **Playwright inspector**: inspect page, generate selectors, step through the test execution, see click points, explore execution logs.
- **Trace viewer**: Capture all the information to investigate the test failure. Playwright trace contains test execution screencast, live DOM snapshots, action explorer, test source, and many more.


## Playwright for Python 

I decided to learn Playwright for Python as I have most experience with Python as a programming language.
I used this documentation for reference: https://playwright.dev/python/docs/writing-tests
I also followed these YouTube tutorials: https://www.youtube.com/watch?v=FK_5SQPq6nY&list=PLYDwWPRvXB8_W56h2C1z5zrlnAlvqpJ6A&index=3


## Writing tests

Playwright tests are simple. They:
- perform actions 
- assert the state against expectations 

No need to deal with...
- anything prior to performing an action: Playwright automatically waits for the wide range of actionability checks to pass prior to performing each action.
- race conditions when performing the checks: Playwright assertions are designed in a way that they describe the expectations that need to be eventually met.

## Actions

### Navigation 
To navigate to a specified URL:
page.goto("https://playwright.dev/")
Playwright will wait for the page to reach the load state prior to moving forward.

The method will throw an error if:
- there's an SSL eror (e.g. in the case of self-signed certificates)
- target URL is invalid
- the timeout is exceeded during navigation
- the remote server does not respond or is unreachable 
- the main resource failed to load
The method will not throw an error when any valid HTTP status code is returned, including 404 and 500.
The status codes for such responses can be retrieved by calling response.status.
The goto method either throws an error or returns a main resource response. The only exceptions are navigation to about:blank or navigation to the same URL with a different hash, which would succeed and return null.


### Interactions 
Performing actions starts with locating the elements. Playwright uses Locators API for that.
Locators represent a way to find element(s) on the page at any moment.
Playwright will wait for the element to be actionable prior to performing the action, so there is no need to wait for it to become available.

Create a locator:
get_started = page.get_by_role("link", name="Get started")

Click it:
get_started.click()

In most cases, it'll be written in one line:
page.get_by_role("link", name="Get started").click()

Basic actions:
- **locator.check()**: check the input checkbox
- **locator.click()**: click the element
- **locator.uncheck()**: uncheck the input checkbox
- **locator.hover()**: hover mouse over the element
- **locator.fill()**: fill the form field, input text
- **locator.focus()**: focus the element
- **locator.press()**: press single key
- **locator.set_input_files()**: pick files to upload
- **locator.select_option()**: select option in the drop down

### Assertions
Playwright includes assertions that will wait until the expected condition is met.
Using these assertions allows making the tests non-flaky and resilient.
Most popular async assertions:
- **expect(locator).to_be_checked()**: checkbox is checked
- **expect(locator).to_be_checked()**: control is enabled
- **expect(locator).to_be_visible()**: element is visible
- **expect(locator).to_contain_text()**: element contains text
- **expect(locator).to_have_attribute()**: element has attribute
- **expect(locator).to_have_count()**: list of elements has given length
- **expect(locator).to_have_text()**: element matches text
- **expect(locator).to_have_value()**: input element has value
- **expect(page).to_have_title()**: page has title
- **expect(page).to_have_url()**: page has url
