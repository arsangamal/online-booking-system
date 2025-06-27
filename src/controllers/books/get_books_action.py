from config import Config
from src.filters.book_release_date_filter import BookReleaseDateFilter
from src.filters.book_price_filter import BookPriceFilter
from src.models.book import Book, BookSchema
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask import request
from flask_query_builder.querying import QueryBuilder, AllowedFilter

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
        query_builder = QueryBuilder(Book).allowed_filters(
            [
                "category_id",
                "author_id",
                AllowedFilter.custom("price", BookPriceFilter()),
                AllowedFilter.custom("price_gt", BookPriceFilter()),
                AllowedFilter.custom("price_lt", BookPriceFilter()),
                AllowedFilter.custom("release_date", BookReleaseDateFilter()),
                AllowedFilter.custom("release_date_gt", BookReleaseDateFilter()),
                AllowedFilter.custom("release_date_lt", BookReleaseDateFilter()),
            ]
        )

        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 10, type=int), Config.MAX_PER_PAGE)

        books = query_builder.query.paginate(max_per_page=per_page, page=page)

        return BookSchema(many=True).dump(books), 200
