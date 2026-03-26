from ..schemas import MilestoneCreate, MilestoneResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from ..database import db_session
import uuid

milestone_router = APIRouter(prefix="/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/milestones")

@milestone_router.get("/")
async def get_milestones(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@milestone_router.post("/")
async def create_milestone(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, data: MilestoneCreate, db: AsyncSession = Depends(db_session)) -> MilestoneResponse:
    pass


@milestone_router.get("/{milestone_id}")
async def get_milestone(org_id: uuid.UUID, team_id:uuid.UUID, proj_id: uuid.UUID, milestone_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@milestone_router.patch("/{milestone_id}")
async def edit_milestone(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, milestone_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@milestone_router.delete("/{milestone_id}")
async def delete_milestone(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, milestone_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass
