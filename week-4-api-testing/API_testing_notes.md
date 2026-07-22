# API Testing with pytest and requests

In this digital age, APIs have become the cornerstone of how data is shared and processed. This is why it's important to leverage API testing techniques to ensure that every aspect of your website or application works as expected.

# What is an API?

APIs (Application Programming Interfaces) are designed for developers to use. They are a coding tool that allows your application to communicate with other applications. APIs allow you to integrate third-party applications into your work, or use your own data and processes in the cloud.

In today's development process, APIs have become an essential part in web and mobile applications.

When dealing with APIs, you need to be sure that everything works together properly, before integrating the API into your applications. That's why testing them is essential. 

## What is API testing?

API testing verifies that an API functions as intended, meets its specifications, and handles errors gracefully. Unlike UI testing, which automates a browser and checks what a user sees, API testing communicates directly with the server: no browser, no locators, no waiting for elements to render. You send an HTTP request and validate the response.

This makes API tests faster, more stable, and less brittle than UI tests. They're also closer to the business logic, since they test what the server actually does rather than how it looks.

## API testing principles

Having a standard set of rules is the best way to ensure the quality of your APIs and their implementation.
1. API testing should be a part of yoru continuous integration and delivery pipeline.
2. API tests should be easy to maintain and write.
3. A well-designed API will make your tests easier to write.
4. You should test at the boundary of your system.
5. Keep your tests small and focused.
6. Make sure your tests are deterministic.
7. Run your tests in parallel for speed.
8. Use the available and freely-accessible tools to simplify API testing.

## Types of API testing

- **Functional testing:** validates that the API handles requests correctly and returns the expected response
- **Integration testing:** ensures the API works correctly with other components (databases, third-party services)
- **Performance testing:** evaluates the API under load (high traffic, concurrent requests)
- **Security testing:** checks for vulnerabilities and ensures compliance with security requirements
- **Negative testing:** verifies that the API handles invalid input and edge cases gracefully

## How to start API testing

To get started with API testing, you will need to have access to an application with an exposed API. You will also need to choose a method for sending requests to the API (manual or automated), and select a tool or framework for writing your tests (if using automated testing).

Once you have these things set up, you can begin writing your test cases and running them against the API.

## API testing tips

API testing can be a challenge, but regardless of the tools you decide to use, here are some tips that can help:
1. Make sure you have a clear understanding of the API before you start testing. Read the documentation and any other available materials. This will help you know what to expct and how the API should work.
2. Use API testing tools: This will give you a better understanding of how the API works and make it easier to find any issues.
3. Test all aspects of the API, including input validation, error handling, and security.
4. Keep your tests up-to-date as the API changes.

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