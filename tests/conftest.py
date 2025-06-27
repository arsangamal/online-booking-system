import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.user import User
import pytest
from app import create_app, db
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="module")
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def test_client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def access_token(app):
    with app.app_context():
        user = User(
            id=1,
            name="testuser",
            email="testuser@example.com",
        )
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=str(user.id))
        return token
