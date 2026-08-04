# ReserveHub API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.140.13-009688)
![Coverage](https://codecov.io/gh/Codersnake01/reservehub/branch/main/graph/badge.svg)
![CI](https://github.com/Codersnake01/reservehub/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)

Sistema de reservas profesional con notificaciones asíncronas, construido con **FastAPI**, **PostgreSQL**, **Redis**, **Celery** y **Docker**.

> **Demo en vivo (Swagger):** [https://reservehub-k3dh.onrender.com/docs](https://reservehub-k3dh.onrender.com/docs)  
> **Colección de Postman:** [Descargar](https://github.com/Codersnake01/reservehub/blob/main/ReserveHub.postman_collection.json)

## Funcionalidades

- ✅ Registro e inicio de sesión con JWT (roles cliente / proveedor)
- ✅ CRUD de servicios (solo proveedores)
- ✅ Configuración de horarios semanales por servicio
- ✅ Cálculo de disponibilidad en tiempo real (evita doble reserva)
- ✅ Creación de reservas con detección de conflictos horarios
- ✅ Control de concurrencia optimista para confirmación de reservas
- ✅ Envío de correos asíncrono con Celery + Redis
- ✅ Suite completa de tests (cobertura 88 %)
- ✅ CI/CD con GitHub Actions (lint, verificación de tipos, tests, cobertura)
- ✅ Docker Compose para desarrollo local (web, db, redis, worker, mailpit)
- ✅ Desplegado en Render (web + worker) con Neon (PostgreSQL) y Upstash (Redis)

## Stack tecnológico

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Base de datos:** PostgreSQL 15 (Neon en producción, Docker en local)
- **Caché / Broker:** Redis (Upstash en producción, Docker en local)
- **ORM:** SQLAlchemy 2.0 (async), Alembic
- **Tareas en segundo plano:** Celery
- **Correo:** Resend (producción), Mailpit (pruebas locales)
- **Testing:** Pytest, HTTPX, coverage
- **DevOps:** Docker, Docker Compose, Render, GitHub Actions

## Primeros pasos

### Requisitos previos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

### 1. Clonar el repositorio
```bash
git clone https://github.com/Codersnake01/reservehub.git
cd reservehub
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
```

### 3. Ejecutar con Docker
```bash
docker-compose up --build
```
La API estará disponible en `http://localhost:8002/docs`.
Interfaz web de Mailpit en `http://localhost:8025`.

### 4. Aplicar migraciones
```bash
docker-compose exec web alembic upgrade head
```

## Control de concurrencia

La confirmación de reservas usa **bloqueo optimista**. Cada reserva tiene un campo `version`. Al confirmar, el cliente envía la versión esperada. Si otro proceso modificó la reserva, la versión no coincidirá y la API devuelve `409 Conflict`. Esto evita confirmaciones dobles accidentales.

## Estructura del proyecto

```
reservehub/
├── app/
│   ├── api/v1/endpoints/   # Manejadores de rutas
│   ├── core/               # Configuración, seguridad, Celery
│   ├── db/                 # Motor asíncrono y sesión
│   ├── models/             # Modelos SQLAlchemy
│   ├── schemas/            # Esquemas Pydantic
│   └── tasks/              # Tareas de Celery (correos)
├── tests/                  # Suite de tests (11 tests, 88 % cobertura)
├── alembic/                # Migraciones
├── .github/workflows/      # CI/CD y keep-alive
├── docker-compose.yml
├── Dockerfile
├── start.sh                # Script de inicio para Render
└── README_ES.md
```

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.