
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/v1",
    tags=["System Status"],
)


class SystemStatus(BaseModel):
    service: str
    version: str
    status: str
    timestamp: datetime
    visualization_mode: str


@router.get("/status", response_model=SystemStatus)
async def system_status():
    return SystemStatus(
        service="ORBITAL",
        version="1.0.0",
        status="operational",
        timestamp=datetime.now(timezone.utc),
        visualization_mode="simulation",
    )
