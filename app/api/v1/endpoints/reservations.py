from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from app.db.session import get_db
from app.models.reservation import Reservation, ReservationStatus
from app.models.service import Service
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.api.deps import get_current_user
from app.models.user import User

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