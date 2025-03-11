import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from db.models import Base, Status
from db.session import get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest.mark.asyncio
async def test_one_test_for_all_endpoint():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:

        fail_task_data = {"title": 123, "status": Status.PENDING.value}
        response = await ac.post("tasks/create", json=fail_task_data)
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

        task_data = {"title": "Test Task", "status": Status.PENDING.value}
        response = await ac.post("tasks/create", json=task_data)
        assert response.status_code == 201

        response = await ac.get("tasks/")
        assert len(response.json()) == 1
        assert response.json()[0].get("title") == "Test Task"

        fail_update_data = {"status": "in_progress"}
        response = await ac.patch("tasks/update_status/1", json=fail_update_data)
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Input should be 'pending' or 'done'"

        update_data = {"status": Status.DONE.value}
        response = await ac.patch("tasks/update_status/10", json=update_data)
        assert response.status_code == 404

        response = await ac.patch("tasks/update_status/1", json=update_data)
        assert response.status_code == 200

        response = await ac.get("tasks/")
        assert response.status_code == 200
        assert response.json()[0].get("status") == "done"

        task_data_2 = {"title": "Two Test Task", "status": Status.PENDING.value}
        response = await ac.post("tasks/create", json=task_data_2)
        assert response.status_code == 201

        response = await ac.get("tasks/?status=pending")
        assert response.status_code == 200
        assert len(response.json()) == 1

        response = await ac.get("/tasks/?page=1&size=1")
        assert response.status_code == 200
        assert len(response.json()) == 1
