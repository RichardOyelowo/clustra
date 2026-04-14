from ..schemas import TeamCreate, TeamResponse, TeamUpdate
from ..schemas import TeamMemberCreate, TeamMemberResponse
from ..models import Team, TeamMember
from ..utils.normalization import normalize_payloads
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from uuid import UUID

class TeamService:
    """
    Service class for team routes operations
    """

    async def create_team(self, data: TeamCreate, current_user: UUID, db: AsyncSession):
        result = await db.execute(select(Team).where(
            Team.name == data.name,
            Team.org_id == data.org_id))
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="Team already exists")

        data_dict = normalize_payloads(data.model_dump())
        data_dict["created_by"] = current_user  # type: ignore
        team = Team(**data_dict)

        db.add(team)
        await db.commit()
        await db.refresh(team)

        return team

    async def get_team(self, team_id: UUID, db: AsyncSession):
        result = await db.execute(select(Team).where(Team.id == team_id))
        team = result.scalar_one_or_none()
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
        return team

    async def edit_team(self, team_id: UUID, data: TeamUpdate, db: AsyncSession):
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

    async def delete_team(self, team_id: UUID, db: AsyncSession):
        result = await db.execute(select(Team).where(Team.id == team_id))
        team = result.scalar_one_or_none()
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
        await db.delete(team)
        await db.commit()
        return {"message": "Team deleted successfully"}

    async def add_member(self, team_id: UUID, data: TeamMemberCreate, db: AsyncSession):
        # First check if team exists
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
            
        # Create new member
        member_data = normalize_payloads(data.model_dump())
        member = TeamMember(**member_data, team_id=team_id)
        
        db.add(member)
        await db.commit()
        await db.refresh(member)
        return member

    async def get_members(self, team_id: UUID, db: AsyncSession):
        result = await db.execute(select(TeamMember).where(TeamMember.team_id == team_id))
        members = result.scalars().all()
        
        if not members:
            return []

        return members

    async def get_member(self, team_id: UUID, member_id: UUID, db: AsyncSession):
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

    async def remove_member(self, team_id: UUID, member_id: UUID, db: AsyncSession):
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
