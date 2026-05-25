from ..schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import validate_user
from fastapi import APIRouter, Depends
from ..services import ProjectService
from ..database import db_session
from typing import List
from uuid import UUID


proj_router = APIRouter(prefix="/orgs/{org_id}/teams/{team_id}/projects")
proj_service = ProjectService()


@proj_router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    org_id: UUID,
    team_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await proj_service.get_projects(org_id, team_id, current_user.id, db)


@proj_router.post("/", response_model=ProjectResponse)
async def create_projects(
    org_id: UUID,
    team_id: UUID,
    data: ProjectCreate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await proj_service.create_project(org_id, team_id, data, current_user.id, db)


@proj_router.get("/{proj_id}", response_model=ProjectResponse)
async def get_project(
    org_id: UUID,
    team_id: UUID,
    proj_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await proj_service.get_project(org_id, team_id, proj_id, current_user.id, db)


@proj_router.patch("/{proj_id}", response_model=ProjectResponse)
async def update_project(
    org_id: UUID,
    team_id: UUID,
    proj_id: UUID,
    data: ProjectUpdate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await proj_service.update_project(org_id, team_id, proj_id, data, current_user.id, db)


@proj_router.delete("/{proj_id}")
async def delete_project(
    org_id: UUID,
    team_id: UUID,
    proj_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await proj_service.delete_project(org_id, team_id, proj_id, current_user.id, db)
