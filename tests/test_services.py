import pytest
from sqlalchemy import select

from app.models.user import User


@pytest.mark.anyio
async def test_update_service(client, test_db):
    # Crear un provider y un servicio
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "provider1@test.com",
            "password": "secret123",
            "full_name": "Provider 1",
        },
    )
    result = await test_db.execute(
        select(User).where(User.email == "provider1@test.com")
    )
    provider = result.scalars().first()
    provider.role = "provider"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "provider1@test.com",
            "password": "secret123",
        },
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear servicio
    create_resp = await client.post(
        "/api/v1/services/",
        json={
            "name": "Servicio Original",
            "duration_minutes": 30,
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    service_id = create_resp.json()["id"]

    # Actualizar servicio
    update_resp = await client.put(
        f"/api/v1/services/{service_id}",
        json={
            "name": "Servicio Actualizado",
            "duration_minutes": 45,
        },
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Servicio Actualizado"


@pytest.mark.anyio
async def test_delete_service(client, test_db):
    # Crear provider, servicio y luego eliminarlo
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "provider2@test.com",
            "password": "secret123",
            "full_name": "Provider 2",
        },
    )
    result = await test_db.execute(
        select(User).where(User.email == "provider2@test.com")
    )
    provider = result.scalars().first()
    provider.role = "provider"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "provider2@test.com",
            "password": "secret123",
        },
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post(
        "/api/v1/services/",
        json={
            "name": "Servicio a borrar",
            "duration_minutes": 20,
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    service_id = create_resp.json()["id"]

    # Eliminar
    del_resp = await client.delete(f"/api/v1/services/{service_id}", headers=headers)
    assert del_resp.status_code == 204

    # Verificar que no existe en la lista general
    list_resp = await client.get("/api/v1/services/", headers=headers)
    assert list_resp.status_code == 200
    services = list_resp.json()
    assert not any(s["id"] == service_id for s in services)


@pytest.mark.anyio
async def test_unauthorized_service_update(client, test_db):
    # Crear un provider, un servicio, y luego un cliente intenta modificarlo
    # 1. Crear provider y servicio
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "owner@test.com",
            "password": "secret123",
            "full_name": "Owner",
        },
    )
    result = await test_db.execute(select(User).where(User.email == "owner@test.com"))
    provider = result.scalars().first()
    provider.role = "provider"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "owner@test.com",
            "password": "secret123",
        },
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post(
        "/api/v1/services/",
        json={
            "name": "Servicio Privado",
            "duration_minutes": 30,
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    service_id = create_resp.json()["id"]

    # 2. Registrar un cliente
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "intruso@test.com",
            "password": "secret123",
            "full_name": "Intruso",
        },
    )
    client_login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "intruso@test.com",
            "password": "secret123",
        },
    )
    client_token = client_login.json()["access_token"]
    client_headers = {"Authorization": f"Bearer {client_token}"}

    # 3. El cliente intenta actualizar el servicio → debe recibir 403
    resp = await client.put(
        f"/api/v1/services/{service_id}",
        json={
            "name": "Hackeado",
        },
        headers=client_headers,
    )
    assert resp.status_code == 403
