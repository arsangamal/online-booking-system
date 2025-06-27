def test_get_categories_unauthorized(test_client):
    response = test_client.get("/categories")
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Missing Authorization Header"


def test_get_categories_authorized(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/categories", headers=headers)
    assert response.status_code in [200, 404]
    data = response.get_json()
    assert "message" in data
