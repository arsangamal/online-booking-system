import pytest


def test_get_authors_unauthorized(test_client):
    response = test_client.get("/authors")
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Missing Authorization Header"


# Example for authorized call (token fixture)
def test_get_authors_authorized(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    response = test_client.get("/authors", headers=headers)  # Debugging output
    print("Response JSON:", response.get_json())  # Debugging output
    # 200 or 404 depending on DB state, but should not be 401
    assert response.status_code in [200, 404]
    data = response.get_json()
    assert "message" in data
