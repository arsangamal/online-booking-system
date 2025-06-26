from src.models.author import Author, AuthorSchema
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from flask import request

api = Namespace("authors", description="Authors operations")

request_params = {
    "page": {
        "description": "Page number",
        "in": "query",
        "type": "integer",
        "default": 1,
        "required": False,
    },
    "per_page": {
        "description": "Authors per page",
        "in": "query",
        "type": "integer",
        "default": 10,
        "required": False,
    },
}


@api.route("", methods=["GET"])
class AuthorController(Resource):

    @jwt_required()
    @api.response(200, "Authors retrieved successfully")
    @api.response(401, "Unauthorized")
    @api.response(404, "Authors not found")
    @api.doc(
        security=["Bearer Auth"],
        params=request_params,
    )
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        authors = Author.query.paginate(page=page, per_page=per_page)
        return AuthorSchema(many=True).dump(authors.items), 200
