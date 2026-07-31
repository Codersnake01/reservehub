from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from app.db.session import get_db
from app.models.reservation import Reservation, ReservationStatus
from app.models.service import Service
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.tasks.email_tasks import send_confirmation_email

router = APIRouter()

@router.post("/reservations", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation_in: ReservationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can make reservations")

    result = await db.execute(select(Service).where(Service.id == reservation_in.service_id))
    service = result.scalars().first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    start_time = reservation_in.start_time
    end_time = start_time + timedelta(minutes=service.duration_minutes)

    overlapping = await db.execute(
        select(Reservation).where(
            Reservation.service_id == service.id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time,
            Reservation.status != ReservationStatus.CANCELLED,
        )
    )
    if overlapping.scalars().first():
        raise HTTPException(status_code=409, detail="Time slot is already booked")

    reservation = Reservation(
        client_id=current_user.id,
        service_id=service.id,
        start_time=start_time,
        end_time=end_time,
        status=ReservationStatus.PENDING,
    )
    db.add(reservation)
    await db.commit()
    await db.refresh(reservation)
    return reservation

@router.patch("/reservations/{reservation_id}/confirm", response_model=ReservationResponse)
async def confirm_reservation(
    reservation_id: int,
    version: int = Body(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    reservation = result.scalars().first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Verificar que el usuario sea el dueño de la reserva o un admin
    if reservation.client_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Control de concurrencia con bloqueo optimista
    if reservation.version != version:
        raise HTTPException(
            status_code=409,
            detail="Conflict: reservation has been modified by another process. Please refresh and try again."
        )

    # Confirmar la reserva
    reservation.status = ReservationStatus.CONFIRMED
    reservation.version += 1
    await db.commit()
    await db.refresh(reservation)

    # Disparar tarea de envío de email de confirmación
    send_confirmation_email.delay(reservation.id, current_user.email)

    return reservation

@router.post("/reservations/{reservation_id}/test-email", status_code=status.HTTP_200_OK)
async def test_email(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    reservation = result.scalars().first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    task = send_confirmation_email.delay(reservation.id, current_user.email)
    return {"message": "Tarea de email enviada a Celery", "task_id": task.id}