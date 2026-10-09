# Get Python image and install uv, both version pinned
FROM python:3.14-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /bin/uv

# Skip installing development dependencies
ENV UV_NO_DEV=1
WORKDIR /app

# Install libraries and dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project

# Install project into environment
COPY app ./app
RUN uv sync --locked

# Serve FastAPI backend through uvicorn server
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
