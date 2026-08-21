# ---------- Этап сборки зависимостей ----------
FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Финальный образ ----------
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

WORKDIR /app

# Не создаём отдельного пользователя для разработки
# RUN useradd --create-home appuser
# USER appuser

COPY --chown=root:root app ./app

COPY --chown=appuser:appuser alembic ./alembic

COPY --chown=appuser:appuser alembic.ini .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]