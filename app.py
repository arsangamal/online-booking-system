from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

from config import Config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Enter JWT token like: **Bearer &lt;your_token&gt;**",
    }
}

# Create Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    api = Api(
        app,
        version="1.0",
        title="Online Booking System",
        description="Online Booking System API",
        doc="/docs",
        authorizations=authorizations,
        security="Bearer Auth",
    )

    from src.controllers.auth.login_controller import api as login_controller
    from src.controllers.auth.signup_controller import api as signup_controller
    from src.models import user

    api.add_namespace(login_controller, path="/users")
    api.add_namespace(signup_controller, path="/users")

    return app
