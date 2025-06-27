def test_get_book_details_unauthorized(test_client):
    response = test_client.get("/books/1")
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Missing Authorization Header"


def test_get_book_details_authorized(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    # create a book first
    create_response = test_client.post(
        "/books",
        headers=headers,
        json={
            "title": "Test Book",
            "price": 19.99,
            "release_date": "2023-10-01",
        },
    )
    assert create_response.status_code in [201, 400]
    response = test_client.get("/books/1", headers=headers)
    assert response.status_code in [200, 404]
    data = response.get_json()
    assert "message" in data
    assert data["data"]["id"] == 1
