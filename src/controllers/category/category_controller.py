from config import Config
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask import request

from src.models.category import Category, CategorySchema

api = Namespace("category", description="Category operations")

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

category_model = api.model(
    "Category",
    {
        "id": fields.Integer(required=True, example=1),
        "name": fields.String(required=True, example="Fiction"),
    },
)


@api.route("", methods=["GET"])
class CategoryController(Resource):

    @jwt_required()
    @api.response(200, "Categories retrieved successfully", category_model)
    @api.response(401, "Unauthorized")
    @api.response(404, "Categories not found")
    @api.doc(
        security=["Bearer Auth"],
        params=request_params,
    )
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 10, type=int), Config.MAX_PER_PAGE)
        categories = Category.query.paginate(page=page, per_page=per_page)
        return CategorySchema(many=True).dump(categories.items), 200
