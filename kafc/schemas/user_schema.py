from pydantic import BaseModel

from .lesson_schema import LessonBase
from .task_schema import Task


# Base user schema
class UserBase(BaseModel):
	username: str


# Schema for creating new user
class UserCreate(UserBase):
	password: str


# Generally user schema
class User(UserBase):
	id: int
	name: str | None
	role: str | None
	uuid: str
	lessons: list[LessonBase]
	tasks: list[Task]

	class Config:
		orm_mode = True
