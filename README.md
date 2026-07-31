# ReserveHub API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.140.13-009688)
![License](https://img.shields.io/badge/license-MIT-green)

Sistema de reservas con notificaciones, construido con FastAPI, PostgreSQL, Redis y Celery.

> **Status:** Core implemented – auth, services, schedules, availability, reservations.

## Features (Current & Upcoming)

- ✅ User registration and login with JWT (client/provider roles)
- ✅ CRUD for services (providers only)
- ✅ Weekly schedule configuration
- ✅ Availability calculation
- ✅ Reservation creation with conflict detection
- ⬜ Email notifications via Celery
- ⬜ Admin dashboard
- ⬜ Background tasks

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Database:** PostgreSQL 15 (local via Docker, production via Supabase)
- **Cache/Broker:** Redis
- **ORM:** SQLAlchemy 2.0 (async), Alembic
- **Authentication:** JWT (passlib, bcrypt)
- **Background Tasks:** Celery (coming)
- **DevOps:** Docker, Docker Compose

## Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 1. Clone the repository
```bash
git clone https://github.com/Codersnake01/reservehub.git
cd reservehub
```

### 2. Configure environment variables
```bash
cp .env.example .env
```

### 3. Run with Docker
```bash
docker-compose up --build
```
API available at `http://localhost:8002/docs`.

## LICENSE

MIT

