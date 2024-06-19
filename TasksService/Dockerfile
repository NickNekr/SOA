FROM python:3.11

WORKDIR /web

COPY ./TasksService/ /web/TasksService
COPY ./common /web/common

RUN pip install poetry
RUN cd /web/TasksService && poetry install --no-root --verbose
