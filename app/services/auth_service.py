from gatevault import OAuthHandler, hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..schemas import UserCreate
from sqlalchemy import select
from ..extensions import tm
from ..models import User


async def register(user: UserCreate, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.email.lower() == user.email.lower()))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=409, detail="Email already associated with an account")

    new_user = User(
        email= user.email,
        username= user.username,
        hashed_password= hash_password(user.plain_password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def login(email: str, password: str, db: AsyncSession) -> User:

    async def get_user(email: str):
        result = await db.execute(select(User).where(User.email.lower() == email.lower()))
        return result.scalar_one_or_none()

    oauth = OAuthHandler(token_manger = tm, get_user = get_user)
    tokens = oauth.async_login(email, password)

    return tokens
