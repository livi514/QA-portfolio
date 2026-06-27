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

Working with SauceDemo because it's intentionally built for testing:
https://www.saucedemo.com/

## The structure of a UI test:

Every UI test follows the same mental model:
1. Arrange: set up the browser and go to the page 
2. Act: interact with the page (click, type, select)
3. Assert: check results

## ARRANGE — Opening the browser + navigating

In Playwright, this is the minimal setup:

def test_example(page):
    page.goto("https://www.saucedemo.com/")


What’s happening?
- page is a fresh browser tab
- goto() loads a URL
- Playwright waits for the page to finish loading