import pytest
from sqlalchemy import select
from app.models.user import User


@pytest.mark.anyio
async def test_availability_with_schedule(client, test_db):
    # Provider crea servicio + horario, luego cliente consulta disponibilidad
    await client.post("/api/v1/auth/register", json={
        "email": "avail@test.com",
        "password": "secret123",
        "full_name": "Avail Provider",
    })
    result = await test_db.execute(select(User).where(User.email == "avail@test.com"))
    provider = result.scalars().first()
    provider.role = "provider"
    await test_db.commit()

    login_resp = await client.post("/api/v1/auth/login", data={
        "username": "avail@test.com", "password": "secret123",
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post("/api/v1/services/", json={
        "name": "Servicio Disponible",
        "duration_minutes": 60,
    }, headers=headers)
    assert create_resp.status_code == 201
    service_id = create_resp.json()["id"]

    # Horario para el lunes (día 0)
    await client.post(f"/api/v1/services/{service_id}/schedules", json={
        "day_of_week": 0,
        "start_time": "09:00:00",
        "end_time": "11:00:00",
    }, headers=headers)

    # Cambiar a cliente y consultar disponibilidad (2026-08-03 es lunes)
    provider.role = "client"
    await test_db.commit()
    fresh_login = await client.post("/api/v1/auth/login", data={
        "username": "avail@test.com", "password": "secret123",
    })
    fresh_token = fresh_login.json()["access_token"]
    client_headers = {"Authorization": f"Bearer {fresh_token}"}

    avail_resp = await client.get(
        f"/api/v1/services/{service_id}/availability?date=2026-08-03",
        headers=client_headers,
    )
    assert avail_resp.status_code == 200
    slots = avail_resp.json()
    assert len(slots) == 2  # 09:00-10:00 y 10:00-11:00


@pytest.mark.anyio
async def test_availability_no_schedule(client, test_db):
    # Servicio sin horario devuelve lista vacía
    await client.post("/api/v1/auth/register", json={
        "email": "nosched@test.com",
        "password": "secret123",
        "full_name": "No Sched",
    })
    result = await test_db.execute(select(User).where(User.email == "nosched@test.com"))
    user = result.scalars().first()
    user.role = "provider"
    await test_db.commit()

    login_resp = await client.post("/api/v1/auth/login", data={
        "username": "nosched@test.com", "password": "secret123",
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post("/api/v1/services/", json={
        "name": "Servicio Sin Horario",
        "duration_minutes": 30,
    }, headers=headers)
    assert create_resp.status_code == 201
    service_id = create_resp.json()["id"]

    user.role = "client"
    await test_db.commit()
    fresh_login = await client.post("/api/v1/auth/login", data={
        "username": "nosched@test.com", "password": "secret123",
    })
    fresh_token = fresh_login.json()["access_token"]
    client_headers = {"Authorization": f"Bearer {fresh_token}"}

    avail_resp = await client.get(
        f"/api/v1/services/{service_id}/availability?date=2026-08-03",
        headers=client_headers,
    )
    assert avail_resp.status_code == 200
    slots = avail_resp.json()
    assert len(slots) == 0