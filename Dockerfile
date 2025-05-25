# --- Build Stage ---
FROM python:3.10-slim-bullseye AS builder

WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install wheelhouse of dependencies
RUN pip install --no-cache-dir wheel && \
    pip wheel --no-cache-dir -r requirements.txt

# --- Final Image ---
FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=friday.settings \
    STATIC_ROOT=/app/staticfiles \
    MEDIA_ROOT=/app/media

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        libcairo2-dev \
        && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' myuser
USER myuser
WORKDIR /app

# Install dependencies from wheelhouse
COPY --from=builder /root/.cache/pip/wheels /wheels
RUN pip install --no-index --find-links=/wheels -r /wheels/requirements.txt

# Copy source code
COPY --chown=myuser:myuser . .

# Entrypoint script
COPY --chown=myuser:myuser entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
