import os
from manage import app, db


def seed_database():
    if os.getenv("FLASK_ENV") != "testing":
        # Run database seeding
        app.logger.info("seeding database...")
        with app.app_context():
            from src.models.author import Author
            from src.models.category import Category

            # Insert an author only if not exists
            author_name = "Arsan Gamal"
            existing_author = Author.query.filter_by(name=author_name).first()
            if not existing_author:
                new_author = Author(name=author_name)
                db.session.add(new_author)

            # Insert a category only if not exists
            category_name = "General"
            existing_category = Category.query.filter_by(name=category_name).first()
            if not existing_category:
                new_category = Category(name=category_name)
                db.session.add(new_category)

            db.session.commit()
