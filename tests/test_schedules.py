import pytest
from sqlalchemy import select
from app.models.user import User


@pytest.mark.anyio
async def test_update_schedule(client, test_db):
    # Provider crea servicio, horario y actualiza este último
    await client.post("/api/v1/auth/register", json={
        "email": "sched1@test.com",
        "password": "secret123",
        "full_name": "Sched 1",
    })
    result = await test_db.execute(select(User).where(User.email == "sched1@test.com"))
    provider = result.scalars().first()
    provider.role = "provider"
    await test_db.commit()

    login_resp = await client.post("/api/v1/auth/login", data={
        "username": "sched1@test.com", "password": "secret123",
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear servicio
    create_resp = await client.post("/api/v1/services/", json={
        "name": "Servicio con horario",
        "duration_minutes": 30,
    }, headers=headers)
    assert create_resp.status_code == 201
    service_id = create_resp.json()["id"]

    # Crear horario
    sched_resp = await client.post(f"/api/v1/services/{service_id}/schedules", json={
        "day_of_week": 1,
        "start_time": "08:00:00",
        "end_time": "12:00:00",
    }, headers=headers)
    assert sched_resp.status_code == 201
    schedule_id = sched_resp.json()["id"]

    # Actualizar horario
    update_resp = await client.put(f"/api/v1/schedules/{schedule_id}", json={
        "day_of_week": 2,
        "start_time": "09:00:00",
        "end_time": "13:00:00",
    }, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["day_of_week"] == 2


@pytest.mark.anyio
async def test_delete_schedule(client, test_db):
    # Provider crea servicio, horario y lo elimina
    await client.post("/api/v1/auth/register", json={
        "email": "sched2@test.com",
        "password": "secret123",
        "full_name": "Sched 2",
    })
    result = await test_db.execute(select(User).where(User.email == "sched2@test.com"))
    provider = result.scalars().first()
    provider.role = "provider"
    await test_db.commit()

    login_resp = await client.post("/api/v1/auth/login", data={
        "username": "sched2@test.com", "password": "secret123",
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post("/api/v1/services/", json={
        "name": "Servicio horario borrable",
        "duration_minutes": 30,
    }, headers=headers)
    assert create_resp.status_code == 201
    service_id = create_resp.json()["id"]

    sched_resp = await client.post(f"/api/v1/services/{service_id}/schedules", json={
        "day_of_week": 3,
        "start_time": "10:00:00",
        "end_time": "14:00:00",
    }, headers=headers)
    assert sched_resp.status_code == 201
    schedule_id = sched_resp.json()["id"]

    del_resp = await client.delete(f"/api/v1/schedules/{schedule_id}", headers=headers)
    assert del_resp.status_code == 204

    get_resp = await client.get(f"/api/v1/services/{service_id}/schedules", headers=headers)
    schedules = get_resp.json()
    assert not any(s["id"] == schedule_id for s in schedules)