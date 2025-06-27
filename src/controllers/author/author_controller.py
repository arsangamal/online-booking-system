from config import Config
from src.models.author import Author, AuthorSchema
from flask_restx import Namespace, Resource, fields
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

author_model = api.model(
    "Author",
    {
        "id": fields.Integer(required=True, example=1),
        "name": fields.String(required=True, example="John Doe"),
    },
)

@api.route("", methods=["GET"])
class AuthorController(Resource):

    @jwt_required()
    @api.response(200, "Authors retrieved successfully", author_model)
    @api.response(401, "Unauthorized")
    @api.response(404, "Authors not found")
    @api.doc(
        security=["Bearer Auth"],
        params=request_params,
    )
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 10, type=int), Config.MAX_PER_PAGE)
        authors = Author.query.paginate(page=page, per_page=per_page)
        return {
            "data": AuthorSchema(many=True).dump(authors.items),
            "message": "Authors retrieved successfully.",
        }, 200
