from functools import wraps
from telebot import TeleBot
from flask import Flask, current_app
from sqlalchemy.orm import Session

from kafc.botapp.tools import get_text


class ContextedBot(TeleBot):
    """
        Клас для патчингу об'єкта Telebot поточним об'єктом Flask
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @property
    def db(self) -> Session:
        """
            Отримуємо базу даних по об'єкту бота
        """
        if self.app is None:
            raise AttributeError("You should init your application")
        
        with self.app.app_context():
            return self.app.extensions["sqlalchemy"].session
        
    def with_app_context(self, func: callable):
        """
            Декоратор який обгортає функцію в контекст flask об'єкту
        """
        if not self.app:
            raise AttributeError("For using decorator `with_app_context you should init it")
        @wraps(func)
        def inner(*args, **kwargs):
            with self.app.app_context():
                return func(*args, **kwargs)
        return inner

    def init_app(self, app: Flask) -> None:
        if not isinstance(app, Flask):
            raise ValueError("You should pass Flask object")
        self.app = app 


bot = ContextedBot(current_app.config["BOT_TOKEN"], parse_mode="Markdown")
bot_text = get_text()
