from ..utils import TEAM_LEAD_ROLES, TEAM_CONTRIBUTION_ROLES, TEAM_VIEW_ROLES
from ..schemas import LabelCreate, LabelUpdate, TaskLabelCreate
from ..utils import check_org_membership, check_team_membership
from ..utils import ORG_ADMIN_ROLES, ORG_ANY_ROLES
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import normalize_payloads
from ..models import Label, TaskLabel
from fastapi import HTTPException
from sqlalchemy import select
from uuid import UUID


class LabelService:
    """
    service class for label route related operations
    """

    # ---------------- Project Label ------------------

    async def create_label(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        data: LabelCreate,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)
        
        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(
            select(Label)
            .where(
                Label.name == data.name,
                Label.proj_id == proj_id, 
                Label.team_id == team_id,
                Label.org_id == org_id
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="Label already exists")
        
        data_dict = data.model_dump(exclude_unset=True)
        data_dict["proj_id"] = proj_id
        data_dict["team_id"] = team_id
        data_dict["org_id"] = org_id

        label = Label(**normalize_payloads(data_dict))

        db.add(label)
        await db.commit()
        await db.refresh(label)

        return label


    async def get_labels(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)
        await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(
            select(Label)
            .where( 
                Label.proj_id == proj_id,
                Label.team_id == team_id,
                Label.org_id == org_id,
            )
        )

        return result.scalars().all()


    async def get_label(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        label_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)
    
        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(
            select(Label)
            .where(
                Label.id == label_id, 
                Label.proj_id == proj_id, 
                Label.team_id == team_id, 
                Label.org_id == org_id
            )
        )
        label = result.scalar_one_or_none()

        if not label:
            raise HTTPException(status_code=404, detail="Label doesn't exist")

        return label

    async def update_label(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        label_id: UUID,
        data: LabelUpdate,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(
            select(Label)
            .where(
                Label.id == label_id,
                Label.proj_id == proj_id,
                Label.team_id == team_id,
                Label.org_id == org_id
            )
        )
        label = result.scalar_one_or_none()

        if not label:
            raise HTTPException(status_code=404, detail="Label doesn't exists")

        data_dict = data.model_dump(exclude_unset=True)
        if not data_dict:
            return label

        updated_data = normalize_payloads(data_dict)
        for field, value in updated_data.items():
            setattr(label, field, value)

        await db.commit()
        await db.refresh(label)

        return label


    async def delete_label(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        label_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(
            select(Label)
            .where(
                Label.id == label_id, 
                Label.proj_id == proj_id,
                Label.team_id == team_id,
                Label.org_id == org_id
            )
        )
        label = result.scalar_one_or_none()

        if not label:
            raise HTTPException(status_code=404, detail="Label doesn't exists")

        await db.delete(label)
        await db.commit()

        return {"message": "label deleted successfully"}


    # ------------------ Task Label ---------------------

    async def create_task_label(
        self,
        org_id: UUID,
        team_id: UUID,
        data: TaskLabelCreate,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_CONTRIBUTION_ROLES, db)

        result = await db.execute(
            select(TaskLabel).where(
                TaskLabel.label_id == data.label_id,
                TaskLabel.task_id == data.task_id
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=409, detail="Task Label already exists")

        task_label = TaskLabel(
            **normalize_payloads(data.model_dump(exclude_unset=True))
        )

        db.add(task_label)
        await db.commit()
        await db.refresh(task_label)

        return task_label


    async def get_task_labels(
        self,
        org_id: UUID,
        team_id: UUID,
        label_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_CONTRIBUTION_ROLES, db)

        result = await db.execute(
            select(TaskLabel).where(TaskLabel.label_id == label_id))
        
        return result.scalars().all()


    async def get_task_label(
        self,
        org_id: UUID,
        team_id: UUID,
        label_id: UUID,
        task_label_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(
            select(TaskLabel)
            .where(TaskLabel.id == task_label_id, TaskLabel.label_id == label_id)
        )
        task_label = result.scalar_one_or_none()

        if not task_label:
            raise HTTPException(status_code=404, detail="Task Label doesn't exist")

        return task_label


    async def delete_task_label(
        self,
        org_id: UUID,
        team_id: UUID,
        label_id: UUID,
        task_label_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_CONTRIBUTION_ROLES, db)

        result = await db.execute(
            select(TaskLabel).where(TaskLabel.id == task_label_id)
        )
        task_label = result.scalar_one_or_none()
        if not task_label:
            raise HTTPException(status_code=404, detail="Task Label doesn't exist")

        await db.delete(task_label)
        await db.commit()

        return {"message": "Task label deleted successfully"}

