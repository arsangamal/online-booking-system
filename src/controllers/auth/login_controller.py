from flask_restx import Namespace, Resource

api = Namespace("Authentication", description="Authentication operations")


@api.route("/login")
class Login(Resource):
    def get(self):
        return {"message": "Login successful"}
