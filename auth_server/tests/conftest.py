"""Configurations for pytest"""

import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient

import pytest

from core.models.helper import pg_db_helper
from core.models import Base
from app import app

from sqlalchemy import String, LargeBinary, sql
from sqlalchemy.orm import Mapped, mapped_column

class TestUser(Base):
    __tablename__ = "test_user"
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(server_default=sql.true())
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary())


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with pg_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with pg_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, tables=[TestUser.__table__])

# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

