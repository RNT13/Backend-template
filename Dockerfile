FROM python:3.13.1-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=2.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential libpq-dev

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-ansi --only main


FROM python:3.13.1-slim AS final

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN addgroup --system app && adduser --system --group app

WORKDIR /app

COPY --from=builder /app /app

COPY . .

USER app

EXPOSE 8000

CMD ["sh", "-c", ". .venv/bin/activate && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT"]
