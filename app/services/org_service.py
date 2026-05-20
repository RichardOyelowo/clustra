from ..models import Organization, OrganizationMember, OrganizationMemberRole
from ..utils.normalization import normalize_payloads
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from uuid import UUID
from ..schemas import (
    OrganizationCreate,
    OrganizationMemberCreate,
    OrganizationUpdate,
)


class OrgService:
    """
    service class for organization routes operations
    """
    # --- roles ---
    ORG_VIEW_ROLES = {
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

    # validates user authorization
    async def _get_member_role(
            self,
            org_id: UUID, 
            current_user: UUID,
            allowed_roles: set[OrganizationMemberRole],
            db: AsyncSession
    ):
        """
        verifies the authorization of the user
        """
        result = await db.execute(select(OrganizationMember).where(
                OrganizationMember.user_id == current_user,
                OrganizationMember.org_id == org_id
            )
        )

        member = result.scalar_one_or_none()

        if not member:
            raise HTTPException(status_code=403, detail="You are not a member of this Organization")
        
        if member.role not in allowed_role:
            raise HTTPException(status_code=403, detail="You don't have permission to perform this action")

        return member


    async def create_org(
            self, 
            current_user: UUID,  
            data: OrganizationCreate, 
            db: AsyncSession
    ):
        result = await db.execute(
            select(Organization).where(Organization.slug == data.slug)
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="Organization already exists")

        data_dict = data.model_dump()
        data_dict["owner_id"] = current_user
        data_dict = normalize_payloads(data_dict)
        org = Organization(**data_dict)

        db.add(org)
        await db.flush()

        # adds owner to the member
        owner = OrganizationMember(
            org_id = org.id,
            user_id =  current_user,
            role = OrganizationMemberRole.OWNER
        )
        db.add(owner)

        await db.commit()
        await db.refresh(org)

        return org

    async def get_org(
            self, 
            org_id: UUID, 
            current_user: UUID, 
            db: AsyncSession
    ):
        await self._get_member_role(org_id, current_user, self.ORG_VIEW_ROLES, db)

        result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = result.scalar_one_or_none()

        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        return org


    async def update_org(
            self, 
            org_id: UUID, 
            current_user: UUID, 
            data: OrganizationUpdate, 
            db: AsyncSession
    ):
        await self._get_member_role(org_id, current_user, self.ORG_ADMIN_ROLES, db)

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


    async def delete_org(
            self, 
            org_id: UUID, 
            current_user: UUID, 
            db: AsyncSession
    ):
        await self._get_member_role(org_id, current_user, self.ORG_OWNER_ROLES, db)

        result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = result.scalar_one_or_none()

        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        await db.delete(org)
        await db.commit()
        return {"message": "Organization deleted successfully"}


    async def add_member(
            self, 
            org_id: UUID,
            current_user: UUID,
            data: OrganizationMemberCreate, 
            db: AsyncSession
    ):
        await self._get_member_role(org_id, current_user, self.ORG_ADMIN_ROLES, db)
        
        org_result = await db.execute(
            select(Organization).where(Organization.id == org_id)
        )
        org = org_result.scalar_one_or_none()

        if not org:
                raise HTTPException(status_code=404, detail="Organization not found")

        # Check if member already exists
        member_result = await db.execute(
            select(OrganizationMember).where(
                OrganizationMember.org_id == org_id,
                OrganizationMember.user_id == data.user_id,
            )
        )
        existing_member = member_result.scalar_one_or_none()

        if existing_member:
            raise HTTPException(
                status_code=409, detail="Member already exists in organization"
            )

        # Create new member
        member_data = normalize_payloads(data.model_dump())
        member = OrganizationMember(**member_data, org_id=org_id)

        db.add(member)
        await db.commit()
        await db.refresh(member)
        return member


    async def get_members(
            self, 
            org_id: UUID,
            current_user: UUID,    
            db: AsyncSession
    ):
        await self._get_member_role(org_id, current_user, self.ORG_VIEW_ROLES, db)

        result = await db.execute(
            select(OrganizationMember).where(OrganizationMember.org_id == org_id)
        )
        members = result.scalars().all()

        if not members:
            return []

        return members


    async def get_member(
            self, 
            org_id: UUID, 
            member_id: UUID, 
            current_user: UUID,
            db: AsyncSession
    ):
        await self._get_member_role(org_id, current_user, self.ORG_VIEW_ROLES, db)

        result = await db.execute(
            select(OrganizationMember).where(
                OrganizationMember.org_id == org_id, OrganizationMember.id == member_id
            )
        )
        member = result.scalar_one_or_none()

        return member


    async def remove_member(
            self, 
            org_id: UUID, 
            member_id: UUID,
            current_user: UUID,
            db: AsyncSession
    ):
        await self._get_member_role(org_id, current_user, self.ORG_ADMIN_ROLES, db)

        result = await db.execute(
            select(OrganizationMember).where(
                OrganizationMember.org_id == org_id, OrganizationMember.id == member_id
            )
        )
        member = result.scalar_one_or_none()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        await db.delete(member)
        await db.commit()
        return {"message": "Member removed successfully"}
