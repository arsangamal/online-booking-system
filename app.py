from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()


# Create Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    api = Api(
        app,
        version="1.0",
        title="Online Booking System",
        description="Online Booking System API",
        doc="/docs",
        prefix="/api",
    )

    from src.controllers.auth.login_controller import api as login_controller
    from src.controllers.auth.signup_controller import api as signup_controller
    from src.models import user

    api.add_namespace(login_controller, path="/users")
    api.add_namespace(signup_controller, path="/users")

    return app
