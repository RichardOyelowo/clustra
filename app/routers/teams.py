from app.schemas.org import OrganizationMemberCreate, OrganizationMemberResponse
from ..schemas import TeamMemberCreate, TeamMemberResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import TeamCreate, TeamResponse
from fastapi import APIRouter, Depends
from ..database import db_session
import uuid


team_router = APIRouter(prefix="/orgs/{org_id}/teams")


@team_router.post("/")
def create_team(org_id: uuid.UUID, data: TeamCreate, db: AsyncSession = Depends(db_session)) -> TeamResponse:
    pass


@team_router.get("/{team_id}")
def get_team(org_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@team_router.patch("/{team_id}")
def edit_team(org_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@team_router.delete("/team_id}")
def delete_team(org_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@team_router.post("/teams/{team_id}/members")
def add_team_member(org_id: uuid.UUID, data: TeamMemberCreate, db:AsyncSession = Depends(db_session)) -> TeamMemberResponse:
    pass


@team_router.get("/teams/{team_id}/members")
def get_team_members(org_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@team_router.delete("/teams/{team_id}/members/{id}")
def delete_team_member(org_id: uuid.UUID, id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass
