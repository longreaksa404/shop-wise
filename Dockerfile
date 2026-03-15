# ── Base image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Environment variables ─────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ── System dependencies (needed for psycopg2) ─────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ───────────────────────────────────────────────
# Copy requirements first so Docker cache skips this layer if deps haven't changed
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ── Copy project source ───────────────────────────────────────────────────────
COPY . .

# ── Create required directories & set permissions ─────────────────────────────
RUN mkdir -p /app/media /app/staticfiles \
    && chown -R django:django /app

# ── Copy entrypoint and make executable ──────────────────────────────────────
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ── Expose Django dev port ────────────────────────────────────────────────────
EXPOSE 8000

# ENTRYPOINT runs migrations + collectstatic before CMD
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]