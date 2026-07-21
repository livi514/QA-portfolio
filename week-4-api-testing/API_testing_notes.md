# API Testing with pytest and requests

## What is API testing?

API testing verifies that an API functions as intended, meets its specifications, and handles errors gracefully. Unlike UI testing, which automates a browser and checks what a user sees, API testing communicates directly with the server: no browser, no locators, no waiting for elements to render. You send an HTTP request and validate the response.

This makes API tests faster, more stable, and less brittle than UI tests. They're also closer to the business logic, since they test what the server actually does rather than how it looks.

## Types of API testing

- **Functional testing:** validates that the API handles requests correctly and returns the expected response
- **Integration testing:** ensures the API works correctly with other components (databases, third-party services)
- **Performance testing:** evaluates the API under load (high traffic, concurrent requests)
- **Security testing:** checks for vulnerabilities and ensures compliance with security requirements
- **Negative testing:** verifies that the API handles invalid input and edge cases gracefully

## HTTP response status codes

Status codes are three-digit numbers indicating the outcome of a request:

| Range | Category |
|:------|:---------|
| 1xx | Informational |
| 2xx | Success |
| 3xx | Redirection |
| 4xx | Client errors |
| 5xx | Server errors |

Most commonly used in testing:

| Code | Meaning |
|:-----|:--------|
| 200 | OK — request succeeded |
| 201 | Created — resource successfully created |
| 204 | No Content — request succeeded, no body returned |
| 400 | Bad Request — invalid request from the client |
| 401 | Unauthorised — authentication required |
| 404 | Not Found — resource doesn't exist |
| 500 | Internal Server Error — something went wrong on the server |

## What to validate in an API test

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

## The `requests` library

`requests` is Python's standard HTTP library for making API calls. It's simple, readable, and widely used in professional API testing.

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1")
```

Key methods:

| Method | HTTP verb | Use case |
|:-------|:----------|:---------|
| `requests.get(url)` | GET | Retrieve a resource |
| `requests.post(url, json=data)` | POST | Create a resource |
| `requests.put(url, json=data)` | PUT | Replace a resource |
| `requests.patch(url, json=data)` | PATCH | Update part of a resource |
| `requests.delete(url)` | DELETE | Delete a resource |

Key response attributes:

```python
response.status_code   # e.g. 200
response.json()        # parses the response body into a Python dictionary
response.headers       # response headers (e.g. Content-Type)
response.text          # raw response body as a string
```

`response.json()` is the most important one — it converts the JSON response body into a Python dictionary you can assert against:

```python
user = response.json()
assert user["name"] == "Leanne Graham"
assert user["address"]["city"] == "Gwenborough"  # nested fields use chained brackets
```

## Difference between UI and API testing

| | UI Testing (Playwright) | API Testing (requests) |
|:--|:--|:--|
| What's tested | What the user sees in the browser | What the server returns |
| Tools | Playwright, page objects, locators | requests, JSON assertions |
| Speed | Slower (browser overhead) | Much faster |
| Stability | More brittle (UI changes break tests) | More stable |
| Closest to | User experience | Business logic |

## Why pytest for API testing?

I've already been using pytest for UI tests: the same framework works for API tests with no changes. The same features apply: fixtures, parametrize, markers, conftest.py. The only difference is that instead of using a `page` fixture, you just call `requests` directly.