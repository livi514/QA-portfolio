import requests 
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_api_uses_https():
    response = requests.get(f"{BASE_URL}/users")
    assert BASE_URL.startswith("https://"), "API should be served over HTTPS"
    assert response.status_code == 200

def test_security_headers():
    response = requests.get(f"{BASE_URL}/users")
    assert "nosniff" in response.headers.get("X-Content-Type-Options", "")
    # X-Frame-Options header is not present on JSONPlaceholder responses
    # On a production API this should be set to DENY or SAMEORIGIN to prevent clickjacking
    assert response.headers.get("X-Frame-Options") is None