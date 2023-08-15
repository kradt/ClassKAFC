from kafc.botapp import bot, bot_text, bot_service, keyboards_models as menu


# Func for unpack chat_id and message_id
def path_edit(call):
	return {"chat_id": call.message.chat.id, "message_id": call.message.message_id}


# Handler for start relation with bot
@bot.message_handler(commands=["start"])
@bot.with_app_context
def start(message):
	bot_service.add_new_user(bot.db, message.from_user.id, message.from_user.username)
	bot.send_sticker(message.chat.id, bot_text["hello_sticker_id"])
	bot.send_message(message.chat.id, bot_text["welcome_message"], reply_markup=menu.keyboard_for_start())


# Handler for get information about bot
@bot.callback_query_handler(func=lambda call: True and str(call.data).split(" ")[0] == "info")
@bot.with_app_context
def info_handler(call):
	bot.edit_message_text(
		**path_edit(call),
		text=bot_text["info_text"].format(bot.app.config["WEBHOOK_HOST"]),
		reply_markup=menu.keyboard_for_contact())


# Handler for back to start keyboard
@bot.callback_query_handler(func=lambda call: True and str(call.data).split(" ")[0] == "back_to_start")
@bot.with_app_context
def back_to_start(call):
	bot.edit_message_text(**path_edit(call), text=bot_text["welcome_message"], reply_markup=menu.keyboard_for_start())


# Handler for start selecting task and get all existing lessons
@bot.callback_query_handler(func=lambda call: True and str(call.data).split(" ")[0] == "my_task" or
													   str(call.data).split(" ")[0] == "back_to_lesson")
@bot.with_app_context
def person_task_handler(call):
	lessons = bot_service.get_all_lessons(bot.db.session)
	if not lessons:
		keyboard = menu.keyboard_for_back_to_start()
		text = bot_text["nobody_task"]
	else:
		keyboard = menu.keyboard_for_lessons(lessons)
		text = bot_text["text_for_get_lessons"]
	try:
		bot.edit_message_text(**path_edit(call), reply_markup=keyboard, text=text)
	except:
		bot.delete_message(**path_edit(call))
		bot.send_message(call.message.chat.id, reply_markup=keyboard, text=text)


# Handler for get all tasks from particular lesson
@bot.callback_query_handler(func=lambda call: True and str(call.data).split(" ")[0] == "lesson" or
													   str(call.data).split(" ")[0] == "back_to_tasks")
@bot.with_app_context
def get_tasks(call):
	lesson_id = str(call.data).split(" ")[1]
	tasks = bot_service.get_tasks_from_lesson(bot.db.session, lesson_id)
	if tasks:
		lesson = tasks[0].lesson
		text = bot_text["text_for_tasks"].format(lesson.name)
		keyboard = menu.keyboard_for_tasks(tasks)
	else:
		text = bot_text["nobody_task_from_lesson"]
		keyboard = menu.keyboard_for_back_to_lessons()

	if call.message.content_type == "document":
		bot.delete_message(**path_edit(call))
		bot.send_message(call.message.chat.id, reply_markup=keyboard, text=text)
	else:
		bot.edit_message_text(**path_edit(call), reply_markup=keyboard, text=text)


# Handler for get all task information
@bot.callback_query_handler(func=lambda call: True and str(call.data).split(" ")[0] == "task")
@bot.with_app_context
def task_handler(call):
	task_id = str(call.data).split(" ")[1]
	task = bot_service.get_task(bot.db.session, task_id)
	if task:
		text = bot_text["task_instance"].format(task.lesson.name, task.title, task.description, task.date_publish)
		keyboard = menu.keyboard_for_back_to_tasks(task.lesson.id)
		if task.file:
			bot.delete_message(**path_edit(call))
			bot_service.send_file(bot.db.session, bot, chat_id=call.message.chat.id, task=task, caption=text, keyboard=keyboard)
	else:
		text = bot_text["welcome_message"]
		keyboard = menu.keyboard_for_start()

	bot.edit_message_text(**path_edit(call), reply_markup=keyboard, text=text)
