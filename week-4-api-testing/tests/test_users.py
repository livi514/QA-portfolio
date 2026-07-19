import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_user():
    response = requests.get(f"{BASE_URL}/users/1")
    assert response.status_code == 200
    
    user = response.json()
    assert user["id"] == 1
    assert user["name"] == "Leanne Graham"
    assert user["username"] == "Bret"
    assert user["email"] == "Sincere@april.biz"
    assert user["address"]["street"] == "Kulas Light"
    assert user["address"]["city"] == "Gwenborough"
    assert user["address"]["zipcode"] == "92998-3874"
    assert user["phone"] == "1-770-736-8031 x56442"
    assert user["website"] == "hildegard.org"
    assert user["company"]["name"] == "Romaguera-Crona"