from ..utils import normalize_payloads, check_org_membership, check_team_membership
from ..utils import TEAM_LEAD_ROLES, TEAM_VIEW_ROLES
from ..utils import ORG_ADMIN_ROLES, ORG_ANY_ROLES
from ..schemas import ProjectCreate, ProjectUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..models  import Project
from sqlalchemy import select
from uuid import UUID

class ProjectService:
    """
    service class for project routes operations
    """

    async def create_project(
        self,
        org_id: UUID,
        team_id: UUID,
        data: ProjectCreate,
        current_user: UUID,
        db: AsyncSession
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(
            select(Project).where(
                Project.name == data.name, Project.team_id == team_id
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="Project already exists")

        data_dict = data.model_dump()
        data_dict["created_by"] = current_user
        data_dict = normalize_payloads(data_dict)
        project = Project(**data_dict)

        db.add(project)
        await db.commit()
        await db.refresh(project)

        return project


    async def get_projects(
        self, 
        org_id: UUID, 
        team_id: UUID, 
        current_user: UUID, 
        db: AsyncSession
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)
        
        if org_member.role in ORG_ADMIN_ROLES:
            # gets all projects from all teams in the org
            result = await db.execute(
                select(Project).where(Project.org_id == org_id)
            )
            return result.scalars().all()
        else:
            # gets all team's projects for team members
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)
            result = await db.execute(
                select(Project).where(Project.team_id == team_id)
            )
            projects = result.scalars().all()

            return projects


    async def get_project(
        self, 
        org_id: UUID, 
        team_id: UUID, 
        proj_id: UUID,
        current_user: UUID,
        db: AsyncSession
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(select(Project).where(Project.id == proj_id))
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        return project


    async def update_project(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        data: ProjectUpdate,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)
        
        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

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


    async def delete_project(
        self, org_id: UUID, team_id: UUID, proj_id: UUID, current_user, db: AsyncSession
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(select(Project).where(Project.id == proj_id))
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        await db.delete(project)
        await db.commit()
        return {"message": "Project deleted successfully"}
