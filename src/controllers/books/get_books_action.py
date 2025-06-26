from src.models.book import Book, BookSchema
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask import request
from . import api

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

book_model = api.model(
    "Book",
    {
        "id": fields.Integer(required=True, example=1),
        "title": fields.String(required=True, example="The Great Gatsby"),
        "author_id": fields.Integer(required=False, example=1),
        "category_id": fields.Integer(required=False, example=1),
    },
)


@api.route("", methods=["GET"])
class GetBooks(Resource):

    @jwt_required()
    @api.response(200, "Books retrieved successfully", book_model)
    @api.response(401, "Unauthorized")
    @api.response(404, "Books not found")
    @api.doc(
        security=["Bearer Auth"],
        params=request_params,
    )
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        books = Book.query.paginate(page=page, per_page=per_page)
        return BookSchema(many=True).dump(books.items), 200
