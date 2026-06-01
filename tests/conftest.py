import pytest_asyncio
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database import db_session
from app.models.base import Base
from app.config import settings
from app.main import app


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        settings.test_database_url, 
        poolclass=NullPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def client(engine):
    test_session = async_sessionmaker(engine, expire_on_commit=False)

    async def override_db_session():
        async with test_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[db_session] = override_db_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as c:
        yield c

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/signup", json={
        "email": "testuser@clustra.com",
        "username": "testuser",
        "plain_password": "testpass123"
    })
    response = await client.post("/login", data={
        "username": "testuser@clustra.com",
        "password": "testpass123"
    })

    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
