FROM python:3.12-rc-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .