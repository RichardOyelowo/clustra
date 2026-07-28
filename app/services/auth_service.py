from gatevault import InvalidCredentialsError, UnauthorizedError, GuardError
from gatevault import TokenExpiredError, TokenDecodeError, InvalidTokenError
from gatevault import hash_password, OAuthHandler
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..schemas import UserCreate
from sqlalchemy import select
from ..models import User


class AuthService:
    """
        service for handling authentication route services
    """
    async def register(self, user: UserCreate, db: AsyncSession) -> User:
        lower_email = user.email.lower()
        result = await db.execute(select(User).where(User.email == lower_email))
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=409, detail="Email already associated with an account")
        new_user = User(
            email=lower_email,
            full_name=user.full_name,
            password_hash=hash_password(user.plain_password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def login(self, email: str, password: str, oauth: OAuthHandler):
        try:
            tokens = await oauth.async_login(email, password)
        except (InvalidCredentialsError, UnauthorizedError):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        except GuardError:
            raise HTTPException(status_code=400, detail="Login failed")
        return tokens

    async def refresh(self, refresh_token: str, oauth: OAuthHandler):
        try:
            tokens = await oauth.async_refresh(refresh_token)
        except (TokenExpiredError, TokenDecodeError, InvalidTokenError, InvalidCredentialsError):
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        return tokens
