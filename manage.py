from flask_migrate import Migrate
from app import create_app, db

app = create_app()

migrate = Migrate(app, db)


if __name__ == "__main__":
    from seed import seed_database

    seed_database()
    app.run(host="0.0.0.0", port=3000, debug=True)
