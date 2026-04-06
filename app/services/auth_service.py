from ..schemas import UserCreate, UserResponse
from fastapi import HTTPException
from sqlalchemy import select
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
    result = await db.execute(select(User).where(User.email.lower() == email.lower()))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email & Password doesn't match")
    
    return user
