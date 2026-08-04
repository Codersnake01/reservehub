# ReserveHub API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.140.13-009688)
![Coverage](https://codecov.io/gh/Codersnake01/reservehub/branch/main/graph/badge.svg)
![CI](https://github.com/Codersnake01/reservehub/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)

Professional reservation system with asynchronous notifications, built with **FastAPI**, **PostgreSQL**, **Redis**, **Celery**, and **Docker**.

> **Live Demo (Swagger):** [https://reservehub-k3dh.onrender.com/docs](https://reservehub-k3dh.onrender.com/docs)  
> **Postman Collection:** [Download](https://github.com/Codersnake01/reservehub/blob/main/ReserveHub.postman_collection.json)

## Features

- ✅ User registration & login with JWT (client / provider roles)
- ✅ CRUD for services (providers only)
- ✅ Weekly schedule configuration per service
- ✅ Real-time availability calculation (avoids double-booking)
- ✅ Reservation creation with time conflict detection
- ✅ Optimistic concurrency control for reservation confirmation
- ✅ Asynchronous email notifications via Celery + Redis
- ✅ Comprehensive test suite (88% coverage)
- ✅ CI/CD pipeline with GitHub Actions (lint, type check, tests, coverage)
- ✅ Docker Compose for local development (web, db, redis, worker, mailpit)
- ✅ Deployed on Render (web + worker) with Neon (PostgreSQL) and Upstash (Redis)

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Database:** PostgreSQL 15 (Neon in production, Docker locally)
- **Cache / Broker:** Redis (Upstash in production, Docker locally)
- **ORM:** SQLAlchemy 2.0 (async), Alembic
- **Background Tasks:** Celery
- **Email:** Resend (production), Mailpit (local testing)
- **Testing:** Pytest, HTTPX, coverage
- **DevOps:** Docker, Docker Compose, Render, GitHub Actions

## Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

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

The API will be available at `http://localhost:8002/docs`.
Mailpit web interface at `http://localhost:8025`.

### 4. Apply database migrations
```bash
docker-compose exec web alembic upgrade head
```

## Concurrency Control

Reservation confirmation uses **optimistic locking**. Each reservation has a `version` field. When confirming, the client sends the expected version. If another process modified the reservation in the meantime, the version won't match and the API returns `409 Conflict`. This prevents accidental double confirmations.

## Project Structure

```
reservehub/
├── app/
│   ├── api/v1/endpoints/   # Route handlers
│   ├── core/               # Configuration, security, Celery
│   ├── db/                 # Async engine and session
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   └── tasks/              # Celery email tasks
├── tests/                  # Test suite (11 tests, 88% coverage)
├── alembic/                # Database migrations
├── .github/workflows/      # CI/CD and keep-alive
├── docker-compose.yml
├── Dockerfile
├── start.sh                # Startup script for Render
└── README.md
```

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.