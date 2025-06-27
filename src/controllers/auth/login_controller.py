from flask import request
from flask_restx import Namespace, Resource, fields
from src.models.user import LoginSchema, UserSchema, User
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

api = Namespace("users", description="users operations")

user_model = api.model(
    "User",
    {
        "id": fields.Integer(required=True, example=1),
        "name": fields.String(required=True, example="John Doe"),
        "email": fields.String(required=True, example="someone@somewhere.com"),
    },
)

login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True, example="someone@somewhere.com"),
        "password": fields.String(required=True, example="securepassword123"),
    },
)

login_response = api.model(
    "LoginResponse",
    {
        "user": fields.Nested(user_model),
        "access_token": fields.String(required=True, example="abcdef123456"),
    },
)


@api.route("/login")
class Login(Resource):

    @api.expect(login_model)
    @api.response(200, "Logged in successfully", login_response)
    @api.response(401, "Invalid credentials")
    @api.doc(security=[])
    def post(self):
        try:
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            return {
                "errors": {"validation": err.messages},
                "message": "Login failed.",
            }, 400

        user = User.query.filter_by(email=data["email"]).first()

        if not user or not user.check_password(data["password"]):
            return {
                "errors": {"validation": "Invalid email or password."},
                "message": "Login failed.",
            }, 401

        token = create_access_token(identity=str(user.id))

        # Serialize the user object using UserSchema
        user_data = UserSchema().dump(user)
        return {
            "data": {"user": user_data, "access_token": token},
            "message": "Logged in successfully",
        }
