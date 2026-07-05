# Page Object Models

Large test suites can be structured to optimise ease of authoring and maintenance. Page object models are one such approach to structure your test suite.

A page object represents a part of your web application. An e-commerce web application might have a home page, a listings page, and a checkout page. Each of them can be represented by page object models.

In other words, a page object is an abstraction of a web page using a programming language. The intention is to represent all of the page within code, so as to take action against specific elements. Page objects are used routinely in the field of test automation, where a Quality Engineer creates objects and tests for the purpose of testing application user journeys.

Page objects simplify authoring by creating a higher-level API which suits your application and simplify maintenance by capturing element selectors in one place, and create reusable code to avoid repetition.

## Implementation 

Page object models wrap over a Playwright Page.

```
class SearchPage:
    def __init__(self, page):
        self.page = page
        self.search_term_input = page.locator('[aria-label="Enter your search term"]')

    def navigate(self):
        self.page.goto("https://bing.com")

    def search(self, text):
        self.search_term_input.fill(text)
        self.search_term_input.press("Enter")
```

Page objects can then be used inside a test.

```
from models.search import SearchPage

# in the test
page = browser.new_page()
search_page = SearchPage(page)
search_page.navigate()
search_page.search("search query")
```