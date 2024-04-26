FROM python:3.11

WORKDIR /web

COPY ./TasksService/ /web/
COPY ./common /web/common

RUN pip install poetry
RUN poetry install --no-root --verbose
