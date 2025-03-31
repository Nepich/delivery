FROM python:3.12.9

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry install