# online-booking-system

## Introduction
This is an Online Booking System API built with Flask. It provides endpoints for user authentication, book management, author and category management, and supports JWT-based authentication. The project is structured for easy development, testing, and deployment using Docker.

## How to Run the App in Development Mode
1. Make sure you have Docker and Docker Compose installed.
2. Clone the repository and navigate to the project directory.
3. Run the following command to start the development environment:

```bash
docker compose --profile development up --build
```

The API will be available at `http://localhost:3000`, the documentation at `http://localhost:3000/docs` and the pgAdmin4 at `http://localhost:8888`.

### To access the PgAdmin4
- use `arsan@example.com` and `123456` as the UI credentials
- after login, create a new server with name of your choice and `db` as host, `postgres` as user and `132456` as the password.

## How to turn down the containers
```bash
docker compose --profile development up --build
```

## How to Test the Application (Docker Compose)
To run the tests in the testing environment, use:

```bash
docker compose --profile testing run --rm api_test pytest
```
and when finished, run 
```bash
docker compose --profile testing down
```
to turn down the postgres container off

## Technologies Used
- Python 3.9
- Flask (REST API framework)
- Flask-RESTX (API documentation)
- Flask-JWT-Extended (JWT authentication)
- Flask-Migrate & Alembic (database migrations)
- Flask-SQLAlchemy (ORM)
- Marshmallow (serialization/validation)
- PostgreSQL (database)
- PgAdmin4 (database client)
- Docker & Docker Compose (containerization)
- Pytest (testing)

## Notes
### Don't forget the Bearer word
to authenticate on swagger, after hitting the `login` endpoint, copy the `access_token` and in the write `Bearer {access_token}` in the authentication box of swagger.

### Database seed
the app will automatically seed 1 author and 1 category, just for testing purposes, otherwise a seeder should be used, for example [Flask-Seeder](https://pypi.org/project/Flask-Seeder/)