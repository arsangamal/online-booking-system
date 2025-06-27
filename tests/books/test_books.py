def test_get_books_unauthorized(test_client):
    response = test_client.get("/books")
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Missing Authorization Header"


def test_get_books_authorized(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/books", headers=headers)
    assert response.status_code in [200, 404]
    data = response.get_json()
    assert "message" in data


def test_create_book_unauthorized(test_client):
    response = test_client.post(
        "/books",
        json={
            "title": "New Book",
            "author": "Author Name",
            "description": "Book description",
            "price": 19.99,
        },
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Missing Authorization Header"


def test_create_book_authorized(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post(
        "/books",
        headers=headers,
        json={
            "title": "New Book",
            "price": 19.99,
            "release_date": "2023-10-01",
        },
    )
    assert response.status_code in [201, 400]
    data = response.get_json()
    assert "data" in data
    assert data["data"]["title"] == "New Book"
    assert data["data"]["price"] == 19.99
    assert data["data"]["release_date"] == "2023-10-01"


def test_update_book_unauthorized(test_client):
    response = test_client.patch(
        "/books",
        json={
            "title": "Updated Book",
            "author": "Updated Author",
            "description": "Updated description",
            "price": 29.99,
        },
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Missing Authorization Header"


def test_update_book_authorized(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    # create book first
    create_response = test_client.post(
        "/books",
        headers=headers,
        json={
            "title": "Book to Update",
            "price": 19.99,
            "release_date": "2023-10-01",
        },
    )
    assert create_response.status_code in [201, 400]
    response = test_client.patch(
        "/books",
        headers=headers,
        json={
            "id": create_response.get_json()["data"]["id"],
            "title": "Updated Book",
            "price": 29.99,
            "release_date": "2023-10-01",
        },
    )
    assert response.status_code in [200, 404]
    data = response.get_json()
    assert "data" in data
    assert data["data"]["title"] == "Updated Book"
    assert data["data"]["price"] == 29.99
    assert data["data"]["release_date"] == "2023-10-01"
