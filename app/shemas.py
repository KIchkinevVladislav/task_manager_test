from enum import Enum

from pydantic import BaseModel

from db.models import Status


class TaskCreate(BaseModel):
    title: str
    status: Status = Status.PENDING


class TaskResponse(BaseModel):
    id: int
    title: str
    status: Status

    class Config:
        from_attributes = True


class UpdateStatus(BaseModel):
    status: Status = Status.DONE
