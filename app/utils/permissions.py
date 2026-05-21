from ..models import OrganizationMemberRole, TeamMemberRole
from ..models import OrganizationMember, TeamMember
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from uuid import UUID

# --- Org role sets ---
ORG_ANY_ROLES = {
    OrganizationMemberRole.OWNER,
    OrganizationMemberRole.ADMIN,
    OrganizationMemberRole.MEMBER,
}
ORG_ADMIN_ROLES = {
    OrganizationMemberRole.OWNER,
    OrganizationMemberRole.ADMIN,
}
ORG_OWNER_ROLES = {
    OrganizationMemberRole.OWNER,
}

# --- Team role sets ---
TEAM_VIEW_ROLES = {
    TeamMemberRole.LEAD,
    TeamMemberRole.CONTRIBUTOR,
    TeamMemberRole.VIEWER,
}
TEAM_CONTRIBUTION_ROLE = {
    TeamMemberRole.LEAD,
    TeamMemberRole.CONTRIBUTOR
}
TEAM_LEAD_ROLES = {
    TeamMemberRole.LEAD,
}


async def check_org_membership(
    org_id: UUID,
    current_user: UUID,
    allowed_roles: set[OrganizationMemberRole],
    db: AsyncSession
):
    result = await db.execute(select(OrganizationMember).where(
        OrganizationMember.user_id == current_user,
        OrganizationMember.org_id == org_id
    ))
    org_member = result.scalar_one_or_none()
    if not org_member:
        raise HTTPException(status_code=403, detail="You are not a member of this Organization")
    if org_member.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="You don't have permission to perform this action")
    return org_member


async def check_team_membership(
    team_id: UUID,
    current_user: UUID,
    allowed_roles: set[TeamMemberRole],
    db: AsyncSession
):
    result = await db.execute(select(TeamMember).where(
        TeamMember.user_id == current_user,
        TeamMember.team_id == team_id
    ))
    team_member = result.scalar_one_or_none()
    if not team_member:
        raise HTTPException(status_code=403, detail="You are not a member of this team")
    if team_member.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="You don't have permission to perform this action")
    return team_member
