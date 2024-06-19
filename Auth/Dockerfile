FROM python:3.11

WORKDIR /web

COPY ./Auth/ /web/Auth
COPY ./common /web/common

RUN pip install poetry
RUN cd /web/Auth && poetry install --no-root --verbose