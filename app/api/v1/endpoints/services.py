from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.models.service import Service
from app.models.state import ServiceState
from app.schemas.state import StateCreate, StateRead
from app.schemas.service import ServiceRead
from app.schemas.service import SLAResponse
from app.services.sla_calculator import calculate_sla

router = APIRouter()

@router.post("/states", response_model=StateRead)
async def create_service_state(
        state_data: StateCreate,
        db:AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Service).where(Service.name == state_data.name))
    service = result.scalars().first()

    if not service:
        service = Service(name = state_data.name)
        db.add(service)
        await db.flush()

    new_state = ServiceState(
        service_id=service.id,
        status=state_data.status,
        description=state_data.description,
    )

    db.add(new_state)
    await db.commit()
    await db.refresh(new_state)
    return new_state

@router.get("/", response_model=List[ServiceRead])
async def list_services(
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Service).options(selectinload(Service.states))
    )
    services = result.scalars().all()

    for service in services:
        if service.states:
            service.current_state = sorted(service.states, key=lambda x: x.created_at, reverse=True)[0]
        else:
            service.current_state = None

    return services

@router.get("/{name}/history", response_model=List[StateRead])
async def get_service_history(
        name: str,
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Service).where(Service.name == name).options(selectinload(Service.states))
    )
    service = result.scalars().first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return sorted(service.states, key=lambda x: x.created_at, reverse=True)

@router.get("/{name}/sla", response_model=SLAResponse)
async def get_service_sla(
        name: str,
        start_date: datetime,
        end_date: datetime,
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Service)
        .where(Service.name == name)
        .options(selectinload(Service.states))
    )
    service = result.scalars().first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    sla_data = calculate_sla(
        service_name = service.name,
        states = service.states,
        start_date=start_date,
        end_date=end_date,
    )

    return sla_data