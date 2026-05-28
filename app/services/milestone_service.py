from ..utils import check_org_membership, check_team_membership
from ..schemas import MilestoneCreate, MilestoneUpdate
from ..utils import TEAM_LEAD_ROLES, TEAM_VIEW_ROLES
from ..utils import ORG_ADMIN_ROLES, ORG_ANY_ROLES
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import normalize_payloads
from fastapi import HTTPException
from ..models import Milestone
from sqlalchemy import select
from uuid import UUID


class MilestoneService:
    """
    service class for milestone route related operations
    """

    async def create_milestone(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        data: MilestoneCreate,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(
            select(Milestone).where(
                Milestone.title == data.title,
                Milestone.proj_id == proj_id,
                Milestone.team_id == team_id,
                Milestone.org_id == org_id,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="Milestone already exists")

        data_dict = data.model_dump(exclude_unset=True)
        data_dict["proj_id"] = proj_id
        data_dict["team_id"] = team_id
        data_dict["org_id"] = org_id
        milestone = Milestone(**normalize_payloads(data_dict))

        db.add(milestone)
        await db.commit()
        await db.refresh(milestone)

        return milestone

    async def get_milestones(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(
            select(Milestone).where(
                Milestone.proj_id == proj_id,
                Milestone.team_id == team_id,
                Milestone.org_id == org_id,
            )
        )
        milestones = result.scalars().all()

        return milestones

    async def get_milestone(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        milestone_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(
            select(Milestone).where(
                Milestone.id == milestone_id,
                Milestone.proj_id == proj_id,
                Milestone.team_id == team_id,
                Milestone.org_id == org_id,
            )
        )
        milestone = result.scalar_one_or_none()

        if not milestone:
            raise HTTPException(status_code=404, detail="Milestone doesn't exist")

        return milestone

    async def update_milestone(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        milestone_id: UUID,
        data: MilestoneUpdate,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(
            select(Milestone).where(
                Milestone.id == milestone_id,
                Milestone.proj_id == proj_id,
                Milestone.team_id == team_id,
                Milestone.org_id == org_id,
            )
        )
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

    async def delete_milestone(
        self,
        org_id: UUID,
        team_id: UUID,
        proj_id: UUID,
        milestone_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(
            select(Milestone).where(
                Milestone.id == milestone_id,
                Milestone.proj_id == proj_id,
                Milestone.team_id == team_id,
                Milestone.org_id == org_id,
            )
        )
        milestone = result.scalar_one_or_none()

        if not milestone:
            raise HTTPException(status_code=404, detail="Milestone doesn't exist")

        await db.delete(milestone)
        await db.commit()

        return {"message": "Milestone deleted successfully"}
