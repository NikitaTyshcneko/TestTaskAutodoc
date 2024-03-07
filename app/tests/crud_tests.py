from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_refresh_token():
    response = client.post("/api/v1/refresh-token/")
    assert response.status_code == 401


def test_user_login():
    response = client.post("/api/v1/user/login/", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 404

def test_get_by_id():
    response = client.get("/api/v1/user/get/?id=1")
    assert response.status_code == 200

def test_get_all_user():
    response = client.get("/api/v1/user/getall/")
    assert response.status_code == 200

def test_add_user():
    response = client.post("/api/v1/user/register/", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200

def test_update_user():
    response = client.put("/api/v1/user/update/", json={"username": "test_user", "password": "updated_password"})
    assert response.status_code == 200

# Test cases for /api/v1/user/delete/ endpoint
def test_delete_user():
    response = client.delete("/api/v1/user/delete/")
    assert response.status_code == 200

def test_get_by_id_item():
    response = client.get("/api/v1/item/get/?id=1")
    assert response.status_code == 200

def test_get_all_item():
    response = client.get("/api/v1/item/getall/")
    assert response.status_code == 200

def test_add_item():
    response = client.post("/api/v1/item/add/", json={"name": "test_item"})
    assert response.status_code == 200

def test_update_item():
    response = client.put("/api/v1/item/update/", json={"name": "updated_test_item", "id": 1})
    assert response.status_code == 200

def test_delete_item():
    response = client.delete("/api/v1/item/delete/?id=1")
    assert response.status_code == 200

def test_user_all_items():
    response = client.get("/api/v1/user-item/all/?username=test_user")
    assert response.status_code == 200


def test_user_add_item():
    response = client.post("/api/v1/user-item/add/", json={"item_name": "test_item"})
    assert response.status_code == 200

def test_user_delete_item():
    response = client.get("/api/v1/user-item/delete/?item_name=test_item&username=test_user")
    assert response.status_code == 200
