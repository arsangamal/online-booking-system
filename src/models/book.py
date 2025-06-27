from app import db, ma


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=True, default=0.0)
    release_date = db.Column(db.Date, nullable=True, default=None)
    # Optional
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    # Relationships
    author = db.relationship("Author", backref="books")
    category = db.relationship("Category", backref="books")


class BookSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    title = ma.String(required=True)
    price = ma.Float(required=True)
    release_date = ma.Date(required=True)
    author_id = ma.Integer(required=False)
    category_id = ma.Integer(required=False)
    author = ma.Nested("AuthorSchema", only=["id", "name"], required=False)
    category = ma.Nested("CategorySchema", only=["id", "name"], required=False)
