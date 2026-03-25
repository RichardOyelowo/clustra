from ..schemas import TeamMemberCreate, TeamMemberResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import TeamCreate, TeamResponse
from fastapi import APIRouter, Depends
from ..database import db_session
import uuid


team_router = APIRouter(prefix="/orgs/{org_id}/teams")


@team_router.post("/")
async def create_team(org_id: uuid.UUID, data: TeamCreate, db: AsyncSession = Depends(db_session)) -> TeamResponse:
    pass


@team_router.get("/")
async def get_teams(org_id: uuid.UUID,db: AsyncSession = Depends(db_session)):
    pass


@team_router.get("/{team_id}")
async def get_team(org_id: uuid.UUID, team_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@team_router.patch("/{team_id}")
async def edit_team(org_id: uuid.UUID, team_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@team_router.delete("/{team_id}")
async def delete_team(org_id: uuid.UUID, team_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@team_router.post("/{team_id}/members")
async def add_team_member(org_id: uuid.UUID, team_id: uuid.UUID, data: TeamMemberCreate, db:AsyncSession = Depends(db_session)) -> TeamMemberResponse:
    pass


@team_router.get("/{team_id}/members")
async def get_team_members(org_id: uuid.UUID, team_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@team_router.delete("/{team_id}/members/{id}")
async def delete_team_member(org_id: uuid.UUID, team_id: uuid.UUID, id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass
