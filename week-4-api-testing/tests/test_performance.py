import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
PERFORMANCE_THRESHOLD_SECONDS = 5.0


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
    Test that key endpoints respond within a realistic time budget for a public
    external API. The live JSONPlaceholder service is slower than a local in-memory
    API, so a 5s threshold still catches meaningful regressions without failing on
    normal network latency.
    """

    response = requests.get(f"{BASE_URL}{endpoint}")
    assert (
        response.elapsed.total_seconds() < PERFORMANCE_THRESHOLD_SECONDS
    ), f"{endpoint} took {response.elapsed.total_seconds():.2f}s"
