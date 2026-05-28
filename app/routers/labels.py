from ..schemas import LabelCreate, LabelUpdate, LabelResponse
from ..schemas import TaskLabelCreate, TaskLabelResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import validate_user
from fastapi import APIRouter, Depends
from ..services import LabelService
from ..database import db_session
from typing import List
from uuid import UUID

label_router = APIRouter(prefix="/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/labels")
label_service = LabelService()


# ---------------- Project Label ------------------
@label_router.get("/", response_model=List[LabelResponse])
async def get_labels(org_id: UUID, team_id: UUID, proj_id: UUID, current_user = Depends(validate_user), db: AsyncSession = Depends(db_session)):
    return await label_service.get_labels(org_id, team_id, proj_id, current_user.id, db)


@label_router.post("/", response_model=LabelResponse)
async def create_label(org_id: UUID, team_id: UUID, proj_id: UUID, data: LabelCreate, current_user = Depends(validate_user), db: AsyncSession = Depends(db_session)):
    return await label_service.create_label(org_id, team_id, proj_id, data, current_user.id, db)


@label_router.get("/{label_id}", response_model=LabelResponse)
async def get_label(org_id: UUID, team_id: UUID, proj_id: UUID, label_id: UUID, current_user = Depends(validate_user), db: AsyncSession = Depends(db_session)):
    return await label_service.get_label(org_id, team_id, proj_id, label_id, current_user.id, db)


@label_router.patch("/{label_id}", response_model=LabelResponse)
async def update_label(org_id: UUID, team_id: UUID, proj_id: UUID, label_id: UUID, data: LabelUpdate, current_user = Depends(validate_user), db: AsyncSession = Depends(db_session)):
    return await label_service.update_label(org_id, team_id, proj_id, label_id, data, current_user.id, db)


@label_router.delete("/{label_id}")
async def delete_label(org_id: UUID, team_id: UUID, proj_id: UUID, label_id: UUID, current_user = Depends(validate_user), db: AsyncSession = Depends(db_session)):
    return await label_service.delete_label(org_id, team_id, proj_id, label_id, current_user.id, db)


# ------------------ Task Label ---------------------
@label_router.get("/{label_id}/task_label", response_model=List[TaskLabelResponse])
async def get_task_labels(org_id: UUID, team_id: UUID, label_id: UUID, current_user = Depends(validate_user), db: AsyncSession = Depends(db_session)):
    return await label_service.get_task_labels(org_id, team_id, label_id, current_user.id, db)


@label_router.post("/{label_id}/task_label/", response_model=TaskLabelResponse)
async def create_task_label(org_id: UUID, team_id: UUID, label_id: UUID, data: TaskLabelCreate, current_user = Depends(validate_user), db: AsyncSession = Depends(db_session)):
    return await label_service.create_task_label(org_id, team_id, label_id, data, current_user.id, db)


@label_router.get("/{label_id}/task_label/{task_label_id}", response_model=TaskLabelResponse)
async def get_task_label(org_id: UUID, team_id: UUID, label_id: UUID, task_label_id: UUID, current_user = Depends(validate_user), db: AsyncSession = Depends(db_session)):
    return await label_service.get_task_label(org_id, team_id, label_id, task_label_id, current_user.id, db)


@label_router.delete("/{label_id}/task_label/{task_label_id}")
async def delete_task_label(org_id: UUID, team_id: UUID, label_id: UUID, task_label_id: UUID, current_user = Depends(validate_user), db: AsyncSession = Depends(db_session)):
    return await label_service.delete_task_label(org_id, team_id, label_id, task_label_id, current_user.id, db)

