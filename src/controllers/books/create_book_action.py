from src.models.book import Book, BookSchema
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required
from flask import request
from marshmallow import ValidationError
from . import api
from app import db
from src.models.author import Author
from src.models.category import Category

book_create_model = api.model(
    "BookCreate",
    {
        "title": fields.String(required=True, example="The Great Gatsby"),
        "price": fields.Float(required=False, example=19.99),
        "release_date": fields.String(required=False, example="2024-01-01"),
        "author_id": fields.Integer(required=False, example=1),
        "category_id": fields.Integer(required=False, example=1),
    },
)


@api.route("", methods=["POST"])
class CreateBook(Resource):
    @jwt_required()
    @api.expect(book_create_model)
    @api.response(201, "Book created successfully", book_create_model)
    @api.response(400, "Validation Error")
    @api.response(401, "Unauthorized")
    @api.doc(security=["Bearer Auth"])
    def post(self):
        data = request.get_json()
        schema = BookSchema()
        try:
            book_data = schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        author_id = book_data.get("author_id")
        category_id = book_data.get("category_id")

        if author_id is not None:
            author = db.session.query(Author).filter_by(id=author_id).first()
            if not author:
                return {
                    "error": {"message": f"Author with id {author_id} does not exist."}
                }, 400

        if category_id is not None:
            category = db.session.query(Category).filter_by(id=category_id).first()
            if not category:
                return {
                    "error": {
                        "message": f"Category with id {category_id} does not exist."
                    }
                }, 400

        book = Book(**book_data)
        db.session.add(book)
        db.session.commit()
        return schema.dump(book), 201
