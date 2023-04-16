from telebot import TeleBot

from . import config
from .tools import get_text


bot = TeleBot(config.BOT_TOKEN, parse_mode="Markdown")
bot_text = get_text()
