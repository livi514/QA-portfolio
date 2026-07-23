# HTTP Request Methods

HTTP methods define the type of operation a client wants to perform on a resource. REST APIs use these methods to implement CRUD (Create, Read, Update, Delete) operations.

## The five core methods

**GET** — retrieve a resource. Does not change server state. The most commonly used method.
```python
response = requests.get(f"{BASE_URL}/users/1")
```

**POST** — send data to the server to create a new resource. Each invocation may produce a different result.
```python
response = requests.post(f"{BASE_URL}/users", json={"name": "John"})
```

**PUT** — completely replace an existing resource. Must include the full resource representation in the request body.
```python
response = requests.put(f"{BASE_URL}/users/1", json={"name": "Jane", "email": "jane@example.com"})
```

**PATCH** — partially update an existing resource. Only the fields included in the request body are changed, unlike PUT which replaces everything.
```python
response = requests.patch(f"{BASE_URL}/users/1", json={"name": "Jane"})
```

**DELETE** — remove a resource from the server.
```python
response = requests.delete(f"{BASE_URL}/users/1")
```

## Safe and idempotent

Two important properties of HTTP methods:

- **Safe** — the operation does not change server state (read-only)
- **Idempotent** — making the same request multiple times produces the same result

| Method | Safe? | Idempotent? |
|:-------|:------|:------------|
| GET | Yes | Yes |
| POST | No | No |
| PUT | No | Yes |
| PATCH | No | No |
| DELETE | No | Yes |

PUT is idempotent because replacing a resource with the same data 100 times leaves the server in the same state. POST is not idempotent because each call could create a new resource.

## Other methods

HEAD, OPTIONS, TRACE, and CONNECT exist but are rarely used in API testing. HEAD returns only headers without a response body, OPTIONS returns a list of supported methods, and TRACE/CONNECT are used for diagnostics and proxying respectively.

## Applied to my week 4 tests

In my week 4 API test suite I covered all five core methods against the JSONPlaceholder API: GET for retrieving users and posts, POST for creating new resources, PUT for full replacements, PATCH for partial updates, and DELETE for removing resources.