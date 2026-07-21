import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_user():
    response = requests.get(f"{BASE_URL}/users/1")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]    
    user = response.json()
    assert user["id"] == 1
    assert user["name"] == "Leanne Graham", f"Expected 'Leanne Graham' but got {user['name']}"
    assert user["username"] == "Bret", f"Expected 'Bret' but got {user['username']}"
    assert user["email"] == "Sincere@april.biz", f"Expected 'Sincere@april.biz', but got {user['email']}"
    assert user["address"]["street"] == "Kulas Light", f"Expected 'Kulas Light', but got {user['address']['street']}"
    assert user["address"]["city"] == "Gwenborough", f"Expected 'Gwenborough', but got {user['address']['city']}"
    assert user["address"]["zipcode"] == "92998-3874", f"Expected '92998-3874', but got {user['address']['zipcode']}"
    assert user["phone"] == "1-770-736-8031 x56442", f"Expected '1-770-736-8031 x56442', but got {user['phone']}"
    assert user["website"] == "hildegard.org", f"Expected 'hildegard.org', but got {user['website']}"
    assert user["company"]["name"] == "Romaguera-Crona", f"Expected 'Romaguera-Crona', but got {user['company']['name']}"


