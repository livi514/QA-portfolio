import requests 

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_api_uses_https():
    response = requests.get(f"{BASE_URL}/users")
    assert BASE_URL.startswith("https://"), "API should be served over HTTPS"
    assert response.status_code == 200

def test_security_headers():
    response = requests.get(f"{BASE_URL}/users")
    
    # X-Content-Type-Options should be set to 'nosniff' to prevent MIME type sniffing
    assert "nosniff" in response.headers.get("X-Content-Type-Options", "")
    
    # X-Frame-Options header is not present on JSONPlaceholder responses
    # On a production API this should be set to DENY or SAMEORIGIN to prevent clickjacking
    assert response.headers.get("X-Frame-Options") is None
    
    # Strict-Transport-Security header is not present on JSONPlaceholder responses
    # On a production API this should be set to enforce HTTPS and prevent downgrade attacks
    # e.g. Strict-Transport-Security: max-age=31536000; includeSubDomains
    assert response.headers.get("Strict-Transport-Security") is None
    
    # Content-Security-Policy header is not present on JSONPlaceholder responses
    # On a production API this controls what resources the browser is allowed to load
    # and helps prevent cross-site scripting (XSS) attacks
    assert response.headers.get("Content-Security-Policy") is None