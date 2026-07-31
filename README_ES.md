# ReserveHub API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.140.13-009688)
![License](https://img.shields.io/badge/license-MIT-green)

Sistema de reservas con notificaciones, construido con **FastAPI**, **PostgreSQL**, **Redis** y **Celery**.

> **Estado:** Núcleo implementado – autenticación, servicios, horarios, disponibilidad y reservas.

## Funcionalidades (actuales y próximas)

- ✅ Registro e inicio de sesión con JWT (roles cliente/proveedor)
- ✅ CRUD de servicios (solo proveedores)
- ✅ Configuración de horarios semanales
- ✅ Cálculo de disponibilidad por fecha
- ✅ Creación de reservas con detección de conflictos
- ⬜ Notificaciones por correo electrónico (Celery)
- ⬜ Panel de administración
- ⬜ Tareas en segundo plano

## Stack tecnológico

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Base de datos:** PostgreSQL 15 (local con Docker, producción con Supabase)
- **Caché/broker:** Redis
- **ORM:** SQLAlchemy 2.0 (async), Alembic
- **Autenticación:** JWT (passlib, bcrypt)
- **Tareas en segundo plano:** Celery (próximamente)
- **DevOps:** Docker, Docker Compose

## Primeros pasos

### Requisitos previos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 1. Clonar el repositorio
```bash
git clone https://github.com/Codersnake01/reservehub.git
cd reservehub
```

### 2. Configurar las variables de entorno
```bash
cp .env.example .env
```

### 3. Ejecutar con Docker
```bash
docker-compose up --build
```
La API estará disponible en `http://localhost:8002/docs`.

## Estructura del proyecto

reservehub/
├── app/
│   ├── api/v1/endpoints/   # Manejo de rutas (auth, services, schedules, availability, reservations)
│   ├── core/               # Configuración y seguridad
│   ├── db/                 # Motor asíncrono y sesión
│   ├── models/             # Modelos SQLAlchemy (User, Service, Schedule, Reservation)
│   └── schemas/            # Esquemas Pydantic
├── alembic/                # Migraciones de base de datos
├── docker-compose.yml
├── Dockerfile
└── README_ES.md

## LICENCIA

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.