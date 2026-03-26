from decimal import DecimalException
from ..schemas import TaskLabelCreate, TaskLabelResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from ..schemas import LabelCreate, LabelResponse
from fastapi import APIRouter, Depends
from ..database import db_session
import uuid

label_router = APIRouter(prefix="/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/labels")


# ---------------- Project Label ------------------
@label_router.get("/")
async def get_labels(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@label_router.post("/")
async def create_label(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, data: LabelCreate, db: AsyncSession = Depends(db_session)) -> LabelResponse:
    pass


@label_router.get("/{label_id}")
async def get_label(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, label_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@label_router.patch("/{label_id}")
async def edit_label(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, label_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@label_router.delete("/{label_id}")
async def delete_label(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uui.UUID, label_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


# ------------------ Task Label ---------------------
@label_router.get("/{label_id}/task_label")
async def get_task_labels(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, label_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@label_router.post("/{label_id}/task_label/")
async def create_task_label(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, label_id: uuid.UUID, data: TaskLabelCreate, db: AsyncSession = Depends(db_session)) -> TaskLabelResponse:
    pass


@label_router.get("/{label_id}/task_label/{task_label_id}")
async def get_task_label(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, label_id: uuid.UUID, task_label_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@label_router.patch("/{label_id}/task_label/{task_label_id}")
async def edit_task_label(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, label_id: uuid.UUID, task_label_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@label_router.delete("/{label_id}/task_label/{task_label_id}")
async def delete_task_label(org_id: uuid.UUID, team_id: uuid.UUID, proj_id: uuid.UUID, label_id: uuid.UUID, task_label_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass

