# QA Summer Roadmap - Week 4

## Introduction 

Week 4 of my QA Summer Roadmap focuses on API testing. I used the pytest and request libraries in Python to build a test suite against the JSONPlaceholder mock API (https://jsonplaceholder.typicode.com/).

This was a big change from the UI testing I did in weeks 1-3. UI tests are all about interacting with the browser: clicking buttons, filling forms, and checking what's visible. API tests skip all of that and talk directly to the backend using HTTP requests. This gives you a much better sense of how the system behaves underneath the UI.

My goals for this week were to build a small automated API test suite, validating status codes as well as JSON structure. I had worked with APIs before, but never through a testing or QA lens.
However, I achieved much more than I had initially set out to do: I explored CRUD operations, negative tests, as well as performance and security checks. 

This week gave me a much clearer sense of how the backend actually works nd how UI and API tests fit together.

## What I tested

I started with full CRUD coverage for /users and /posts, validating not just status codes, but the actual JSON structure (names, emails, nested address fields, and many more). This made the tests feel much closer to what you'd write against a real production API.

Then I added negative tests. Mock APIs don’t always behave realistically (JSONPlaceholder returns 200 for deleting a non‑existent resource and 201 for invalid POSTs), so I documented those quirks and skipped tests that would normally expect 400/404.

I also added simple performance checks to make sure key endpoints respond within one second, and a few security tests to look for headers like X-Content-Type-Options and Strict-Transport-Security. Most of them are missing, which is expected for a mock API, but it was a useful exercise in understanding what a secure API should return.

## What I learned 

### Recapping key API concepts 

Since I had worked with API methods, I was already somewhat familiar with key concepts such as CRUD operations and HTTP response codes. This week was therefore a good opportunity to review those key concepts, while looking at APIs from a new perspective: that of a software tester. One of the key concepts that I reviewed this week was the difference between the PUT and PATCH methods: I now understand why sending a partial body to PUT is wrong.

Another concept I reviewed is safe and idempotent methods. For example, the DELETE method is idempotent, meaning that if you delete the same resource 100 times, the end state is the same (the resource is gone). However, it's not safe, because it changes server state.

The interesting thing with JSONPlaceholder is that it returns 200 for DELETE /users/999 even though the resource doesn't exist. On a real API, the first delete might return 200 (or 204), but a second delete on the same resource would return 404 since it no longer exists — which would actually break idempotency in terms of status codes, even though the end state is the same.

This is a good example of how mock APIs don't always match how a real API would work in a given scenario.

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

One completely new concept to me this week was testing security headers. I learned that security headers are HTTP response headers that instruct the client on how to handle the API's content and interact with the server securely.

I tested the JSONPlaceholder API for security headers such as X-Content-Type-Options and Strict-Transport-Security. Most of them are missing, which is expected for a mock API, but it was a useful exercise in understanding what a secure API should return.


## Key takeaways from this week 

### What a poorly-behaved API looks like 

While using a mock API limited me in some ways, it was an interesting learning experience in how a poorly behaved API looks like. For example, JSONPlaceholder sometimes returned unexpected response codes, such as 500 on PUT to a non-existent resource. As well as this, it lacked input validation as well as some security headers. However, this experience helped me to understand what to look for and flag in a real API.

### Skipped tests as a testing tool 

One issue I faced with JSONPlaceholder was that it didn't validate missing or invalid input in PUT operations. However, this became a valuable lesson in how to use skipped tests with explanations, to document missing logic. When something cannot be tested due to missing logic, documenting what should be tested is just as valuable.

### Purposes of API vs UI testing 

Working at the UI layer only shows you the surface of an application. API testing exposes everything underneath: the data, the behaviour, and the edge cases you’d never see through the browser. 

API testing is faster and more stable than UI testing, but tests closer to the business logic means failures are harder to diagnose without understanding the data model.

## How to run the tests

For full setup and installation instructions, see the main README.

Ensure you've set up env and navigated to the week-4-api-testing folder before running tests.

Run all tests: `pytest`

Run a specific test file: `pytest tests/test_users.py`