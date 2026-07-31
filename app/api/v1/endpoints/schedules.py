from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.schedule import Schedule
from app.models.service import Service
from app.schemas.schedule import ScheduleCreate, ScheduleResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/services/{service_id}/schedules", response_model=list[ScheduleResponse])
async def list_schedules(
    service_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Schedule).where(Schedule.service_id == service_id))
    return result.scalars().all()

@router.post("/services/{service_id}/schedules", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    service_id: int,
    schedule_in: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verificar que el servicio existe y pertenece al provider
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalars().first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    schedule = Schedule(
        service_id=service_id,
        day_of_week=schedule_in.day_of_week,
        start_time=schedule_in.start_time,
        end_time=schedule_in.end_time,
    )
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule

@router.put("/schedules/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_in: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Schedule).where(Schedule.id == schedule_id))
    schedule = result.scalars().first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    # Verificar propiedad a través del servicio
    srv_result = await db.execute(select(Service).where(Service.id == schedule.service_id))
    service = srv_result.scalars().first()
    if service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    schedule.day_of_week = schedule_in.day_of_week
    schedule.start_time = schedule_in.start_time
    schedule.end_time = schedule_in.end_time
    await db.commit()
    await db.refresh(schedule)
    return schedule

@router.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Schedule).where(Schedule.id == schedule_id))
    schedule = result.scalars().first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    srv_result = await db.execute(select(Service).where(Service.id == schedule.service_id))
    service = srv_result.scalars().first()
    if service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await db.delete(schedule)
    await db.commit()