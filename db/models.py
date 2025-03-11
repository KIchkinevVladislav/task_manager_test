from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, Integer, String

from .base import Base


class Status(PyEnum):
    PENDING = "pending"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.PENDING)
