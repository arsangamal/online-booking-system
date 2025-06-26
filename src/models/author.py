from app import db, ma


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class AuthorSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
