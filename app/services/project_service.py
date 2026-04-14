from ..schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from ..utils.normalization import normalize_payloads
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..models  import Project
from sqlalchemy import select
from uuid import UUID


class ProjectService:
    """
    service class for project routes operations
    """

    async def create_project(self, data: ProjectCreate, db: AsyncSession):
        result = await db.execute(select(Project).where(
            Project.name == data.name,
            Project.team_id == data.team_id))
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="Project already exists")
  
        data_dict = data.model_dump()
        data_dict = normalize_payloads(data_dict)
        project = Project(**data_dict)

        db.add(project)
        await db.commit()
        await db.refresh(project)

        return project


    async def get_projects(self, team_id: UUID, db: AsyncSession):
        result = await db.execute(select(Project).where(Project.team_id == team_id))
        projects = result.scalars().all()
        
        if not projects:
            return []

        return projects


    async def get_project(self, proj_id: UUID, db: AsyncSession):
        result = await db.execute(select(Project).where(Project.id == proj_id))
        project = result.scalar_one_or_none()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        return project


    async def edit_project(self, proj_id: UUID, data: ProjectUpdate, db: AsyncSession):
        result = await db.execute(select(Project).where(Project.id == proj_id))
        project = result.scalar_one_or_none()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        updated_data = normalize_payloads(data.model_dump(exclude_unset=True))
        for field, value in updated_data.items():
            setattr(project, field, value)
            
        await db.commit()
        await db.refresh(project)
        return project


    async def delete_project(self, proj_id: UUID, db: AsyncSession):
        result = await db.execute(select(Project).where(Project.id == proj_id))
        project = result.scalar_one_or_none()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        await db.delete(project)
        await db.commit()
        return {"message": "Project deleted successfully"}

