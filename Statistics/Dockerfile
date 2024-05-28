FROM python:3.11

WORKDIR /web

COPY ./Statistics/ /web/
COPY ./common /web/common

RUN pip install poetry
RUN poetry install --no-root --verbose
