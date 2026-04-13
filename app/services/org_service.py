from ..schemas import OrganizationCreate, OrganizationResponse, OrganizationUpdate
from ..schemas import OrganizationMemberCreate, OrganizationMemberResponse
from ..models import Organization, OrganizationMember
from ..utils.normalization import normalize_payloads
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from uuid import UUID

class OrgService:
    """
    service class for organization routes operations
    """

    async def create_org(self, data: OrganizationCreate, db: AsyncSession):
        result = await db.execute(select(Organization).where(Organization.slug == data.slug))
        existing = result.scalar_one_or_none()

        if existing:
            return []

        data_dict = normalize_payloads(data.model_dump())
        org = Organization(**data_dict)

        db.add(org)
        await db.commit()
        await db.refresh(org)

        return org


    async def get_org(self, org_id: UUID, db: AsyncSession):
        result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
            
        return org


    async def edit_org(self, org_id: UUID, data: OrganizationUpdate, db: AsyncSession):
        result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
            
        updated_data = normalize_payloads(data.model_dump(exclude_unset=True))
        for field, value in updated_data.items():
            setattr(org, field, value)
            
        await db.commit()
        await db.refresh(org)
        return org


    async def delete_org(self, org_id: UUID, db: AsyncSession):
        result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
            
        await db.delete(org)
        await db.commit()
        return {"message": "Organization deleted successfully"}


    async def add_member(self, org_id: UUID, data: OrganizationMemberCreate, db: AsyncSession):
        # First check if organization exists
        org_result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
            
        # Check if member already exists
        member_result = await db.execute(
            select(OrganizationMember).where(
                OrganizationMember.org_id == org_id,
                OrganizationMember.user_id == data.user_id
            )
        )
        existing_member = member_result.scalar_one_or_none()
        
        if existing_member:
            raise HTTPException(status_code=409, detail="Member already exists in organization")
            
        # Create new member
        member_data = normalize_payloads(data.model_dump())
        member = OrganizationMember(**member_data, org_id=org_id)
        
        db.add(member)
        await db.commit()
        await db.refresh(member)
        return member


    async def get_members(self, org_id: UUID, db: AsyncSession):
        result = await db.execute(select(OrganizationMember).where(OrganizationMember.org_id == org_id))
        members = result.scalars().all()
        
        if not members:
            raise HTTPException(status_code=404, detail="Organization has no members")
            
        return members



    async def get_member(self, org_id: UUID, member_id: UUID, db: AsyncSession):
        result = await db.execute(
            select(OrganizationMember).where(
                OrganizationMember.org_id == org_id,
                OrganizationMember.id == member_id 
            )
        )
        member = result.scalar_one_or_none()
        
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
            
        return member


    async def remove_member(self, org_id: UUID, member_id: UUID, db: AsyncSession):
        result = await db.execute(
            select(OrganizationMember).where(
                OrganizationMember.org_id == org_id,
                OrganizationMember.id == member_id
            )
        )
        member = result.scalar_one_or_none()
        
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
            
        await db.delete(member)
        await db.commit()
        return {"message": "Member removed successfully"}
