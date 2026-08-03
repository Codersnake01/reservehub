#!/bin/bash
# Iniciar el worker de Celery en segundo plano
celery -A app.core.celery_app worker --loglevel=info &
# Iniciar la API de FastAPI
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}