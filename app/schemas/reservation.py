from datetime import datetime

from pydantic import BaseModel


class ReservationCreate(BaseModel):
    service_id: int
    start_time: datetime


class ReservationResponse(BaseModel):
    id: int
    client_id: int
    service_id: int
    start_time: datetime
    end_time: datetime
    status: str
    version: int
    created_at: datetime

    model_config = {"from_attributes": True}
