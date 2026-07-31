from app.core.celery_app import celery_app
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="send_confirmation_email")
def send_confirmation_email(reservation_id: int, user_email: str):
    """
    Tarea para enviar un correo de confirmación de reserva.
    Por ahora, solo registra en los logs.
    """
    logger.info(f"[CELERY] Enviando confirmación de reserva {reservation_id} a {user_email}")
    # Aquí irá la integración con Mailpit/Resend
    return f"Email enviado (simulado) para reserva {reservation_id}"

@celery_app.task(name="send_reminder_email")
def send_reminder_email(reservation_id: int, user_email: str):
    """Tarea para enviar un recordatorio de reserva."""
    logger.info(f"[CELERY] Enviando recordatorio de reserva {reservation_id} a {user_email}")
    return f"Recordatorio enviado (simulado) para reserva {reservation_id}"