# QA Summer Roadmap - Week 4

## Introduction 

Week 4 of my QA Summer Roadmap focuses on API testing. I used the pytest and request libraries in Python to build a test suite against the JSONPlaceholder mock API (https://jsonplaceholder.typicode.com/).

This was a significant shift from the UI testing I did in weeks 1-3. UI tests are all about interacting with the browser: clicking buttons, filling forms, and checking what's visible. API tests skip all of that and talk directly to the backend using HTTP requests, giving you a much clearer picture of how the system behaves underneath the UI.

My initial goals were to build a small automated API test suite validating status codes and JSON structure. I had worked with APIs before, but never through a testing or QA lens. By the end of the week I had gone well beyond those goals, covering CRUD operations, negative tests, performance checks, and security header validation.

## What I tested

I started with full CRUD coverage for /users and /posts, validating not just status codes, but the actual JSON structure (names, emails, nested address fields, and many more). This made the tests feel much closer to what you'd write against a real production API.

I also tested the relationship between users and posts, using both nested URLs (/users/1/posts) and query parameters (/posts?userId=1) to retrieve the same data through different URL patterns, and verifying that both approaches returned consistent results.

Then I added negative tests. Mock APIs don't always behave realistically. For example, JSONPlaceholder returns 200 for deleting a non-existent resource, 201 for POSTs with missing or invalid fields, and 500 for PUT to a non-existent resource. I documented these quirks throughout the test suite and used skipped tests to record scenarios that couldn't be meaningfully tested against this API.

Finally, I added simple performance checks to verify that key endpoints respond within one second, and security tests to check for headers like X-Content-Type-Options and Strict-Transport-Security. Most security headers are absent, which is expected for a mock API, but the exercise gave me a clear picture of what a secure API should include.

## What I learned 

### Recapping key API concepts 

Since I had worked with APIs before, I was already familiar with concepts like CRUD operations and HTTP response codes. This week was a good opportunity to revisit those from a testing perspective. One concept I clarified was the difference between PUT and PATCH — PUT requires the full resource in the request body, while PATCH only requires the fields being changed. Sending a partial body to PUT is wrong by design.

I also revisited safe and idempotent methods. DELETE is idempotent — deleting the same resource 100 times leaves the server in the same state — but it is not safe, because it changes server state. JSONPlaceholder's behaviour of returning 200 for DELETE /users/999 (a non-existent resource) is interesting: on a real API, a second delete would return 404, which would technically break status code idempotency even though the end state is identical. This is a good example of how mock APIs don't always reflect how a real API behaves.

### The three layers of API validation 

A good API test checks more than just the status code. There are three layers of validation:

**1. Status code:** did the request succeed or fail as expected?
```python
assert response.status_code == 200
```

**2. Response structure:** does the response contain the expected fields with the right types?
```python
user = response.json()
assert "id" in user
assert isinstance(user["id"], int)
assert isinstance(user["name"], str)
```

**3. Response values:** do the field values match what you expect?
```python
assert user["id"] == 1
assert user["name"] == "Leanne Graham"
assert user["address"]["city"] == "Gwenborough"
```

Checking structure separately from values is useful because it catches cases where a field is missing entirely, rather than just having the wrong value.

### What security headers are and why they matter

One completely new concept to me this week was testing security headers. These are HTTP response headers that instruct the client on how to handle the API's content, and interact with the server securely. For example, X-Content-Type-Options: nosniff prevents MIME type sniffing, X-Frame-Options protects against clickjacking, and Strict-Transport-Security enforces HTTPS connections and prevents downgrade attacks.

JSONPlaceholder only returns X-Content-Type-Options, while the others are absent. This was expected for a mock API, but understanding what each header does and why it matters gave me a clearer picture of what to look for when testing a real production API.

## Key takeaways from this week 

### What a poorly-behaved API looks like 

While using a mock API limited me in some ways, it was a valuable exercise in recognising poor API behaviour. For example, JSONPlaceholder sometimes returned unexpected response codes (for example, 500 on PUT to a non-existent resource), lacked input validation (accepting missing or incorrectly typed fields without complaint), and was missing several security headers. Identifying and documenting these issues is exactly what a QA engineer would do on a real project. The mock API just made the problems more visible.

### Skipped tests as a testing tool 

When JSONPlaceholder returned 201 for POSTs with missing or invalid fields, I couldn't write meaningful negative tests against it. Rather than omitting those scenarios entirely, I used @pytest.mark.skip with explanations to document what should be tested on a real API. Documenting what can't be tested, and why, is just as valuable as the tests themselves.

### Purposes of API vs UI testing 

Working at the UI layer only shows you the surface of an application. API testing exposes everything underneath: the data, the behaviour, and the edge cases you’d never see through the browser. 

API tests are also faster and more stable than UI tests since there's no browser overhead or rendering to wait for. The trade-off is that failures are harder to diagnose without a solid understanding of the data model, which makes knowing the API well an essential part of testing it effectively.

## How to run the tests

For full setup and installation instructions, see the main README.

Ensure you are running commands from the `week-4-api-testing` folder. 

Use `cd week-4-api-testing` to navigate to the folder if necessary.

Run all tests: `pytest`

Run a specific test file: `pytest tests/test_users.py`