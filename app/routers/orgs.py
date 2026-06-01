from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import validate_user
from fastapi import APIRouter, Depends
from ..services import OrgService
from ..database import db_session
from typing import List
from uuid import UUID
from ..schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    OrganizationMemberCreate,
    OrganizationMemberResponse,
) 

org_router = APIRouter(prefix="/org")
org_service = OrgService()


@org_router.post("", response_model=OrganizationResponse)
async def create_organization(
    data: OrganizationCreate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await org_service.create_org(current_user.id, data, db)


@org_router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: UUID, 
    current_user=Depends(validate_user), 
    db: AsyncSession = Depends(db_session)
):
    return await org_service.get_org(org_id, current_user.id, db)


@org_router.patch("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: UUID,
    data: OrganizationUpdate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session)
):
    return await org_service.update_org(org_id, current_user.id, data, db)


@org_router.delete("/{org_id}")
async def delete_organization(
    org_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session)
):
    return await org_service.delete_org(org_id, current_user.id, db)


@org_router.post("/{org_id}/members", response_model=OrganizationMemberResponse)
async def add_member(
    org_id: UUID,
    data: OrganizationMemberCreate,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session),
):
    return await org_service.add_member(org_id, current_user.id, data, db)


@org_router.get("/{org_id}/members", response_model=List[OrganizationMemberResponse])
async def get_members(
    org_id: UUID, 
    current_user=Depends(validate_user), 
    db: AsyncSession = Depends(db_session)
):
    return await org_service.get_members(org_id, current_user.id, db)

@org_router.get("/{org_id}/members/{member_id}", response_model=OrganizationMemberResponse)
async def get_member(
    org_id: UUID,
    member_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session)
):
    return await org_service.get_member(org_id, member_id, current_user.id, db)


@org_router.delete("/{org_id}/members/{member_id}")
async def remove_member(
    org_id: UUID, 
    member_id: UUID,
    current_user=Depends(validate_user),
    db: AsyncSession = Depends(db_session)
):
    return await org_service.remove_member(org_id, member_id, current_user.id, db)
