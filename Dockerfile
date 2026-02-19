# Build stage for frontend assets
FROM node:20-slim AS frontend-builder
WORKDIR /app
COPY package*.json ./
COPY static ./static
RUN npm install
RUN npm run build

# Build stage for Python dependencies
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen --no-cache

# Final execution stage
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment
COPY --from=builder /app/.venv /app/.venv

# Copy the frontend assets
COPY --from=frontend-builder /app/static/css/output.css ./static/css/output.css

# Copy the rest of the application code [cite: 3]
COPY . .

# Ensure the .env file is handled [cite: 4]
RUN if [ -f .env.example ]; then cp .env.example .env; fi

# Collect static files
RUN python manage.py collectstatic --noinput

# --- CONFIGURAÇÃO DO ENTRYPOINT ---
# Copia o script, dá permissão de execução e define como ponto de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Expose the port the app runs on
EXPOSE 8005

# O CMD agora é passado como argumento para o entrypoint.sh [cite: 1]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kore-product-manager.wsgi:application"]