from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta, date, time, timezone
from app.db.session import get_db
from app.models.service import Service
from app.models.schedule import Schedule
from app.models.reservation import Reservation, ReservationStatus

router = APIRouter()

@router.get("/services/{service_id}/availability")
async def get_availability(
    service_id: int,
    date_str: str = Query(..., alias="date"),
    db: AsyncSession = Depends(get_db),
):
    # Validar formato de fecha
    try:
        query_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Obtener el servicio
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalars().first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Obtener horarios para el día de la semana
    day_of_week = query_date.weekday()
    sched_result = await db.execute(
        select(Schedule).where(
            Schedule.service_id == service_id,
            Schedule.day_of_week == day_of_week,
        )
    )
    schedules = sched_result.scalars().all()
    if not schedules:
        return []

    # Generar slots libres usando datetime aware (UTC)
    free_slots = []
    for sched in schedules:
        current = datetime.combine(query_date, sched.start_time, tzinfo=timezone.utc)
        end = datetime.combine(query_date, sched.end_time, tzinfo=timezone.utc)
        while current + timedelta(minutes=service.duration_minutes) <= end:
            slot_end = current + timedelta(minutes=service.duration_minutes)
            free_slots.append({
                "start": current.isoformat(),
                "end": slot_end.isoformat(),
            })
            current += timedelta(minutes=service.duration_minutes)

    # Filtrar slots ocupados por reservas no canceladas
    start_of_day = datetime.combine(query_date, time.min, tzinfo=timezone.utc)
    end_of_day = datetime.combine(query_date, time.max, tzinfo=timezone.utc)
    res_result = await db.execute(
        select(Reservation).where(
            Reservation.service_id == service_id,
            Reservation.start_time >= start_of_day,
            Reservation.start_time <= end_of_day,
            Reservation.status != ReservationStatus.CANCELLED,
        )
    )
    reservations = res_result.scalars().all()

    for res in reservations:
        res_start = res.start_time
        res_end = res.end_time
        free_slots = [
            slot for slot in free_slots
            if not (datetime.fromisoformat(slot["start"]) < res_end and datetime.fromisoformat(slot["end"]) > res_start)
        ]

    return free_slots