# Build stage for frontend assets
FROM node:20-slim AS frontend-builder
WORKDIR /app
COPY package*.json ./
COPY static ./static
RUN npm install
RUN npm run build

# Build stage for Python dependencies
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Final execution stage
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the frontend assets from the frontend stage
COPY --from=frontend-builder /app/static/css/output.css ./static/css/output.css

# Copy the rest of the application code
COPY . .

# Ensure the .env file is handled
RUN if [ -f .env.example ]; then cp .env.example .env; fi

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kore_product_manager.wsgi:application"]
