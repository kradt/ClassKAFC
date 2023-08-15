import telebot
from flask import request, Blueprint, current_app as app

from kafc.botapp.view import bot


bot_bp = Blueprint(name="bot_bp", import_name=__name__)


@bot_bp.route(app.config["WEBHOOK_URL_PATH"], methods=["POST"])
def get_update():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200
