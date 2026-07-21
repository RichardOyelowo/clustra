from ..schemas import UserPublicResponse, UserResponse, UserUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import validate_user
from ..services import UserService
from ..database import db_session
from uuid import UUID

user_router = APIRouter(prefix="/user")
user_service = UserService()


@user_router.get("/me", response_model=UserResponse)
async def get_user(current_user = Depends(validate_user)):
    return current_user


@user_router.get("/{id}", response_model=UserPublicResponse)
async def get_user_info(id: UUID, db: AsyncSession = Depends(db_session), current_user=Depends(validate_user)):
    return await user_service.get_user(id, db)


@user_router.patch("/{id}", response_model=UserResponse)
async def update_user(id: UUID, data: UserUpdate, db: AsyncSession = Depends(db_session), current_user=Depends(validate_user)):
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return await user_service.edit_user(id, data, db)


@user_router.delete("/{id}")
async def delete_user(id: UUID, db: AsyncSession = Depends(db_session), current_user=Depends(validate_user)):
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return await user_service.delete_user(id, db)
