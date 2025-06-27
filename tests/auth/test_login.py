def test_login_success(test_client):
    # First, sign up a user
    signup_payload = {
        "name": "Login User",
        "email": "loginuser@example.com",
        "password": "testpassword123",
    }
    test_client.post("/users/signUp", json=signup_payload)

    login_payload = {"email": "loginuser@example.com", "password": "testpassword123"}
    response = test_client.post("/users/login", json=login_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data["data"]
    assert data["data"]["user"]["email"] == login_payload["email"]
    assert data["message"] == "Logged in successfully"


def test_login_invalid_credentials(test_client):
    login_payload = {"email": "notfound@example.com", "password": "wrongpassword"}
    response = test_client.post("/users/login", json=login_payload)
    assert response.status_code == 401
    data = response.get_json()
    assert "Invalid email or password." in str(data["errors"]["validation"])
