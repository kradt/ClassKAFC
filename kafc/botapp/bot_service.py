import telebot
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import bot, bot_text
from ..database import models
from ..schemas.lesson_schema import LessonList


# Fuction for get all lessons from base
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


# Fucntion for add file_id for already existing file
def file_add_file_id(db: Session, filename: str, fileid: str) -> None:
	file = db.query(models.File).filter_by(obj_name=filename).first()
	file.fileid = fileid
	db.add(file)
	db.commit()


# Function for add user who sent /start to bot
def add_new_user(db: Session, user_id: str, username: str) -> None:
	user = models.BotUser(user_id=user_id, username=username)
	try:
		db.add(user)
		db.commit()
	# If user already in Base
	except IntegrityError:
		db.rollback()
		return 


# Function for get all user who using bot
def get_all_users(db: Session) -> list[str]:
	users = [i.user_id for i in db.query(models.BotUser).all()]
	return users


# Function for send file by chat_id
# If file sending firstly, file_id added to base
def send_file(db: Session,
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
	# if file_id sent file not equel file_id in base add file_id to file column in base
	if file != document_id:
		file_add_file_id(db, task.file.obj_name, document_id)


# Function for send message to all users. Function can send documents and simple text
def send_task_to_all(db: Session, bot: telebot.TeleBot, task: models.Task) -> None:
	for i in get_all_users(db):
		try:
			bot.send_message(i, bot_text["new_task"].format(task.author.name, task.lesson.name))
			text = bot_text["task_instance"].format(task.lesson.name, task.title, task.description, task.date_publish)
			if task.file:
				send_file(db, bot, chat_id=i, task=task, caption=text)
			else:
				bot.send_message(i, text)
		# If user block bot
		except Exception:
			continue

