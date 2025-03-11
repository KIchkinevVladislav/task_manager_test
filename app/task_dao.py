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


    async def get_all_task_from_db(self):
        result = await self.db.execute(select(Task))
        
        return result.scalars().all()
