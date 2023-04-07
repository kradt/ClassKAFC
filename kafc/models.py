from flask_login import UserMixin

from kafc import login_manager
from .database import db
from kafc.database import models
from kafc.schemas.user_schema import User as UserSchema


class User(UserMixin):
	def __init__(
			self,
			id: str,
			uuid: str,
			name: str | None,
			username: str,
			role: str | None,
			tasks: list,
			lessons: list) -> None:
		self.id = id
		self.uuid = uuid
		self.name = name
		self.username = username
		self.role = role
		self.tasks = tasks
		self.lessons = [name for lesson in lessons for name in lesson.values()]

	def get_id(self) -> str:
		return self.uuid


@login_manager.user_loader
def load_user(user_id):
	db_user = db.session.query(models.User).filter_by(uuid=user_id).first()
	user = UserSchema.from_orm(db_user)
	if user:
		return User(**user.dict())
	return None
