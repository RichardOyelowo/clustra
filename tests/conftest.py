import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database import db_session
from app.models.base import Base
from app.config import settings
from app.main import app


database_url = settings.test_database_url

test_engine = create_async_engine(database_url)
test_session = async_sessionmaker(test_engine, expire_on_commit=False)

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


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as c:
        yield c


@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/signup", json={
        "email": "testuser@clustra.com",
        "username": "testuser",
        "plain_password": "testpass123"
    })
    response = await client.post("/login/", data={
        "username": "testuser@clustra.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
