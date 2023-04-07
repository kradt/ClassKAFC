import telebot
from flask import request, Blueprint

from . import config
from .view import bot


bot_bp = Blueprint(name="bot_bp", import_name=__name__)


@bot_bp.route(config.WEBHOOK_URL_PATH, methods=["POST"])
def getUpdate():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200


@bot_bp.route("/webhook")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH)
	return "!", 200
