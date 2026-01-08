from pydantic import BaseModel
from datetime import datetime
from app.models.state import ServiceStatus

class StateCreate(BaseModel):
    name: str
    status: ServiceStatus
    description: str | None = None

class StateRead(BaseModel):
    status: ServiceStatus
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True