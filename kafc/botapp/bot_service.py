import telebot
from sqlalchemy.orm import Session
from kafc.database import models


# Function for get all lessons from base
def get_all_lessons(db: Session) -> list[models.Lesson]:
	lessons = db.query(models.Lesson).all()
	return lessons


# Function for get all tasks who have particular lesson
def get_tasks_from_lesson(db: Session, id: str) -> list[models.Task]:
	tasks = db.query(models.Task).join(models.Lesson).filter_by(id=id).all()
	return tasks


# Function for get task for task_id
def get_task(db: Session, id: str) -> models.Task:
	task = db.query(models.Task).filter_by(id=id).first()
	return task


# Function for add user who sent /start to bot
def add_new_user(db: Session, user_id: str, username: str) -> models.BotUser:
	user = db.query(models.BotUser).filter_by(user_id=str(user_id)).first()
	if not user:
		user = models.BotUser(user_id=user_id, username=username)
		db.add(user)
		db.commit()
	return user


# Function for get all user who using bot
def get_all_users(db: Session) -> list[str]:
	users = [i.user_id for i in db.query(models.BotUser).all()]
	return users


# Function for add file_id for already existing file
def file_add_file_id(db: Session, filename: str, fileid: str) -> None:
	file = db.query(models.File).filter_by(obj_name=filename).first()
	file.fileid = fileid
	db.add(file)
	db.commit()


# Function for send file by chat_id
# If file sending firstly, file_id added to base
def send_file(
		db: Session,
		bot: telebot.TeleBot,
		chat_id: str,
		task: models.Task,
		caption: str,
		keyboard: telebot.types.InlineKeyboardMarkup | None = None) -> None:
	# select file_id from task file
	file = task.file.fileid
	# if file_id is None download file from aws: s3 
	if not file:
		file = task.file.download_file()
		file.name = task.file.file_name

	f = bot.send_document(chat_id, document=file, caption=caption, reply_markup=keyboard)
	document_id = f.document.file_id
	# if file_id sent file not equal file_id in base add file_id to file column in base
	if file != document_id:
		file_add_file_id(db, task.file.obj_name, document_id)
