from ..schemas import MilestoneCreate, MilestoneUpdate, MilestoneResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import validate_user
from ..services import MilestoneService
from fastapi import APIRouter, Depends
from ..database import db_session
from typing import List
from uuid import UUID


milestone_router = APIRouter(
    prefix="/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/milestones"
)
milestone_service = MilestoneService()


@milestone_router.get("/", response_model=List[MilestoneResponse])
async def get_milestones(
    org_id: UUID,
    team_id: UUID,
    proj_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await milestone_service.get_milestones(
        org_id, team_id, proj_id, current_user.id, db
    )


@milestone_router.post("/", response_model=MilestoneResponse)
async def create_milestone(
    org_id: UUID,
    team_id: UUID,
    proj_id: UUID,
    data: MilestoneCreate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await milestone_service.create_milestone(
        org_id, team_id, proj_id, data, current_user.id, db
    )


@milestone_router.get("/{milestone_id}", response_model=MilestoneResponse)
async def get_milestone(
    org_id: UUID,
    team_id: UUID,
    proj_id: UUID,
    milestone_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await milestone_service.get_milestone(
        org_id, team_id, proj_id, milestone_id, current_user.id, db
    )


@milestone_router.patch("/{milestone_id}", response_model=MilestoneResponse)
async def update_milestone(
    org_id: UUID,
    team_id: UUID,
    proj_id: UUID,
    milestone_id: UUID,
    data: MilestoneUpdate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await milestone_service.update_milestone(
        org_id, team_id, proj_id, milestone_id, data, current_user.id, db
    )


@milestone_router.delete("/{milestone_id}")
async def delete_milestone(
    org_id: UUID,
    team_id: UUID,
    proj_id: UUID,
    milestone_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await milestone_service.delete_milestone(
        org_id, team_id, proj_id, milestone_id, current_user.id, db
    )
