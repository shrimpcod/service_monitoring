from datetime import datetime

from pydantic import BaseModel
from .state import StateRead

class ServiceRead(BaseModel):
    id: int
    name: str

    current_state: StateRead | None = None

    class Config:
        from_attributes = True

class SLAResponse(BaseModel):
    service_name: str
    start_date: datetime
    end_date: datetime
    sla_percentage: float
    downtime_seconds: float