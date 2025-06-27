#!/bin/bash


if [ "$FLASK_ENV" != "testing" ]; then
    # Run database migrations
    echo "Running database migrations..."
    python -m flask db upgrade
fi

python manage.py