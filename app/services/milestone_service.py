from ..schemas import MilestoneCreate, MilestoneResponse, MilestoneUpdate
from ..utils.normalization import normalize_payloads
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Milestone
from fastapi import HTTPException
from sqlalchemy import select
from typing import List
from uuid import UUID


class MilestoneService:
    """
    service class for milestone route related operations
    """

    async def create_milestone(self, data: MilestoneCreate, db: AsyncSession) -> Milestone:
        try:
            result = await db.execute(select(Milestone).where(
                Milestone.title == data.title,
                Milestone.proj_id == data.proj_id
            ))
            existing = result.scalar_one_or_none()

            if existing:
                raise HTTPException(status_code=409, detail="Milestone already exists")

            milestone = Milestone(**normalize_payloads(data.model_dump()))

            db.add(milestone)
            await db.commit()
            await db.refresh(milestone)

            return milestone
        except Exception as e:
            await db.rollback()
            raise e


    async def get_milestones(self, proj_id: UUID, db: AsyncSession) -> List[Milestone]:
        try:
            result = await db.execute(select(Milestone).where(Milestone.proj_id == proj_id))
            milestones = result.scalars().all()

            return milestones
        except Exception as e:
            await db.rollback()
            raise e


    async def get_milestone(self, milestone_id: UUID, db: AsyncSession) -> Milestone:
        try:
            result = await db.execute(select(Milestone).where(Milestone.id == milestone_id))
            milestone = result.scalar_one_or_none()

            if not milestone:
                raise HTTPException(status_code=404, detail="Milestone doesn't exist")

            return milestone
        except Exception as e:
            await db.rollback()
            raise e


    async def edit_milestone(self, milestone_id: UUID, data: MilestoneUpdate, db: AsyncSession) -> Milestone:
        try:
            result = await db.execute(select(Milestone).where(Milestone.id == milestone_id))
            milestone = result.scalar_one_or_none()

            if not milestone:
                raise HTTPException(status_code=404, detail="Milestone doesn't exist")

            data_dict = data.model_dump(exclude_unset=True)
            if not data_dict:
                return milestone

            updated_data = normalize_payloads(data_dict)
            for field, value in updated_data.items():
                setattr(milestone, field, value)

            await db.commit()
            await db.refresh(milestone)

            return milestone
        except Exception as e:
            await db.rollback()
            raise e


    async def delete_milestone(self, milestone_id: UUID, db: AsyncSession) -> dict:
        try:
            result = await db.execute(select(Milestone).where(Milestone.id == milestone_id))
            milestone = result.scalar_one_or_none()

            if not milestone:
                raise HTTPException(status_code=404, detail="Milestone doesn't exist")

            await db.delete(milestone)
            await db.commit()

            return {"message": "Milestone deleted successfully"}
        except Exception as e:
            await db.rollback()
            raise e