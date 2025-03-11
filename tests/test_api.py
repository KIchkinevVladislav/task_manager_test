import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.taskdao import TaskDAO
from db.models import Base, Status
from db.session import get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


class TestTaskAPI:

    @pytest.mark.asyncio
    async def test_create_task(self):
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        task_data = {"title": "Test Task", "status": Status.PENDING.value}

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            response = await ac.post("tasks/create", json=task_data)

            assert response.status_code == 201

            response = await ac.get("tasks/")

            assert response.json()[0].get("id") == 1

    @pytest.mark.asyncio
    async def test_get_tasks(self):
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        async for session in override_get_db():
            task_dao = TaskDAO(db=session)
            await task_dao.create_task(title="First task", status=Status.PENDING)
            await task_dao.create_task(title="Second task", status=Status.PENDING)
            await session.commit()
        
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            response = await ac.get("tasks/")

            assert len(response.json())
            assert response.json()[1].get('title') == "Second task"
            

    @pytest.mark.asyncio
    async def test_update_tasks(self):
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        async for session in override_get_db():
            task_dao = TaskDAO(db=session)
            await task_dao.create_task(title="First task", status=Status.PENDING)
            await session.commit()
        
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            task_data = {"status": Status.DONE.value}
            response = await ac.patch("tasks/update_status/1", json=task_data)

            response = await ac.get("tasks/")

            assert response.status_code == 200
            assert response.json()[0].get("status") == "done"
