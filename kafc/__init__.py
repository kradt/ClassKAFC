from flask import Flask, redirect, url_for, request
from flask_login import LoginManager
import telebot

from .utils import ManageFile
from .config import Config


manage_s3 = ManageFile(bucket_name=Config.BUCKET_NAME, 
					   aws_access_key_id=Config.AWS_ACCESS_KEY,
					   aws_secret_access_key=Config.AWS_SECRET_KEY)
login_manager = LoginManager()


def create_app(configurate=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	from .database import db, migrate
	db.init_app(app)
	migrate.init_app(app)
	migrate.db = db

	with app.app_context():
		from .database import models
		db.create_all()

	login_manager.init_app(app)
	login_manager.login_view = "auth_bp.login"

	@app.route("/")
	def index():
		return redirect(url_for("cab_bp.cabinet_page"))
	
	from .botapp.webhook import bot_bp
	from .auth.routes import auth_bp
	from .cabinet.routes import cab_bp
	
	app.register_blueprint(bot_bp, url_prefix="/")
	app.register_blueprint(auth_bp, url_prefix="/auth")
	app.register_blueprint(cab_bp, url_prefix="/me")
	
	return app





