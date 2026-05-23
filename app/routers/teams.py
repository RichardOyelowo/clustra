from ..schemas import TeamMemberCreate, TeamMemberResponse
from ..schemas import TeamCreate, TeamResponse, TeamUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import validate_user
from fastapi import APIRouter, Depends
from ..services import TeamService
from ..database import db_session
from typing import List
from uuid import UUID


team_router = APIRouter(prefix="/orgs/{org_id}/teams")
team_service = TeamService()


@team_router.post("/", response_model=TeamResponse)
async def create_team(
    org_id: UUID,
    data: TeamCreate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await team_service.create_team(org_id, data, current_user.id, db)


@team_router.get("/", response_model=List[TeamResponse])
async def get_teams(
    org_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await team_service.get_teams(org_id, current_user.id, db)


@team_router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    org_id: UUID,
    team_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await team_service.get_team(org_id, team_id, current_user.id, db)


@team_router.patch("/{team_id}", response_model=TeamResponse)
async def update_team(
    org_id: UUID,
    team_id: UUID,
    data: TeamUpdate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await team_service.update_team(org_id, team_id, data, current_user.id, db)


@team_router.delete("/{team_id}")
async def delete_team(
    org_id: UUID,
    team_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await team_service.delete_team(org_id, team_id, current_user.id, db)


@team_router.post("/{team_id}/members", response_model=TeamMemberResponse)
async def add_team_member(
    org_id: UUID,
    team_id: UUID,
    data: TeamMemberCreate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await team_service.add_member(org_id, team_id, data, current_user.id, db)


@team_router.get("/{team_id}/members", response_model=List[TeamMemberResponse])
async def get_team_members(
    org_id: UUID,
    team_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await team_service.get_members(org_id, team_id, current_user.id, db)


@team_router.get("/{team_id}/members/{member_id}", response_model=TeamMemberResponse)
async def get_team_member(
    org_id: UUID,
    team_id: UUID,
    member_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await team_service.get_member(
        org_id, team_id, member_id, current_user.id, db
    )


@team_router.delete("/{team_id}/members/{member_id}")
async def remove_team_member(
    org_id: UUID,
    team_id: UUID,
    member_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await team_service.remove_member(
        org_id, team_id, member_id, current_user.id, db
    )
