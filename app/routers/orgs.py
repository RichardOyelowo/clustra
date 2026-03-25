import uuid
from ..database import db_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import OrganizationCreate, OrganizationResponse
from ..schemas import OrganizationMemberCreate, OrganizationMemberResponse


org_router = APIRouter()


@org_router.post("/orgs")
async def create_organization(data: OrganizationCreate, db: AsyncSession = Depends(db_session)) -> OrganizationResponse:
    pass


@org_router.get("/orgs/{org_id}")
async def get_organization(org_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@org_router.patch("/orgs/{org_id}")
async def edit_organization(org_id: uuid.UUID, data: OrganizationCreate, db: AsyncSession = Depends(db_session)):
    pass


@org_router.delete("/orgs/{org_id}")
async def delete_organization(org_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@org_router.post("/orgs/{org_id}/members")
async def add_members(org_id: uuid.UUID, data: OrganizationMemberCreate, db: AsyncSession = Depends(db_session)) -> OrganizationMemberResponse:
    pass


@org_router.get("/orgs/{org_id}/members")
async def get_members(org_id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass


@org_router.delete("/orgs/{org_id}/members/{id}")
async def delete_members(org_id: uuid.UUID, id: uuid.UUID, db: AsyncSession = Depends(db_session)):
    pass
