from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import UserCreate, UserResponse
from fastapi import APIRouter, Depends, Response, Request, HTTPException
from ..dependencies import get_oauth
from ..services import AuthService
from gatevault import OAuthHandler
from ..database import db_session
from typing import Annotated

auth_router = APIRouter()
auth_service = AuthService()

REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # matches refresh_expiry_days


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_COOKIE_MAX_AGE,
        path="/",
    )


@auth_router.post("/signup", response_model=UserResponse)
async def create_account(data: UserCreate, db: AsyncSession = Depends(db_session)):
    user = await auth_service.register(data, db)
    return user


@auth_router.post("/login")
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    oauth: OAuthHandler = Depends(get_oauth),
):
    tokens = await auth_service.login(form_data.username, form_data.password, oauth)
    _set_refresh_cookie(response, tokens["refresh_token"])
    return {"access_token": tokens["access_token"], "token_type": tokens["token_type"]}


@auth_router.post("/refresh")
async def refresh(
    response: Response,
    request: Request,
    oauth: OAuthHandler = Depends(get_oauth),
):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    tokens = await auth_service.refresh(refresh_token, oauth)
    _set_refresh_cookie(response, tokens["refresh_token"])
    return {"access_token": tokens["access_token"], "token_type": tokens["token_type"]}


@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/auth")
    return {"detail": "Logged out"}
