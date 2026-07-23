import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

# GET tests

def test_get_list_of_posts():
    """Test that the full list of posts is returned with the correct structure."""
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    posts = response.json()
    assert len(posts) == 100, f"Expected 100 posts but got {len(posts)}"
    for i, post in enumerate(posts, start=1):
        assert post["id"] == i, f"Expected id == {i}, but got {post['id']}"
        assert isinstance(post["userId"], int) and post["userId"] in range(1, 11)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)


def test_get_post():
    """Test that a single post is returned with the correct field values."""
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert post["userId"] == 1
    assert post["id"] == 1
    assert post["title"] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    assert post["body"] == "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"


def test_get_non_existent_post():
    """Negative test: requesting a post that doesn't exist should return 404 and an empty body."""
    response = requests.get(f"{BASE_URL}/posts/999")
    assert response.status_code == 404, f"Expected 404 but got {response.status_code}"
    assert response.json() == {}


def test_get_posts_by_user():
    """Test retrieving posts for a specific user via the nested URL (/users/{id}/posts).
    Every post in the response should belong to user 1."""
    response = requests.get(f"{BASE_URL}/users/1/posts")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    posts = response.json()
    assert len(posts) == 10, f"Expected 10 posts but got {len(posts)}"
    for i, post in enumerate(posts, start=1):
        assert post["userId"] == 1, f"Expected userId == 1, but got {post['userId']}"
        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)


def test_get_posts_by_user_id():
    """Test retrieving posts for a specific user via query parameter (/posts?userId=1).
    This is an alternative approach to test_get_posts_by_user — same result, different URL pattern."""
    response = requests.get(f"{BASE_URL}/posts?userId=1")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    posts = response.json()
    assert len(posts) == 10, f"Expected 10 posts but got {len(posts)}"
    for i, post in enumerate(posts, start=1):
        assert post["userId"] == 1, f"Expected userId == 1, but got {post['userId']}"
        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)


def test_get_posts_by_user_invalid_id():
    """Negative test: querying posts for a non-existent userId.
    JSONPlaceholder returns 200 with an empty list for a non-existent userId.
    This is valid REST design — the query succeeded but found no matching results.
    A 404 would only be appropriate if the endpoint itself didn't exist."""
    response = requests.get(f"{BASE_URL}/posts?userId=999")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert response.json() == [], "Expected empty list for non-existent userId"


# POST tests

def test_create_post():
    """Test that a new post can be created and the response echoes back the correct data."""
    url = f"{BASE_URL}/posts"
    data = {
        "userId": 1,
        "title": "Example title",
        "body": "Example body"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert post["id"] == 101
    assert post["userId"] == 1
    assert post["title"] == "Example title", f"Expected 'Example title', but got {post['title']}"
    assert post["body"] == "Example body", f"Expected 'Example body', but got {post['body']}"


@pytest.mark.skip(reason="JSONPlaceholder does not validate input — POSTing with missing fields returns 201 instead of 400. On a real API, this should return 400 Bad Request.")
def test_create_post_with_missing_fields():
    pass


@pytest.mark.skip(reason="JSONPlaceholder does not validate data types — POSTing with incorrect types returns 201 instead of 400. On a real API, this should return 400 Bad Request.")
def test_create_post_with_incorrect_data_types():
    pass


def test_create_post_by_user():
    """Test creating a post via the nested user URL (/users/{id}/posts).
    Note: userId is returned as a string when posting via this endpoint — this is a JSONPlaceholder quirk."""
    url = f"{BASE_URL}/users/1/posts"
    data = {
        "title": "User 1's post",
        "body": "New post by user 1"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert post["id"] == 101
    # userId is returned as a string when posting via /users/{id}/posts
    assert int(post["userId"]) == 1
    assert post["title"] == "User 1's post", f"Expected 'User 1's post', but got {post['title']}"
    assert post["body"] == "New post by user 1", f"Expected 'New post by user 1', but got {post['body']}"


def test_create_post_by_non_existent_user():
    """Test creating a post via the nested user URL (/users/{id}/posts), where the id doesn't belong to an existing user.
    JSON placeholder allows this."""
    url = f"{BASE_URL}/users/999/posts"
    data = {
        "title": "User 999's post",
        "body": "New post by user 999"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert post["id"] == 101
    # userId is returned as a string when posting via /users/{id}/posts
    assert int(post["userId"]) == 999
    assert post["title"] == "User 999's post", f"Expected 'User 999's post', but got {post['title']}"
    assert post["body"] == "New post by user 999", f"Expected 'New post by user 99', but got {post['body']}"


# PUT tests

def test_put_replaces_post():
    """Test that PUT replaces all fields of an existing post.
    The full resource must be sent in the request body, as partial updates are not supported by PUT."""
    url = f"{BASE_URL}/posts/1"
    data = {
        "userId": 1,
        "title": "New title",
        "body": "New body"
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert int(post["userId"]) == 1
    assert post["id"] == 1
    assert post["title"] == "New title"
    assert post["body"] == "New body"

def test_put_with_other_users_id():
    "Shouldn't be allowed"
    url = f"{BASE_URL}/posts/1"
    data = {
        "userId": 2,
        "title": "New title",
        "body": "New body"
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert int(post["userId"]) == 2
    assert post["id"] == 1
    assert post["title"] == "New title"
    assert post["body"] == "New body"

def test_put_with_invalid_user_id():
    "Shouldn't be allowed."
    url = f"{BASE_URL}/posts/1"
    data = {
        "userId": 999,
        "title": "New title",
        "body": "New body"
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert int(post["userId"]) == 999
    assert post["id"] == 1
    assert post["title"] == "New title"
    assert post["body"] == "New body"

def test_put_non_existent_post():
    """Negative test: PUTting to a non-existent post.
    According to the REST spec, PUT to a non-existent resource should either
    create it (201) or return 404. JSONPlaceholder returns 500, which indicates
    the server does not handle this case gracefully — this would be a bug on a real API."""
    url = f"{BASE_URL}/posts/999"
    data = {
        "userId": 1,
        "title": "New title",
        "body": "New body"
    }
    response = requests.put(url, json=data)
    assert response.status_code == 500, f"Expected 500 but got {response.status_code}"

# PATCH tests

def test_patching_post_title():
    """Test that PATCH updates only the title field, leaving all other fields unchanged."""
    url = f"{BASE_URL}/posts/2"
    data = {
        "title": "New title"
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert int(post["userId"]) == 1
    assert post["id"] == 2
    assert post["title"] == "New title"
    # body should be unchanged since it was not included in the PATCH request
    assert post["body"] == "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"


def test_patching_post_body():
    """Test that PATCH updates only the body field, leaving all other fields unchanged."""
    url = f"{BASE_URL}/posts/3"
    data = {
        "body": "New body"
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert int(post["userId"]) == 1
    assert post["id"] == 3
    # title should be unchanged since it was not included in the PATCH request
    assert post["title"] == "ea molestias quasi exercitationem repellat qui ipsa sit aut"
    assert post["body"] == "New body"


def test_patching_post_id_to_existing_post_id():
    """This is interesting. This shouldn't be allowed as there is already a post with id 5."""
    url = f"{BASE_URL}/posts/4"
    data = {
        "id": 5
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert int(post["userId"]) == 1
    assert post["id"] == 5
    assert post["title"] == "eum et est occaecati"
    assert post["body"] == "ullam et saepe reiciendis voluptatem adipisci\nsit amet autem assumenda provident rerum culpa\nquis hic commodi nesciunt rem tenetur doloremque ipsam iure\nquis sunt voluptatem rerum illo velit"


def test_patching_post_id_to_nonexistent_post_id():
    url = f"{BASE_URL}/posts/4"
    data = {
        "id": 5
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert int(post["userId"]) == 1
    assert post["id"] == 5
    assert post["title"] == "eum et est occaecati"
    assert post["body"] == "ullam et saepe reiciendis voluptatem adipisci\nsit amet autem assumenda provident rerum culpa\nquis hic commodi nesciunt rem tenetur doloremque ipsam iure\nquis sunt voluptatem rerum illo velit"


def test_patching_user_id_to_existing_user_id():
    """The API seems to essentially ignore the request and keep the userID as it currently is."""
    url = f"{BASE_URL}/posts/5"
    data = {
        "userID": 2
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert int(post["userId"]) == 1
    assert post["id"] == 5
    assert post["title"] == "nesciunt quas odio"
    assert post["body"] == "repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"

def test_patching_user_id_to_nonexistent_user_id():
    url = f"{BASE_URL}/posts/5"
    data = {
        "userID": 999
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert int(post["userId"]) == 1
    assert post["id"] == 5
    assert post["title"] == "nesciunt quas odio"
    assert post["body"] == "repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"
    

# DELETE tests

def test_deleting_post():
    """Test that DELETE returns 200 and an empty body, confirming the post was removed."""
    url = f"{BASE_URL}/posts/4"
    response = requests.delete(url)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert response.json() == {}

def test_delete_non_existent_post():
    """Negative test: deleting a non-existent post.
    JSONPlaceholder returns 200 regardless of whether the resource exists,
    since it doesn't actually persist any changes.
    On a real API, this would typically return 404."""
    response = requests.delete(f"{BASE_URL}/posts/999")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert response.json() == {}