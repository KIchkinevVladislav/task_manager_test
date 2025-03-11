from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Status
from db.session import get_db

from .shemas import TaskCreate, TaskResponse, UpdateStatus
from .task_dao import TaskDAO

task_router = APIRouter()


@task_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: AsyncSession=Depends(get_db)):

    await TaskDAO(db=db).create_task(**task.model_dump())


@task_router.get("/", response_model=list[TaskResponse])
async def get_all_tasks(
    status: Optional[Status] = Query(None, description="Фильтр по статусу задачи"),
    page: int=Query(1, ge=1, description="Номер страницы."),
    size: int=Query(10, ge=1, le=20, description="Количество записей на странице"),
    db: AsyncSession = Depends(get_db)
    ):
    tasks = await TaskDAO(db=db).get_all_tasks_from_db(
        status=status, page=page, size=size)
    return tasks


@task_router.patch("/update_status/{task_id}")
async def update_status_task(task_id: int, status: UpdateStatus, db: AsyncSession=Depends(get_db)):
    
    task = await TaskDAO(db=db).update_task_status(task_id, status.status)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
