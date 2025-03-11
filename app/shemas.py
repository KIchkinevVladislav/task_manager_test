from pydantic import BaseModel, ConfigDict

from db.models import Status


class TaskCreate(BaseModel):
    title: str
    status: Status = Status.PENDING


class TaskResponse(BaseModel):
    id: int
    title: str
    status: Status

    model_config = ConfigDict(from_attributes=True)


class UpdateStatus(BaseModel):
    status: Status = Status.DONE
