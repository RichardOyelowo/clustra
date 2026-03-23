from typing import Annotated
from ..database import db_session
from fastapi import APIRouter, Depends
from ..schemas import UserCreate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter()


@auth_router.post("/signup")
async def create_account(data: UserCreate, db: AsyncSession = Depends(db_session)) -> UserResponse:
    pass


@auth_router.post("/login/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(db_session)):
    pass
