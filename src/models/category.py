from app import db, ma


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class CategorySchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
