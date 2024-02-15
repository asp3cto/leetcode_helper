"""Configurations for pytest"""

import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient

import pytest

from core.models.helper import pg_db_helper
from core.models import Base, User
from core.config import settings
from app import app

from sqlalchemy import NullPool, String, LargeBinary, sql
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

TEST_DB_URL = f"postgresql+asyncpg://auth:{settings.postgres_password}@postgres_test/auth"

engine_test = create_async_engine(TEST_DB_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[pg_db_helper.scoped_session_dependency] = override_get_async_session
User.metadata.bind = engine_test

@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)

# SETUP
# @pytest.fixture(scope="session")
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
