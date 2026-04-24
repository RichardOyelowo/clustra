from ..schemas import TaskLabelCreate, TaskLabelResponse, TaskLabelUpdate
from ..schemas import LabelCreate, LabelResponse, LabelUpdate
from ..utils.normalization import normalize_payloads
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Label, TaskLabel
from fastapi import HTTPException
from sqlalchemy import select
from typing import List
from uuid import UUID


class LabelService:
    """
    service class for label route related operations
    """

    # ---------------- Project Label ------------------

    async def create_label(self, data: LabelCreate, db: AsyncSession) -> Label:
        try:
            result = await db.execute(select(Label).where(
                Label.name == data.name,
                Label.proj_id == data.proj_id
            ))
            existing = result.scalar_one_or_none()

            if existing:
                raise HTTPException(status_code=409, detail="Label already exists")

            label = Label(**normalize_payloads(data.model_dump()))

            db.add(label)
            await db.commit()
            await db.refresh(label)

            return label
        except Exception as e:
            await db.rollback()
            raise e


    async def get_labels(self, proj_id: UUID, db: AsyncSession) -> List[Label]:
        try:
            result = await db.execute(select(Label).where(Label.proj_id == proj_id))
            labels = result.scalars().all()

            return labels
        except Exception as e:
            await db.rollback()
            raise e


    async def get_label(self, label_id: UUID, proj_id: UUID, db: AsyncSession) -> Label:
        try:

            result = await db.execute(select(Label).where(
                Label.id == label_id,
                Label.proj_id == proj_id
            ))
            label = result.scalar_one_or_none()

            if not label: raise HTTPException(status_code=404, detail="Label doesn't exist")

            return label
        except Exception as e:
            await db.rollback()
            raise e


    async def edit_label(self, label_id: UUID, data: LabelUpdate, db: AsyncSession) -> Label:
        try:
            result =  await db.execute(select(Label).where(
                Label.id == label_id,
                Label.proj_id == data.proj_id
            ))
            label = result.scalar_one_or_none()

            if not label:
                raise HTTPException(status_code=404, detail="Label doesn't exists")

            data_dict = data.model_dump(exclude_unset=True)
            if not data_dict:
                return label

            updated_data = normalize_payloads(data_dict)
            for field, value in updated_data.items():
                setattr(label,field,value)

            await db.commit()
            await db.refresh(label)
            
            return label
        except Exception as e:
            await db.rollback()
            raise e


    async def delete_label(self, label_id: UUID, proj_id: UUID, db: AsyncSession) -> dict:
        try:
            result = await db.execute(select(Label).where(
                Label.id == label_id, 
                Label.proj_id == proj_id
            ))
            label = result.scalar_one_or_none()

            if not label:
                raise HTTPException(status_code=404, detail="Label doesn't exists")

            await db.delete(label)
            await db.commit()
            
            return {"message": "label deleted successfully"}
        except Exception as e:
            await db.rollback()
            raise e


    # ------------------ Task Label ---------------------

    async def create_task_label(self, data: TaskLabelCreate, db: AsyncSession) -> TaskLabel:
        try:
            result = await db.execute(select(TaskLabel).where(
                TaskLabel.label_id == data.label_id,
                TaskLabel.task_id == data.task_id
            ))
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=409, detail="Task Label already exists")

            task_label = TaskLabel(**normalize_payloads(data.model_dump()))

            db.add(task_label)
            await db.commit()
            await db.refresh(task_label)

            return task_label
        except Exception as e:
            await db.rollback()
            raise e


    async def get_task_labels(self, task_id: UUID, db: AsyncSession) -> List[TaskLabel]:
        result = await db.execute(select(TaskLabel).where(TaskLabel.task_id == task_id))
        task_labels = result.scalars().all()

        return task_labels


    async def get_task_label(self, task_label_id: UUID, db: AsyncSession) -> TaskLabel:
        result = await db.execute(select(TaskLabel).where(TaskLabel.id == task_label_id))
        task_label = result.scalar_one_or_none()

        if not task_label:
            raise HTTPException(status_code=404, detail="Task Label doesn't exist")

        return task_label


    async def edit_task_label(self, task_label_id: UUID, data: TaskLabelCreate, db: AsyncSession) -> TaskLabel:
        try:
            result = await db.execute(select(TaskLabel).where(TaskLabel.id == task_label_id))
            task_label = result.scalar_one_or_none()

            if not task_label:
                raise HTTPException(status_code=404, detail="Task Label doesn't exist")

            data_dict = data.model_dump(exclude_unset=True)
            if not data_dict:
                return task_label

            updated_data = normalize_payloads(data_dict)
            for field, value in updated_data.items():
                setattr(task_label, field, value)

            await db.commit()
            await db.refresh(task_label)

            return task_label
        except Exception as e:
            await db.rollback()
            raise e


    async def delete_task_label(self, task_label_id: UUID, db: AsyncSession) -> dict:
        try:
            result = await db.execute(select(TaskLabel).where(TaskLabel.id == task_label_id))
            task_label = result.scalar_one_or_none()
            if not task_label:
                raise HTTPException(status_code=404, detail="Task Label doesn't exist")

            await db.delete(task_label)
            await db.commit()

            return {"message": "Task label deleted successfully"}
        except Exception as e:
            await db.rollback()
            raise e


    async def get_task_labels_by_label(self, label_id: UUID, db: AsyncSession) -> List[TaskLabel]:
        result = await db.execute(select(TaskLabel).where(TaskLabel.label_id == label_id))
        task_labels = result.scalars().all()

        return task_labels

