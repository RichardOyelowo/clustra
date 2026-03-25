from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import TaskCreate, TaskResponse
from fastapi import APIRouter, Depends
from ..database import db_session
import uuid


task_router = APIRouter(prefix="/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/task")


@task_router.get("/")
async def get_tasks(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@task_router.post("/")
async def create_tasks(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, data: TaskCreate, db: AsyncSession = Depends(db_session)) -> TaskResponse:
    pass


@task_router.get("/{task_id}")
async def get_task(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, task_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@task_router.patch("/{task_id}")
async def edit_task(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, task_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@task_router.delete("/{task_id}")
async def delete_task(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, task_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass

