import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base

class ServiceStatus(str, enum.Enum):
    working = "working"
    not_working = "not_working"
    unstable = "unstable"

class ServiceState(Base):
    __tablename__ = 'service_states'
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    status = Column(Enum(ServiceStatus), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    service = relationship("Service", back_populates="states")


