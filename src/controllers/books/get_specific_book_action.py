from src.models.book import Book, BookSchema
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required
from flask import abort
from . import api

book_model = api.model(
    "BookDetail",
    {
        "id": fields.Integer(required=True, example=1),
        "title": fields.String(required=True, example="The Great Gatsby"),
        "price": fields.Float(required=True, example=19.99),
        "release_date": fields.String(required=True, example="2024-01-01"),
        "author_id": fields.Integer(required=False, example=1),
        "category_id": fields.Integer(required=False, example=1),
    },
)


@api.route("/<int:id>", methods=["GET"])
class GetSpecificBook(Resource):
    @jwt_required()
    @api.response(200, "Book retrieved successfully", book_model)
    @api.response(401, "Unauthorized")
    @api.response(404, "Book not found")
    @api.doc(security=["Bearer Auth"])
    def get(self, id):
        book = Book.query.get(id)
        if not book:
            return {"data": None, "message": "Book not found"}, 404
        return {
            "data": BookSchema().dump(book),
            "message": "Book retrieved successfully.",
        }, 200
