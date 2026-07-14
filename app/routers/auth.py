from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import UserCreate, UserResponse
from fastapi import APIRouter, Depends
from ..dependencies import get_oauth
from ..services import AuthService
from gatevault import OAuthHandler
from ..database import db_session
from typing import Annotated


auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post("/signup", response_model=UserResponse)
async def create_account(data: UserCreate, db: AsyncSession = Depends(db_session)):
    user = await auth_service.register(data, db)
    return user


@auth_router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        oauth: OAuthHandler = Depends(get_oauth)
):
    tokens = await auth_service.login(form_data.username, form_data.password, oauth)
    return tokens
