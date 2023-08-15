from kafc import create_app

# File for running celery worker

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

# celery --app make_celery:celery_app worker --loglevel=infos