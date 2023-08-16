from celery import shared_task

from kafc.schemas.task_schema import TaskCreate
from kafc.schemas.lesson_schema import LessonBase
from kafc.database import db, models
from kafc.botapp import bot_service, bot, bot_text
from kafc.cabinet import cabinet_service


@shared_task
def save_task_to_base_and_send_to_students(
		title: str, description: str, group: str,
		lesson: str, user_uuid: str, 
		file: bytes, filename: str):
	"""
	Function for send message to all users. Function can send documents and simple text
	"""
	lesson = LessonBase(name=lesson)
	validate_task = TaskCreate(title=title, description=description,
							   group=group, lesson=lesson)

	task = cabinet_service.create_task(db.session, validate_task, user_uuid, file, filename)
	if not task:
		return 
	for i in bot_service.get_all_users(db.session):
		try:
			bot.send_message(i, bot_text["new_task"].format(task.author.name, task.lesson.name))
			text = bot_text["task_instance"].format(task.lesson.name, task.title, task.description, task.date_publish)
			if task.file:
				bot_service.send_file(db.session, bot, chat_id=i, task=task, caption=text)
			else:
				bot.send_message(i, text)
		# If user block bot
		except Exception as e:
			print(e)
			continue
