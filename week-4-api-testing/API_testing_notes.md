# API Testing with pytest and requests

## What is an API?

An API (Application Programming Interface) is a way for two software systems to communicate with each other. It defines the rules and structure for how requests should be made and how responses will be returned. It is essentially a contract between a client and a server.

In web development, APIs are typically used to:
- Expose data from a database to a frontend application
- Allow third-party services to integrate with your application
- Enable different parts of a system to communicate (e.g. a mobile app talking to a backend)
- Share functionality between teams or organisations without exposing internal code

The most common type in modern web development is a **REST API**, which uses standard HTTP methods (GET, POST, PUT, PATCH, DELETE) to perform operations on resources. Resources are typically represented as JSON.

## How a REST API works

A client sends an HTTP request to a URL (called an endpoint), and the server returns a response. The response includes a status code indicating success or failure, and usually a JSON body containing the requested data.

For example:

```
GET https://jsonplaceholder.typicode.com/users/1
```

Returns:
```json
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz"
  ...
}
```

The client (your test, a browser, a mobile app) doesn't need to know anything about how the server stores or processes the data, it just sends a request and handles the response.


## What is API testing?

API testing verifies that an API functions as intended, meets its specifications, and handles errors gracefully. Unlike UI testing, which automates a browser and checks what a user sees, API testing communicates directly with the server: no browser, no locators, no waiting for elements to render. You send an HTTP request and validate the response.

This makes API tests faster, more stable, and less brittle than UI tests. They're also closer to the business logic, since they test what the server actually does rather than how it looks.

## Types of API testing

- **Functional testing:** validates that the API handles requests correctly and returns the expected response
- **Integration testing:** ensures the API works correctly with other components (databases, third-party services)
- **Performance testing:** evaluates the API under load (high traffic, concurrent requests)
- **Security testing:** checks for vulnerabilities and ensures compliance with security requirements
- **Negative testing:** verifies that the API handles invalid input and edge cases gracefully

## Getting started with API testing

To start API testing you need three things: an API to test, a way to send requests, and a framework for writing and running tests.

### Choosing an API

For learning purposes, public APIs are a great starting point. I used **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`), a free, fake REST API designed specifically for testing and prototyping. It provides realistic resources (users, posts, comments, todos, albums, photos) and supports all HTTP methods, though it doesn't actually persist any changes.

### Sending requests: the `requests` library

Python's `requests` library is the standard choice for making HTTP calls in tests. Install it with:

```
pip install requests
```

A basic request looks like this:

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1")
print(response.status_code)  # 200
print(response.json())       # {'id': 1, 'name': 'Leanne Graham', ...}
```

### Writing tests: pytest

pytest works for API tests with no changes from UI testing: no browser, no page objects, no fixtures required to get started. The simplest possible API test looks like this:

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_user():
    response = requests.get(f"{BASE_URL}/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert user["name"] == "Leanne Graham"
```

### Project structure

For a small API test suite, a flat structure works well:

```
week-4-api-testing/
├── tests/
│   ├── test_users.py
│   └── test_posts.py
├── test_data.py       # expected values and request payloads
├── pyproject.toml     # pytest configuration
└── README.md
```

Unlike UI testing, you typically don't need page objects or complex fixture chains. API tests are simpler by nature, so the structure can be simpler too.

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

## Best practices
- Keep tests small and focused: one test should verify one thing.
- Test all HTTP methods relevant to your API (GET, POST, PUT, PATCH, DELETE).
- Always validate status code, response structure, and response values.
- Write negative tests to verify that the API handles invalid input gracefully.
- Use descriptive assertion messages, so that failures are easy to diagnose.
- Kep test data separate from test logic.