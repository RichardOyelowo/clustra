from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


async_engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(async_engine)


async def db_session():
    async with async_session() as session:

        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
