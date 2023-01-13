from pydantic import BaseModel, validator

from .lesson_schema import LessonBase
from .file_schema import FileBase


# Schema for create task
class TaskCreate(BaseModel):
	title: str 
	description: str 
	group: int 
	lesson: LessonBase
	

# Generaly Task schema
class Task(TaskCreate):
	id: int
	date_publish: str
	file: FileBase | None

	class Config:
		orm_mode = True