import requests 
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.mark.parametrize("endpoint", [
    "/users",
    "/users/1",
    "/posts",
    "/posts/1",
    "/users/1/posts",
])
def test_response_time(endpoint):
    """Test that the response time of crucial endpoints does not exceed one second."""
    response = requests.get(f"{BASE_URL}{endpoint}")
    assert response.elapsed.total_seconds() < 1.0, \
        f"{endpoint} took {response.elapsed.total_seconds():.2f}s"