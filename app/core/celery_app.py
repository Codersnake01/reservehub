from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "reservehub",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL, # Para guardar resultados (opcional)
    include=["app.tasks.email_tasks"] # Importante: carga las tareas al iniciar
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)