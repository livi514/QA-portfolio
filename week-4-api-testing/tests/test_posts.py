import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

# GET tests

def test_get_list_of_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    posts = response.json()
    assert len(posts) == 100, f"Expected 100 posts but got {len(posts)}"
    for i, post in enumerate(posts, start=1):
        assert post["id"] == i, f"Expected id == {i}, but got {post['id']}"
        assert isinstance(post["userId"], int) and post["userId"] in range(1,11)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)

def test_get_post():
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    post = response.json()
    assert post["userId"] == 1
    assert post["id"] == 1
    assert post["title"] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    assert post["body"] == "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"

def test_get_non_existent_post():
    response = requests.get(f"{BASE_URL}/posts/999")
    assert response.status_code == 404, f"Expected 404 but got {response.status_code}"
    assert response.json() == {}

def test_get_posts_by_user():
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
    response = requests.get(f"{BASE_URL}/posts?userId=1")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    posts = response.json()
    assert len(posts) == 10, f"Expected 10 posts but got {len(posts)}"
    for i, post in enumerate(posts, start=1):
        assert post["userId"] == 1, f"Expected userId == 1, but got {post['userId']}"
        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)

# POST tests

def test_create_post():
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


def test_create_post_by_user():
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

# PUT tests 

def test_replacing_post_content():
    url = f"{BASE_URL}/posts/1"
    data = {
        "userId": 1,
        "title" : "New title",
        "body" : "New body"
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]    
    post = response.json()
    assert int(post["userId"]) == 1
    assert post["id"] == 1
    assert post["title"] == "New title"
    assert post["body"] == "New body"

# PATCH tests

def test_replacing_post_title():
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
    assert post["body"] == "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"

def test_replacing_post_body():
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
    assert post["title"] == "ea molestias quasi exercitationem repellat qui ipsa sit aut"
    assert post["body"] == "New body"

# DELETE tests 

def test_deleting_post():
    url = f"{BASE_URL}/posts/4"
    response = requests.delete(url)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert response.json() == {}