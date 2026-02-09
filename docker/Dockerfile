# Frontend build stage
FROM docker.arvancloud.ir/node:25-alpine AS frontend-builder

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Python base
FROM docker.arvancloud.ir/python:3.14-slim AS backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG DJANGO_ENV
ENV DJANGO_ENV=${DJANGO_ENV}

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# python deps
COPY pyproject.toml uv.lock .python-version ./
RUN pip install --upgrade pip && pip install --no-cache-dir .

# App code
COPY backend/ /app/backend/
COPY static/ /app/static/

# copy built frontend assets
RUN mkdir -p /app/frontend
COPY --from=frontend-builder /frontend/assets /app/frontend/assets
COPY frontend/templates /app/frontend/templates

COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Django setup
WORKDIR /app/backend

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
