from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import UserResponse, UserUpdate
from ..dependencies import validate_user
from fastapi import APIRouter, Depends
from ..services import UserService
from ..database import db_session
import uuid

user_router = APIRouter(prefix="/user")
user_service = UserService()


@user_router.get("/me")
async def get_user(current_user = Depends(validate_user)) -> UserResponse:
    return current_user


@user_router.patch("/{id}")
async def edit_user(id: uuid.UUID, data: UserUpdate, db: AsyncSession = Depends(db_session), current_user=Depends(validate_user)):
    return await user_service.edit_user(id, data, db)


@user_router.delete("/{id}")
async def delete_user(id: uuid.UUID, db: AsyncSession = Depends(db_session), current_user=Depends(validate_user)):
    return await user_service.delete_user(id, db)
