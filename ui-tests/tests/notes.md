# Week 1 - Playwright Fundamentals 

## What is Playwright?
- Playwright Test is an end-to-end test framework for modern web apps.
- It bundles test runner, assertions, parallelization, and rich tooling.
- Playwright supports Chromium, WebKit, and Firefox on Windows, Linux, and macOS, locally or in CI, headless or header, with native mobile emulation for Chrome (Android) and Mobile Safari.

## Playwright for Python 

I decided to learn Playwright for Python as I have most experience with Python as a programming language.
I used this documentation for reference: https://playwright.dev/python/docs/writing-tests

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
