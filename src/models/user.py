from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    email = ma.Email(required=True)
    password = ma.String(required=True, load_only=True)


class LoginSchema(ma.Schema):
    email = ma.Email(required=True)
    password = ma.String(required=True, load_only=True)
