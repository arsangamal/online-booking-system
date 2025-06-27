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

book_edit_model = api.model(
    "BookEdit",
    {
        "id": fields.Integer(required=True, example=1),
        "title": fields.String(required=False, example="The Great Gatsby"),
        "price": fields.Float(required=False, example=19.99),
        "release_date": fields.String(required=False, example="2024-01-01"),
        "author_id": fields.Integer(required=False, example=1),
        "category_id": fields.Integer(required=False, example=1),
    },
)


@api.route("", methods=["POST", "PATCH"])
class CreateUpdateBook(Resource):
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
            return {
                "errors": {"validation": err.messages},
                "message": "Book creation failed.",
            }, 400

        author_id = book_data.get("author_id")
        category_id = book_data.get("category_id")

        if author_id is not None:
            author = db.session.query(Author).filter_by(id=author_id).first()
            if not author:
                return {
                    "errors": {
                        "validation": "Author with id {author_id} does not exist."
                    },
                    "message": "Book creation failed.",
                }, 400

        if category_id is not None:
            category = db.session.query(Category).filter_by(id=category_id).first()
            if not category:
                return {
                    "errors": {
                        "validation": f"Category with id {category_id} does not exist."
                    },
                    "message": "Book creation failed.",
                }, 400

        book = Book(**book_data)
        db.session.add(book)
        db.session.commit()
        return {"data": schema.dump(book), "message": "Book created successfully."}, 201

    @jwt_required()
    @api.expect(book_edit_model)
    @api.response(200, "Book updated successfully", book_edit_model)
    @api.response(400, "Validation Error")
    @api.response(401, "Unauthorized")
    @api.response(404, "Book not found")
    @api.doc(security=["Bearer Auth"])
    def patch(self):
        data = request.get_json()
        if not data or "id" not in data:
            return {
                "errors": {"validation": "Book id is required."},
                "message": "Book update failed.",
            }, 400

        book_id = data["id"]
        book = Book.query.get(book_id)
        if not book:
            return {
                "errors": {"validation": f"Book with id {book_id} not found."},
                "message": "Book update failed.",
            }, 404

        # Validate author and category if present
        author_id = data.get("author_id")
        if author_id is not None:
            author = db.session.query(Author).filter_by(id=author_id).first()
            if not author:
                return {
                    "errors": {
                        "validation": f"Author with id {author_id} does not exist."
                    }
                }, 400

        category_id = data.get("category_id")
        if category_id is not None:
            category = db.session.query(Category).filter_by(id=category_id).first()
            if not category:
                return {
                    "errors": {
                        "validation": f"Category with id {category_id} does not exist."
                    }
                }, 400

        schema = BookSchema(partial=True)
        try:
            # remove id from book data
            data.pop("id", None)
            book_data = schema.load(data, partial=True)
        except ValidationError as err:
            return {
                "errors": {"validation": err.messages},
                "message": "Book update failed.",
            }, 400

        for key, value in book_data.items():
            setattr(book, key, value)

        db.session.commit()
        return {
            "data": BookSchema().dump(book),
            "message": "Book updated successfully.",
        }, 200
