from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import UserResponse, UserUpdate
from gatevault import hash_password
from fastapi import HTTPException
from sqlalchemy import select
from ..models import User
from uuid import UUID


class UserService:
    """
        service class for user routes operations
    """

    async def get_user(self, user_id: UUID, db: AsyncSession) -> UserResponse:
        """ retrieve a user by their id """

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user


    async def edit_user(self, user_id: UUID, update_data: UserUpdate, db: AsyncSession) -> UserResponse:
        """ update User details """
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        updated_data =  update_data.model_dump(exclude_unset=True)
        if "password" in updated_data:
            updated_data["password_hash"] = hash_password(updated_data.pop("password"))

        for key, value in updated_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await db.commit()
        await db.refresh(user)

        return user


    async def delete_user(self, user_id: UUID, db: AsyncSession) -> dict:
        """ delete user from database """

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(user)
        await db.commit()

        return {"status": "success"}
