from ..utils import check_org_membership, check_team_membership, normalize_payloads
from ..schemas import TeamCreate, TeamUpdate, TeamMemberCreate
from ..utils import TEAM_LEAD_ROLES, TEAM_VIEW_ROLES
from ..utils import ORG_ADMIN_ROLES, ORG_ANY_ROLES
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Team, TeamMember
from fastapi import HTTPException
from sqlalchemy import select
from uuid import UUID

class TeamService:
    """
    Service class for team routes operations
    """
    async def create_team(self, org_id: UUID, data: TeamCreate, current_user: UUID, db: AsyncSession):
        # must belong in an organization to be in or create teams
        await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        result = await db.execute(
            select(Team).where(Team.name == data.name,Team.org_id == org_id)
        )

        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=409, detail="Team already exists")

        data_dict = normalize_payloads(data.model_dump())
        data_dict["created_by"] = current_user
        team = Team(**data_dict)

        db.add(team)
        await db.commit()
        await db.refresh(team)

        return team

    
    async def get_teams(self, org_id: UUID, current_user: UUID, db: AsyncSession):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)
        teams = []

        if org_member.role not in ORG_ADMIN_ROLES:
            # gets all teams in organization
            result = await db.execute(
                select(Team).where(Team.org_id == org_id)
            )
            teams = result.scalars().all()
        else:
            # gets teams with membership only
            result = await db.execute(
                select(Team)
                .join(TeamMember, TeamMember.team_id == Team.id)
                .where(Team.org_id == org_id, TeamMember.user_id == current_user)
            )
            teams = result.scalars().all()

        return teams

 
    async def get_team(self, org_id: UUID, team_id: UUID, current_user: UUID, db: AsyncSession):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(select(Team).where(Team.id == team_id, Team.org_id == org_id))
        team = result.scalar_one_or_none()
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
        return team


    async def edit_team(self, org_id: UUID, team_id: UUID, data: TeamUpdate, current_user: UUID, db: AsyncSession):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(select(Team).where(Team.id == team_id))
        team = result.scalar_one_or_none()
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
        updated_data = normalize_payloads(data.model_dump(exclude_unset=True))
        for field, value in updated_data.items():
            setattr(team, field, value)
            
        await db.commit()
        await db.refresh(team)

        return team

    async def delete_team(self, org_id: UUID, team_id: UUID, current_user: UUID, db: AsyncSession):
        await check_org_membership(org_id, current_user, ORG_ADMIN_ROLES, db)

        result = await db.execute(select(Team).where(Team.id == team_id))
        team = result.scalar_one_or_none()
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
        await db.delete(team)
        await db.commit()
        return {"message": "Team deleted successfully"}


    async def add_member(self, org_id: UUID, team_id: UUID, data: TeamMemberCreate, current_user: UUID, db: AsyncSession):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        team_result = await db.execute(select(Team).where(Team.id == team_id))
        team = team_result.scalar_one_or_none()
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
        # Check if member already exists
        member_result = await db.execute(
            select(TeamMember).where(
                TeamMember.team_id == team_id,
                TeamMember.user_id == data.user_id
            )
        )
        existing_member = member_result.scalar_one_or_none()
        
        if existing_member:
            raise HTTPException(status_code=409, detail="Member already exists in team")
            
        member_data = normalize_payloads(data.model_dump())
        member = TeamMember(**member_data, team_id=team_id)
        
        db.add(member)
        await db.commit()
        await db.refresh(member)

        return member


    async def get_members(self, org_id: UUID, team_id: UUID, current_user: UUID, db: AsyncSession):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(select(TeamMember).where(TeamMember.team_id == team_id))
        members = result.scalars().all()
        
        return members


    async def get_member(self, org_id: UUID, team_id: UUID, member_id: UUID, current_user: UUID, db: AsyncSession):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)

        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_VIEW_ROLES, db)

        result = await db.execute(
            select(TeamMember).where(
                TeamMember.team_id == team_id,
                TeamMember.id == member_id 
            )
        )
        member = result.scalar_one_or_none()
        
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
            
        return member


    async def remove_member(self, org_id: UUID, team_id: UUID, member_id: UUID, current_user: UUID, db: AsyncSession):
        org_member = await check_org_membership(org_id, current_user, ORG_ANY_ROLES, db)
        
        if org_member.role not in ORG_ADMIN_ROLES:
            await check_team_membership(team_id, current_user, TEAM_LEAD_ROLES, db)

        result = await db.execute(
            select(TeamMember).where(
                TeamMember.team_id == team_id,
                TeamMember.id == member_id
            )
        )
        member = result.scalar_one_or_none()
        
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
            
        await db.delete(member)
        await db.commit()
        return {"message": "Member removed successfully"}

