from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import validate_user
from ..services import ActivityService
from fastapi import APIRouter, Depends
from ..schemas import ActivityResponse
from ..database import db_session
from typing import List
import uuid

activity_router = APIRouter(prefix="/orgs/{org_id}")
activity_service = ActivityService()


@activity_router.get("/activity", response_model=List[ActivityResponse])
async def get_org_activity(
    org_id: uuid.UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await activity_service.get_org_activity(org_id, current_user.id, db)


@activity_router.get(
    "/teams/{team_id}/projects/{proj_id}/activity",
    response_model=List[ActivityResponse],
)
async def get_project_activity(
    org_id: uuid.UUID,
    team_id: uuid.UUID,
    proj_id: uuid.UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await activity_service.get_project_activity(
        org_id, team_id, proj_id, current_user.id, db
    )

