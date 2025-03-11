from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db

from .shemas import TaskCreate, TaskResponse, UpdateStatus
from .task_dao import TaskDAO

task_router = APIRouter()


@task_router.post("/create")
async def create_task(task: TaskCreate, response: Response, db: AsyncSession=Depends(get_db)):

    await TaskDAO(db=db).create_task(**task.model_dump())

    response.status_code = status.HTTP_201_CREATED


@task_router.get("/", response_model=list[TaskResponse])
async def get_all_tasks(db: AsyncSession=Depends(get_db)):
    
    tasks = await TaskDAO(db=db).get_all_task_from_db()
    return tasks


@task_router.patch("/update_status/{task_id}")
async def update_status_task(task_id: int, status: UpdateStatus, db: AsyncSession=Depends(get_db)):
    
    task = await TaskDAO(db=db).update_task_status(task_id, status.status)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
