from gatevault import InvalidCredentialsError, UnauthorizedError, GuardError
from gatevault import OAuthHandler, hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..schemas import UserCreate
from sqlalchemy import select
from ..extensions import tm
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
            email= lower_email,
            username= user.username,
            hashed_password= hash_password(user.plain_password)
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user


    async def login(self, email: str, password: str, db: AsyncSession):
        async def get_user(email: str):
            lower_email = email.lower()
            result = await db.execute(select(User).where(User.email == lower_email))
            return result.scalar_one_or_none()

        oauth = OAuthHandler(token_manager = tm, get_user = get_user)
        try:
            tokens = await oauth.async_login(email, password)
        except InvalidCredentialsError:
            raise HTTPException(status_code=404, detail="No account connected with email")
        except UnauthorizedError:
            raise HTTPException(status_code=401, detail="Login info doesn't match")
        except GuardError as e:
            raise HTTPException(status_code=400, detail=f"{e}")

        return tokens
