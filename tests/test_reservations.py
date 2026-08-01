import pytest
from sqlalchemy import select
from app.models.user import User

@pytest.mark.anyio
async def test_concurrent_confirmation(client, test_db):
    # 1. Registrar usuario y convertirlo en provider
    await client.post("/api/v1/auth/register", json={
        "email": "concur@test.com",
        "password": "secret123",
        "full_name": "Concur Client",
    })
    result = await test_db.execute(select(User).where(User.email == "concur@test.com"))
    user = result.scalars().first()
    user.role = "provider"
    await test_db.commit()

    login_resp = await client.post("/api/v1/auth/login", data={
        "username": "concur@test.com", "password": "secret123",
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear servicio y guardar su ID real
    service_resp = await client.post("/api/v1/services/", json={
        "name": "Test Service",
        "duration_minutes": 60,
    }, headers=headers)
    assert service_resp.status_code == 201
    service_id = service_resp.json()["id"]

    # 3. Configurar horario (lunes) para ese servicio
    await client.post(f"/api/v1/services/{service_id}/schedules", json={
        "day_of_week": 0,
        "start_time": "09:00:00",
        "end_time": "17:00:00",
    }, headers=headers)

    # 4. Cambiar rol a cliente y obtener un token fresco
    user.role = "client"
    await test_db.commit()

    fresh_login = await client.post("/api/v1/auth/login", data={
        "username": "concur@test.com", "password": "secret123",
    })
    fresh_token = fresh_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {fresh_token}"}

    # 5. Crear reserva
    resp = await client.post("/api/v1/reservations", json={
        "service_id": service_id,
        "start_time": "2026-08-03T10:00:00",
    }, headers=headers)
    assert resp.status_code == 201
    reservation = resp.json()
    reservation_id = reservation["id"]
    initial_version = reservation["version"]

    # 6. Primera confirmación (debe funcionar)
    resp1 = await client.patch(
        f"/api/v1/reservations/{reservation_id}/confirm",
        json={"version": initial_version},
        headers=headers,
    )
    assert resp1.status_code == 200
    assert resp1.json()["version"] == 2

    # 7. Segunda confirmación con versión antigua (debe fallar con 409)
    resp2 = await client.patch(
        f"/api/v1/reservations/{reservation_id}/confirm",
        json={"version": initial_version},
        headers=headers,
    )
    assert resp2.status_code == 409