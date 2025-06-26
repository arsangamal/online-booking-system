from flask_restx import Namespace, Resource

api = Namespace("users", description="users operations")


@api.route("/login")
class Login(Resource):
    def get(self):
        return {"message": "Login successful"}
