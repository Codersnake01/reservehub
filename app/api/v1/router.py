from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, services, schedules, availability, reservations

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(schedules.router, tags=["schedules"])
api_router.include_router(availability.router, tags=["availability"])
api_router.include_router(reservations.router, tags=["reservations"])