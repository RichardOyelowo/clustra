from ..schemas import TaskCreate, TaskResponse, TaskUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import validate_user 
from fastapi import APIRouter, Depends
from ..services import TaskService
from ..database import db_session
from typing import List
import uuid


task_router = APIRouter(prefix="/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/tasks")
task_service = TaskService()


@task_router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    org_id: uuid.UUID,
    team_id: uuid.UUID,
    proj_id: uuid.UUID,
    current_user = Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await task_service.get_tasks(org_id, team_id, proj_id, current_user.id, db)


@task_router.post("/", response_model=TaskResponse)
async def create_task(
    org_id: uuid.UUID,
    team_id: uuid.UUID,
    proj_id: uuid.UUID,
    data: TaskCreate,
    current_user = Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await task_service.create_task(org_id, team_id, proj_id, data, current_user.id, db)


@task_router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    org_id: uuid.UUID,
    team_id: uuid.UUID,
    proj_id: uuid.UUID,
    task_id: uuid.UUID,
    current_user = Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await task_service.get_task(org_id, team_id, proj_id, task_id, current_user.id, db)


@task_router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    org_id: uuid.UUID,
    team_id: uuid.UUID,
    proj_id: uuid.UUID,
    task_id: uuid.UUID,
    data: TaskUpdate,
    current_user = Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await task_service.update_task(org_id, team_id, proj_id, task_id, data, current_user.id, db)


@task_router.delete("/{task_id}")
async def delete_task(
    org_id: uuid.UUID,
    team_id: uuid.UUID,
    proj_id: uuid.UUID,
    task_id: uuid.UUID,
    current_user = Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await task_service.delete_task(org_id, team_id, proj_id, task_id, current_user.id, db)
