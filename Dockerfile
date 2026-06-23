FROM node:22-bookworm-slim AS frontend

WORKDIR /app/cms
COPY cms/package*.json ./
RUN npm ci
COPY cms/ ./
RUN npm run build

FROM python:3.13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .
COPY --from=frontend /app/cms/dist ./cms/dist

RUN uv run python run.py reset-demo \
    && uv run python run.py validate

ENV CS_CONTEXT_REPOSITORY_PATH=/var/data/context_repo
ENV CS_USERS_PATH=/var/data/users.sqlite
ENV CS_AUDIT_PATH=/var/data/audit.sqlite
ENV CS_COLLECTIONS_ROOT_PATH=/var/data/collections
ENV CS_COLLECTIONS_DB_PATH=/var/data/collections.sqlite
ENV CS_PUBLIC_APP_URL=https://context-studio-demo.onrender.com

EXPOSE 10000

CMD ["sh", "-c", "uv run python run.py init-demo && uv run python run.py serve --host 0.0.0.0 --port ${PORT:-10000}"]

