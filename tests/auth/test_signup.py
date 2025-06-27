def test_signup_success(test_client):
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword123",
    }
    response = test_client.post("/users/signUp", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["data"]["email"] == payload["email"]
    assert "id" in data["data"]
    assert data["message"] == "User created successfully."


def test_signup_duplicate_email(test_client):
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword123",
    }
    # First signup
    test_client.post("/users/signUp", json=payload)
    # Duplicate signup
    response = test_client.post("/users/signUp", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "User with this email already exists." in str(data["errors"]["validation"])
