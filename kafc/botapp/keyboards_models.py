from telebot.types import InlineKeyboardMarkup
from keyboa import Keyboa

from kafc.database import models
from kafc.botapp import bot_text
from kafc.botapp.tools import create_inlineKeyboard


# Keyboard for start relation with bot
def keyboard_for_start() -> object:
	data = bot_text["welcome_reply"]
	keyboard = create_inlineKeyboard(data, 2)
	return keyboard


def keyboard_for_contact() -> InlineKeyboardMarkup:
	data = bot_text["contacts"]
	keyboard = create_inlineKeyboard(data, 1, "url")
	result = Keyboa.combine(keyboards=(keyboard, keyboard_for_back_to_start()))
	return result


# Keyboard for back to start handler
def keyboard_for_back_to_start() -> InlineKeyboardMarkup:
	data = {bot_text["text_for_back"]: bot_text["back_reply"]}
	keyboard = create_inlineKeyboard(data)
	return keyboard


# keyboard for choice lesson
def keyboard_for_lessons(lessons: list[models.Lesson]) -> InlineKeyboardMarkup:
	data = {i.name: f"lesson {str(i.id)}" for i in lessons}
	keyboard = create_inlineKeyboard(data, 2)
	result = Keyboa.combine(keyboards=(keyboard, keyboard_for_back_to_start()))
	return result
	

# Keyboard for back to choice lesson
def keyboard_for_back_to_lessons() -> InlineKeyboardMarkup:
	data = {bot_text["text_for_back"]: bot_text["back_to_lesson"]}
	keyboard = create_inlineKeyboard(data, 1)
	return keyboard


# Keyboard for choice task
def keyboard_for_tasks(tasks: list[models.Task]) -> InlineKeyboardMarkup:
	data = {i.title: f"task {str(i.id)}" for i in tasks}
	keyboard = create_inlineKeyboard(data, 2)
	result = Keyboa.combine(keyboards=(keyboard, keyboard_for_back_to_lessons()))
	return result


# Keyboard for back to choice tasks
def keyboard_for_back_to_tasks(id: str) -> InlineKeyboardMarkup:
	data = {bot_text["text_for_back"]: bot_text["back_to_tasks"].format(id)}
	keyboard = create_inlineKeyboard(data, 1)
	return keyboard
