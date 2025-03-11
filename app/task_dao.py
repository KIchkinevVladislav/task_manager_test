from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Status, Task


class TaskDAO():
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, title: str, status: Status):
        new_task = Task(title=title, status=status)

        self.db.add(new_task)
        await self.db.commit()

    async def update_task_status(self, task_id: int, status: Status):
        task = await self.db.get(Task, task_id)

        if task:
            task.status = status
            await self.db.commit()
            return task


    async def get_all_tasks_from_db(self, 
                                   status: Optional[Status] = None,
                                   page: int = 1,
                                   size: int = 10):
        query = select(Task)

        if status:
            query = query.where(Task.status == status)

        query = query.offset((page - 1) * size).limit(size)

        result = await self.db.execute(query)
        return result.scalars().all()
