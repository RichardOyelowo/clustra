from ..schemas import ActivityCreate, ActivityResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from ..database import db_session
import uuid

activity_router = APIRouter(prefix="/orgs/{org_id}/activities")


@activity_router.get("/")
async def get_activities(org_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@activity_router.get("/{activity_id}")
async def get_activity(org_id: uuid.UUID, activity_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass