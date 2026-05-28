from ..utils import ORG_ADMIN_ROLES, ORG_ANY_ROLES, TEAM_VIEW_ROLES
from ..utils import check_org_membership, check_team_membership
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Activity, Project
from fastapi import HTTPException
from sqlalchemy import select
from uuid import UUID


class ActivityService:

    async def get_org_activity(
        self,
        org_id: UUID,
        current_user: UUID,
        db: AsyncSession,
    ):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            raise HTTPException(status_code=403, detail="Only org admins can view org-wide activity")

        result = await db.execute(
            select(Activity)
            .where(Activity.org_id == org_id)
            .order_by(Activity.created_at.desc())
        )
        return result.scalars().all()


    async def get_project_activity(
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

        # verify project exists and belongs to this org/team
        proj_result = await db.execute(
            select(Project).where(
                Project.id == proj_id,
                Project.team_id == team_id,
                Project.org_id == org_id,
            )
        )
        project = proj_result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        result = await db.execute(
            select(Activity)
            .where(
                Activity.org_id == org_id,
                Activity.model_id == proj_id,
            )
            .order_by(Activity.created_at.desc())
        )
        return result.scalars().all()

