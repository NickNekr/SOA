FROM python:3.11

WORKDIR /web

COPY . .

RUN pip install poetry
RUN poetry install --no-root --verbose
