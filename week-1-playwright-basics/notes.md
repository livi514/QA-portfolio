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

### Test isolation 

The Playwright Pytest plugin is based on the concept of text fixtures such as the built in page fixture, which is passed into your test.
Pages are isolated between tests due to the Browser Context, which is equivalent to a brand new browser profile, where every test gets a fresh environment, even when multiple tests run in a single browser.

### Using fixtures

You can use various fixtures to execute code before or after your tests and to share objects between them.

A function scoped fixture e.g. with autouse behaves like a beforeEach/afterEach. And a module scoped fixture with autouse behaves like a beforeAll/afterAll which runs before all and after all the tests.

import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    
    print("before the test runs")

    # Go to the starting url before each test.
    page.goto("https://playwright.dev/")
    yield
    
    print("after the test runs")

def test_main_navigation(page: Page):
    # Assertions use the expect API.
    expect(page).to_have_url("https://playwright.dev/")

# Running and debugging tests

You can run a single test, a set of tests, or all tests.
Tests can be run on one browser or multiple browsers by using the --browser flag.
By default, tests are run in a headless manner.
- Running tests headless means executing automated browser tests without a visible graphical user interface.
- Running tests headed means executing the tests in a real, visible browser window that renders every frame.

Headless mode is faster and uses fewer resources, making it the industry standard for CI/CD pipelines and large regression suites. Headed mode is best utilized for local debugging, visually verifying UI interactions, and test development.

If running tests in a headless manner, the results will be shown in the terminal.
If you prefer, you can run your tests in headed mode by using the --headed CLI argument.

## Running tests

### Command Line 

To run your tests, use the pytest command. This will run your tests on the Chromium browser by default. Tests run in headless mode by default meaning no browser window will be opened while running the tests and results will be seen in the terminal.

pytest

### Run tests in headed mode

To run your tests in headed mode, use the --headed flag. This will open up a browser window while running your tests and once finished the browser window will close.

pytest --headed

### Run tests on different browsers

To specify which browser you would like to run your tests on, use the --browser flag followed by the name of the browser.

pytest --browser webkit

To specify multiple browsers to run your tests on, use the --browser flag multiple times followed by the name of each browser.

pytest --browser webkit --browser firefox

### Run specific tests

To run a single test file, pass in the name of the test file that you want to run.

pytest test_login.py

To run a set of test files, pass in the names of the test files that you want to run.

pytest tests/test_todo_page.py tests/test_landing_page.py

To run a specific test, pass in the function name of the test you want to run.

pytest -k test_add_a_todo_item
