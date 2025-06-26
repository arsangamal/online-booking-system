from flask import request
from flask_restx import Namespace, Resource, fields
from src.models.user import User, UserSchema
from marshmallow import ValidationError
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
    @api.response(201, "User created successfully", user_response)
    @api.response(400, "Validation error")
    @api.doc(security=[])
    def post(self):

        try:
            data = UserSchema().load(request.get_json())
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if User.query.filter_by(email=data["email"]).first():
            return {
                "errors": {"validation": "User with this email already exists."}
            }, 400

        user = User(name=data["name"], email=data["email"])
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        user_data = UserSchema().dump(user)
        return user_data, 201
