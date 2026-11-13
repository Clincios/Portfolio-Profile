FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend /app/backend
COPY index.html /app/index.html
COPY css /app/css
COPY js /app/js
COPY assets /app/assets

ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend

EXPOSE 8000

CMD ["sh", "-c", "python -m scripts.seed && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
