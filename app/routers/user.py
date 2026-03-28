from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import validate_user
from fastapi import APIRouter, Depends
from ..database import db_session
import uuid

user_router = APIRouter(prefix="/user")


@user_router.get("/me")
async def get_user(current_user = Depends(validate_user)):
    return current_user


@user_router.patch("/{id}")
async def edit_user(id: uuid.UUID, db: AsyncSession = Depends(db_session), current_user = Depends(validate_user)):
    pass


@user_router.delete("/{id}")
async def delete_user(id: uuid.UUID, db: AsyncSession = Depends(db_session), current_user = Depends(validate_user)):
    pass


