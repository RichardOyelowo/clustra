from ..schemas import TaskCreate, TaskResponse, TaskUpdate
from ..utils.normalization import normalize_payloads
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from ..models import Task
from uuid import UUID


class TaskService:
    """
    service class for task routes operations
    """

    async def create_task(self, data: TaskCreate, db: AsyncSession):
        result = await db.execute(select(Task).where(
            Task.name == data.name,
            Task.proj_id == data.proj_id))
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="Task already exists")
  
        data_dict = data.model_dump()
        data_dict = normalize_payloads(data_dict)
        task = Task(**data_dict)

        db.add(task)
        await db.commit()
        await db.refresh(task)

        return task


    async def get_tasks(self, proj_id: UUID, db: AsyncSession):
        result = await db.execute(select(Task).where(Task.proj_id == proj_id))
        tasks = result.scalars().all()
        
        if not tasks:
            return []

        return tasks


    async def get_task(self, task_id: UUID, db: AsyncSession):
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
            
        return task


    async def edit_task(self, task_id: UUID, data: TaskUpdate, db: AsyncSession):
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
            
        updated_data = normalize_payloads(data.model_dump(exclude_unset=True))
        for field, value in updated_data.items():
            setattr(task, field, value)
            
        await db.commit()
        await db.refresh(task)
        return task


    async def delete_task(self, task_id: UUID, db: AsyncSession):
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
            
        await db.delete(task)
        await db.commit()
        return {"message": "Task deleted successfully"}
 
