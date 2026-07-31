from pydantic import BaseModel

class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    duration_minutes: int
    price: float | None = None

class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    duration_minutes: int | None = None
    price: float | None = None

class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    duration_minutes: int
    price: float | None = None
    provider_id: int

    model_config = {"from_attributes": True}