import telebot
from celery import shared_task
from sqlalchemy.orm import Session

from ..database import models



@shared_task
def send_classtask_to_all_students(db: Session, bot: telebot.TeleBot, task: models.Task) -> None:
	"""
	Function for send message to all users. Function can send documents and simple text
	"""
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