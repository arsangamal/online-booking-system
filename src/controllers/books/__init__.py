from flask_restx import Namespace

api = Namespace("books", description="Books operations")

from .book_action import BookResource
from .book_details_action import BookDetailsAction
