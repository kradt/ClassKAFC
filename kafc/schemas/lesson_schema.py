from pydantic import BaseModel


class LessonBase(BaseModel):
	name: str

	class Config:
		orm_mode = True


class LessonList(BaseModel):
	lesson: LessonBase

	class Config:
		orm_mode = True
