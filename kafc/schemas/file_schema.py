from pydantic import BaseModel


class FileBase(BaseModel):
	id: int
	file_name: str
	obj_name: str

	class Config:
		orm_mode = True
