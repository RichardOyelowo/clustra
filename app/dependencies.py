from gatevault import InvalidTokenError, TokenDecodeError, TokenExpiredError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from .database import db_session
from sqlalchemy import select
from app.models import User
from .extensions import tm


Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def validate_user(token: str = Depends(Oauth2_scheme), db: AsyncSession = Depends(db_session)):
    try:
        payload = tm.decode_token(token)
        user_id = payload.get("user_id")

        if user_id == None:
            raise HTTPException(status_code=401, detail="Invalid token: user_id missing")

    except (TokenExpiredError, TokenDecodeError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=str(e))

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
