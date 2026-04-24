from ..schemas import ActivityCreate, ActivityResponse
from ..utils.normalization import normalize_payloads
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..models import Activity
from sqlalchemy import select
from uuid import UUID


class ActivityService:
    """
    service class for Activity routes operations
    """

    async def create_activity(self, org_id: UUID, data: ActivityCreate, db: AsyncSession):
        data_dict = data.model_dump()
        activity = Activity(**normalize_payloads(data_dict), org_id=org_id)

        db.add(activity)
        await db.commit()
        await db.refresh(activity)

        return activity


    async def get_activities(self, org_id: UUID, db: AsyncSession):
        result = await db.execute(select(Activity).where(Activity.org_id == org_id))
        activities = result.scalars().all()

        if not activities: return []

        return activities


    async def get_activity(self, activity_id: UUID, db: AsyncSession):
        result = await db.execute(select(Activity).where(Activity.id == activity_id))
        activity = result.scalar_one_or_none()

        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        return activity


    async def delete_activity(self, activity_id: UUID, db: AsyncSession):
        result = await db.execute(select(Activity).where(Activity.id == activity_id))
        activity = result.scalar_one_or_none()

        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        await db.delete(activity)
        await db.commit()

        return {"message": "Activity deleted successfully"}
