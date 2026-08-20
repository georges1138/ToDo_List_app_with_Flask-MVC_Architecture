FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project --no-dev

COPY app ./app

WORKDIR /app/app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid appuser --create-home appuser

USER appuser

EXPOSE 3000

CMD ["gunicorn", "--workers", "2", "--timeout", "60", "--bind", "0.0.0.0:3000", "app:create_app()"]
