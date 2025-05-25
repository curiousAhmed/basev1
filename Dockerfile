# --- Build Stage ---
FROM python:3.10-slim-bullseye AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user pipx && \
    pipx ensurepath && \
    pip install pip-tools && \
    pip-compile --output-file=requirements.txt requirements.in || cp requirements.txt .

RUN pip wheel --no-cache-dir -r requirements.txt

# --- Final Image ---
FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=friday.settings \
    STATIC_ROOT=/app/staticfiles \
    MEDIA_ROOT=/app/media

WORKDIR /app

# Install required system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' root
USER root
WORKDIR /app

# Copy wheels and app code
COPY --from=builder /root/.cache/pip/wheels /wheels
COPY --chown=root:root . .

# Install dependencies from wheelhouse
RUN pip install --no-index --find-links=/wheels -r requirements.txt

EXPOSE 8000

# Run migrations and collect static files
COPY --chown=root:root entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]