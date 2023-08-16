from sqlalchemy.orm import Session

from kafc.database import models
from kafc.schemas.user_schema import UserCreate


# function returning user by uuid
def get_user(db: Session, uuid: str) -> models.User:
	return db.query(models.User).filter_by(uuid=uuid).first()
	

# function returning user by username
def get_user_by_username(db: Session, username: str) -> models.User:
	return db.query(models.User).filter_by(username=username).first()


# function create new user by schema
def create_user(db: Session, user: UserCreate) -> models.User | None:
	db_user = models.User(username=user.username, password=user.password)
	db.add(db_user)	
	db.commit()
	return db_user
