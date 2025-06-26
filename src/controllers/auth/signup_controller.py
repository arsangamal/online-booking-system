from flask import request
from flask_restx import Namespace, Resource, fields
from src.models.user import User
from app import db

api = Namespace("users", description="users operations")


signup_model = api.model(
    "Signup",
    {
        "name": fields.String(required=True, example="arsan"),
        "email": fields.String(required=True, example="arsan@example.com"),
        "password": fields.String(required=True, example="securepassword123"),
    },
)

user_response = api.model(
    "UserResponse",
    {"id": fields.Integer, "name": fields.String, "email": fields.String},
)


@api.route("/signUp", methods=["POST"])
class SignUp(Resource):

    @api.expect(signup_model)
    @api.marshal_with(user_response, code=201)
    def post(self):
        data = request.json

        if User.query.filter(
            (User.name == data["name"]) | (User.email == data["email"])
        ).first():
            api.abort(400, {"error": "Name or email already exists"})

        user = User(name=data["name"], email=data["email"])
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return user, 201
