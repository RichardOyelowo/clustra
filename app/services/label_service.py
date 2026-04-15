from ..schemas import LabelCreate, LabelResponse, LabelUpdate
from ..schemas import TaskLabelCreate, TaskLabelResponse
from ..utils.normalization import normalize_payloads
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..models import Label, TaskLabel
from sqlalchemy import select, values
from uuid import UUID


class LabelService:
    """
    service class for label route related operations
    """

    async def create_label(self, data: LabelCreate, db: AsyncSession):
        result = await db.execute(select(Label).where(
            Label.name == data.name,
            Label.proj_id == data.proj_id
        ))
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="label already exists")

        label = Label(**normalize_payloads(data.model_dump()))

        db.add(label)
        await db.commit()
        await db.refresh(label)

        return label


    async def get_labels(self, proj_id: UUID, db: AsyncSession):
        result = await db.execute(select(Label).where(Label.proj_id == data.proj_id))
        labels = result.scalars().all()

        if not labels: return []

        return labels


    async def get_label(self, label_id: UUID, proj_id: UUID, db: AsyncSession):
        result = await db.execute(select(Label).where(
            Label.id == label_id,
            Label.proj_id == proj_id
        ))
        label = result.scalar_one_or_none()

        if not label: raise HTTPException(status_code=404, detail="Label doesn't exist")

        return label


    async def edit_label(self, label_id: UUID, data: LabelUpdate, db: AsyncSession):
        result =  await db.execute(select(Label).where(
            Label.id == label_id,
            Label.proj_id == data.proj_id
        ))
        label = result.scalar_one_or_none()

        if not label:
            raise HTTPException(status_code=404, detail="Label doesn't exist")

        data_dict = data.model_dump(exclude_unset=True)
        if not data_dict:
            return label

        updated_data = normalize_payloads(data_dict)
        for field, value in updated_data.items():
            setattr(label,field,value)

        await db.commit()
        await db.refresh(label)
        
        return label


    async def delete_label(self, label_id: UUID, proj_id: UUID, db: AsyncSession):
        result = await db.execute(select(Label).where(
            Label.id == label_id, 
            Label.proj_id == proj_id
        ))
        label = result.scalar_one_or_none()

        if not label:
            raise HTTPException(status_code=404, detail="Label doesn't exists")

        await db.delete(label)
        await db.commit()
        await db.refresh(label)

        return {"message": "label deleted successfully"}
