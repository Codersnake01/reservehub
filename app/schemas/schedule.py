from pydantic import BaseModel
from datetime import time

class ScheduleCreate(BaseModel):
    day_of_week: int  # 0=Lunes, 6=Domingo
    start_time: time
    end_time: time

class ScheduleResponse(BaseModel):
    id: int
    service_id: int
    day_of_week: int
    start_time: time
    end_time: time

    model_config = {"from_attributes": True}