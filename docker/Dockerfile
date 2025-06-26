FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py"]