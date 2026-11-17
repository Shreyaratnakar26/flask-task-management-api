# ---------- Stage 1: build ----------
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app ./app
COPY run.py .
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} PORT=5000
EXPOSE 5000
RUN useradd -m appuser
USER appuser
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} run:app"]
