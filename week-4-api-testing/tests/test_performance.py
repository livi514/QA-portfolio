import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.mark.parametrize(
    "endpoint",
    [
        "/users",
        "/users/1",
        "/posts",
        "/posts/1",
        "/users/1/posts",
    ],
)
def test_response_time(endpoint):
    """
    Test that the response time of crucial endpoints does not exceed 1.5.
    1.5 seconds is a reasonable threshold for a public API under normal conditions.
    On a real project this threshold would be defined in performance requirements
    """

    response = requests.get(f"{BASE_URL}{endpoint}")
    assert (
        response.elapsed.total_seconds() < 1.5
    ), f"{endpoint} took {response.elapsed.total_seconds():.2f}s"
