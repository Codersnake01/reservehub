from pydantic import BaseModel


class ConfirmReservationRequest(BaseModel):
    version: int
