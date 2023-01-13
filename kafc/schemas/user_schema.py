from pydantic import BaseModel, validator

from .lesson_schema import LessonBase
from .task_schema import Task, TaskCreate


# Base user schema
class UserBase(BaseModel):
	username: str


# Schema for creating new user
class UserCreate(UserBase):
	password: str


# Generaly user schema
class User(UserBase):
	id:int
	name: str | None
	role: str | None
	uuid:str
	lessons: list[LessonBase]
	tasks: list[Task]

	class Config:
		orm_mode = True




