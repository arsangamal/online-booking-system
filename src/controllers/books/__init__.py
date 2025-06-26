from flask_restx import Namespace

api = Namespace("books", description="Books operations")

from .get_books_action import GetBooks
