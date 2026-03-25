from ..schemas import ProjectCreate, ProjectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from database import db_session
import uuid

proj_router = APIRouter(prefix="/orgs/{org_id}/teams/{team_id}/projects")


@proj_router.get("/")
async def get_projects(org_id: uuid.UUID, team_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@proj_router.post("/")
async def create_projects(org_id: uuid.UUID, team_id: uuid.UUID, data: ProjectCreate, db: AsyncSession = Depends(db_session)) -> ProjectResponse:
    pass


@proj_router.patch("/{proj_id}")
async def edit_project(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: proj_id, db: AsyncSession = Depends(db_session)):
    pass


@proj_router.delete("/{proj_id}")
async def delete_project(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: proj_id, db: AsyncSession = Depends(db_session)):
    pass


