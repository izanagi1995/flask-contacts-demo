FROM python:3.9

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.11

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock /app/
RUN  poetry install --no-interaction --no-ansi
COPY . /app/

# TODO: replace the dev server by gunicorn
CMD FLASK_APP=flask_contacts_demo/app.py poetry run flask run --host=0.0.0.0
