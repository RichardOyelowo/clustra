from ..utils import TEAM_LEAD_ROLES, TEAM_CONTRIBUTION_ROLES, TEAM_VIEW_ROLES
from ..utils import ORG_ADMIN_ROLES, ORG_ANY_ROLES, normalize_payloads
from ..utils import check_org_membership, check_team_membership
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import TaskCreate, TaskUpdate
from fastapi import HTTPException
from sqlalchemy import select
from ..models import Task
from uuid import UUID


class TaskService:
    """
    service class for task routes operations
    """

    async def create_task(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        data: TaskCreate,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_CONTRIBUTION_ROLES, db)

        result = await db.execute(
            select(Task)
            .where(Task.team_id == team_id, Task.name == data.name, Task.proj_id == proj_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="Task already exists")

        data_dict = data.model_dump(exclude_unset=True)
        data_dict["proj_id"] = proj_id
        data_dict["team_id"] = team_id
        data_dict["org_id"] = org_id
        data_dict["created_by"] = current_user
        data_dict = normalize_payloads(data_dict)
        task = Task(**data_dict)

        db.add(task)
        await db.commit()
        await db.refresh(task)

        return task

    async def get_tasks(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        # non admins must be team members
        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(
            select(Task)
            .where(
                Task.org_id == org_id, Task.team_id == team_id, Task.proj_id == proj_id
            )
        )
        tasks = result.scalars().all()

        if not tasks:
            return []

        return tasks


    async def get_task(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        task_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES,db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(
            select(Task)
            .where(
                Task.org_id == org_id, Task.team_id == team_id, Task.proj_id == proj_id, Task.id == task_id
            )
        )
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task


    async def update_task(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        task_id: UUID,
        data: TaskUpdate,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        # non admin members must be contibutors to edit
        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_CONTRIBUTION_ROLES, db)

        result = await db.execute(
            select(Task)
            .where(
                Task.org_id == org_id ,Task.team_id == team_id, Task.proj_id == proj_id, Task.id == task_id
            )
        )
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        updated_data = normalize_payloads(data.model_dump(exclude_unset=True))
        for field, value in updated_data.items():
            setattr(task, field, value)

        await db.commit()
        await db.refresh(task)
        return task


    async def delete_task(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        task_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)
        
        # only org asdmins or team leads
        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(
            select(Task)
            .where(
                Task.org_id == org_id, Task.team_id == team_id, Task.proj_id == proj_id, Task.id == task_id
            )
        )
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        await db.delete(task)
        await db.commit()
        return {"message": "Task deleted successfully"}
