from celery import Celery, Task
from flask import Flask


def celery_init_app(app: Flask):
	class FlaskTask(Task):
		def __call__(self, *args, **kwargs):
			with app.app_context():
				self.run(*args, **kwargs)

	celery_app = Celery(app.name, task_cls=FlaskTask)
	celery_app.config_from_object(app.config["CELERY"])
	celery_app.set_default()
	app.extensions["celery"] = celery_app

	return celery_app
