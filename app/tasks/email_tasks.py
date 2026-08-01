import smtplib
import logging
from email.mime.text import MIMEText
from app.core.celery_app import celery_app
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, body: str):
    """
    Envía un email utilizando el servidor SMTP configurado (Mailpit en desarrollo)
    o Resend si la API key está configurada (producción).
    """
    if settings.RESEND_API_KEY:
        # Modo producción: usar el SDK de Resend
        import resend
        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send({
            "from": "noreply@reservehub.com",
            "to": to_email,
            "subject": subject,
            "html": body
        })
        logger.info(f"Email enviado a {to_email} vía Resend")
    else:
        # Modo desarrollo: enviar mediante SMTP (Mailpit)
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = "noreply@reservehub.com"
        msg["To"] = to_email
        try:
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.sendmail(msg["From"], [to_email], msg.as_string())
            logger.info(f"Email enviado a {to_email} vía SMTP ({settings.EMAIL_HOST}:{settings.EMAIL_PORT})")
        except Exception as e:
            logger.error(f"Error enviando email a {to_email}: {e}")

@celery_app.task(name="send_confirmation_email")
def send_confirmation_email(reservation_id: int, user_email: str):
    """Tarea para enviar un correo de confirmación de reserva."""
    subject = f"Reserva #{reservation_id} Confirmada"
    body = f"<h1>Reserva Confirmada</h1><p>Tu reserva con ID {reservation_id} ha sido confirmada.</p>"
    send_email(user_email, subject, body)

@celery_app.task(name="send_reminder_email")
def send_reminder_email(reservation_id: int, user_email: str):
    """Tarea para enviar un recordatorio de reserva (se llamará manualmente o vía Celery beat)."""
    subject = f"Recordatorio de tu reserva #{reservation_id}"
    body = f"<p>Te recordamos que tienes una reserva activa con ID {reservation_id}.</p>"
    send_email(user_email, subject, body)