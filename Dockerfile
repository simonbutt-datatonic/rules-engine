from python:buster

RUN pip install --upgrade pip && pip install pdm

COPY . /workspace
WORKDIR /workspace

ENV PYTHONPATH "$PYTHONPATH:$(pwd)"

