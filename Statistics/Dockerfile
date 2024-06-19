FROM python:3.11

WORKDIR /web

COPY ./Statistics/ /web/Statistics
COPY ./common /web/common

RUN pip install poetry
RUN cd /web/Statistics && poetry install --no-root --verbose
