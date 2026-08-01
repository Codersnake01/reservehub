import pytest
from unittest.mock import patch
from app.tasks.email_tasks import send_confirmation_email

@pytest.mark.anyio
async def test_send_confirmation_email_calls_send_email():
    with patch("app.tasks.email_tasks.send_email") as mock_send:
        send_confirmation_email(1, "test@test.com")
        mock_send.assert_called_once_with(
            "test@test.com",
            "Reserva #1 Confirmada",
            "<h1>Reserva Confirmada</h1><p>Tu reserva con ID 1 ha sido confirmada.</p>"
        )