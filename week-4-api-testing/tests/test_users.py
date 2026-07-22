import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

# GET tests 

def test_get_list_of_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]
    users = response.json()
    assert len(users) == 10, f"Expected 10 users but got {len(users)}"
    for i, user in enumerate(users, start=1):
        assert user["id"] == i, f"Expected id == {i}, but got {user['id']}"
        assert isinstance(user["name"], str)
        assert isinstance(user["username"], str)
        assert isinstance(user["email"], str)
        assert isinstance(user["address"]["street"], str)
        assert isinstance(user["address"]["city"], str)
        assert isinstance(user["address"]["zipcode"], str)
        assert isinstance(user["phone"], str)
        assert isinstance(user["website"], str)
        assert isinstance(user["company"]["name"], str)
        
# retrieve an existing user
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

# negative test: retrieve a non-existent user
def test_get_non_existent_user():
    response = requests.get(f"{BASE_URL}/users/999")
    assert response.status_code == 404, f"Expected 404 but got {response.status_code}"
    assert response.json() == {}

# POST tests

def test_create_user():
    '''
    Note: JSONPlaceholder doesn't actually persist the created user, so a follow-up GET /users/11 would return 404. 
    The POST response simulates what would be returned if the API were real.
    '''
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "John Doe",
        "username": "john123",
        "email": "johndoe123@somebusiness.com",
        "address" : {
            "street": "Sample Street",
            "suite": "Apt. 1",
            "city": "Sample City",
            "zipcode": "123456",
            "geo" : {
                "lat": "-12.3456",
                "lang": "78.9123"
            }
        },
        "phone" : "12345678910",
        "website" : "john.com",
        "company" : {
            "name" : "Some Business",
            "catchPhrase" : "We do things",
            "bs" : "Nobody knows what we do but it is something"
        },
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]    
    user = response.json()
    assert user["id"] == 11
    assert user["name"] == "John Doe", f"Expected 'John Doe' but got {user['name']}"
    assert user["username"] == "john123", f"Expected 'john123' but got {user['username']}"
    assert user["email"] == "johndoe123@somebusiness.com", f"Expected 'johndoe123@somebusiness.com', but got {user['email']}"
    assert user["address"]["street"] == "Sample Street", f"Expected 'Sample Street', but got {user['address']['street']}"
    assert user["address"]["city"] == "Sample City", f"Expected 'Sample City', but got {user['address']['city']}"
    assert user["address"]["zipcode"] == "123456", f"Expected '123456', but got {user['address']['zipcode']}"
    assert user["phone"] == "12345678910", f"Expected '12345678910', but got {user['phone']}"
    assert user["website"] == "john.com", f"Expected 'john.com', but got {user['website']}"
    assert user["company"]["name"] == "Some Business", f"Expected 'Some Business', but got {user['company']['name']}"

@pytest.mark.skip(reason="JSONPlaceholder does not validate input — POSTing with missing fields returns 201 instead of 400. On a real API, this should return 400 Bad Request.")
def test_create_user_with_missing_fields():
    pass

# PUT tests 

def test_replacing_user():
    url = f"{BASE_URL}/users/1"
    data = {
        "name": "Jane Doe",
        "username": "jane123",
        "email": "janedoe123@somebusiness.com",
        "address" : {
            "street": "Sample Street",
            "suite": "Apt. 1",
            "city": "Sample City",
            "zipcode": "123456",
            "geo" : {
                "lat": "-12.3456",
                "lang": "78.9123"
            }
        },
        "phone" : "10987654321",
        "website" : "jane.com",
        "company" : {
            "name" : "Some Business",
            "catchPhrase" : "We do things",
            "bs" : "Nobody knows what we do but it is something"
        },
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]    
    user = response.json()
    assert user["id"] == 1
    assert user["name"] == "Jane Doe", f"Expected 'Jane Doe' but got {user['name']}"
    assert user["username"] == "jane123", f"Expected 'jane123' but got {user['username']}"
    assert user["email"] == "janedoe123@somebusiness.com", f"Expected 'janedoe123@somebusiness.com', but got {user['email']}"
    assert user["address"]["street"] == "Sample Street", f"Expected 'Sample Street', but got {user['address']['street']}"
    assert user["address"]["city"] == "Sample City", f"Expected 'Sample City', but got {user['address']['city']}"
    assert user["address"]["zipcode"] == "123456", f"Expected '123456', but got {user['address']['zipcode']}"
    assert user["phone"] == "10987654321", f"Expected '10987654321', but got {user['phone']}"
    assert user["website"] == "jane.com", f"Expected 'jane.com', but got {user['website']}"
    assert user["company"]["name"] == "Some Business", f"Expected 'Some Business', but got {user['company']['name']}"

# PATCH tests 

def test_patching_user():
    url = f"{BASE_URL}/users/2"
    data = {
        "name": "Eva Howell",
        "email": "eva123@melissa.tv",
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert "application/json" in response.headers["Content-Type"]    
    user = response.json()
    assert user["id"] == 2
    assert user["name"] == "Eva Howell", f"Expected 'Eva Howell' but got {user['name']}"
    assert user["username"] == "Antonette", f"Expected 'Antonette' but got {user['username']}"
    assert user["email"] == "eva123@melissa.tv", f"Expected 'eva123@melissa.tv', but got {user['email']}"
    assert user["address"]["street"] == "Victor Plains", f"Expected 'Victor Plains', but got {user['address']['street']}"
    assert user["address"]["city"] == "Wisokyburgh", f"Expected 'Wisokyburgh', but got {user['address']['city']}"
    assert user["address"]["zipcode"] == "90566-7771", f"Expected '90566-7771', but got {user['address']['zipcode']}"
    assert user["phone"] == "010-692-6593 x09125", f"Expected '010-692-6593 x09125', but got {user['phone']}"
    assert user["website"] == "anastasia.net", f"Expected 'anastasia.net', but got {user['website']}"
    assert user["company"]["name"] == "Deckow-Crist", f"Expected 'Deckow-Crist', but got {user['company']['name']}"

# DELETE tests 

def test_deleting_user():
    url = f"{BASE_URL}/users/3"
    response = requests.delete(url)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert response.json() == {}