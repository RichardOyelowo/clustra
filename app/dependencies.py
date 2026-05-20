from gatevault import TokenDecodeError, TokenExpiredError
from gatevault import OAuthHandler, InvalidTokenError 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from .database import db_session
from sqlalchemy import select
from app.models import User
from .extensions import tm

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_oauth(db: AsyncSession = Depends(db_session)) -> OAuthHandler:
    async def get_user(email: str):
        lower_email = email.lower()
        result = await db.execute(select(User).where(User.email == lower_email))
        return result.scalar_one_or_none()
    
    return OAuthHandler(token_manager=tm, get_user=get_user)


async def validate_user(
    token: str = Depends(Oauth2_scheme), db: AsyncSession = Depends(db_session)
):
    try:
        payload = tm.decode_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=401, detail="Invalid token: user_id missing"
            )

    except (TokenExpiredError, TokenDecodeError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=str(e))

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
