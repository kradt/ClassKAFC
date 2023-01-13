import flask_login
from flask import Blueprint, render_template, redirect, flash, url_for
from werkzeug.security import check_password_hash
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from ..database import db
from kafc.models import User
from kafc.schemas.user_schema import UserCreate, User as UserSchema
from .forms import LoginForm, SignUpForm
from . import auth_service


auth_bp = Blueprint(name="auth_bp", template_folder="templates", static_folder="static", import_name=__name__)


# Auth user
@auth_bp.route("/login", methods=["POST", "GET"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		db_user = auth_service.get_user_by_username(db=db.session, username=form.login.data)
		if not db_user:
			flash("Не існує користувача з таким username")
		elif not check_password_hash(db_user.password, form.password.data):
			flash("Не правильний пароль")
		else:
			try:
				validate_user = UserSchema.from_orm(db_user)
			except ValidationError as e:
				flash(e)
			else:
				user = User(**validate_user.dict())
				flask_login.login_user(user, remember=True)
				return redirect(url_for(".first_page"))

	return render_template("login.html", form=form)


# Register user
@auth_bp.route("/sign-up", methods=["POST", "GET"])
def sign_up():
	form = SignUpForm()
	if form.validate_on_submit():
		try:
			validate_user = UserCreate(username=form.login.data, password=form.password.data)
			created_user = auth_service.create_user(db=db.session, user=validate_user)
		except IntegrityError:
			flash("Користувач з таким username уже існує")
		except ValidationError as e:
			flash(e)
		else:
			return redirect(url_for(".login"))

	return render_template("sign_up.html", form=form)


# logout user
@auth_bp.route("/logout")
@flask_login.login_required
def logout_user():
	flask_login.logout_user()
	return redirect(url_for(".login"))


# home page user
@auth_bp.route("/")
@flask_login.login_required
def first_page():
	return redirect(url_for("cab_bp.cabinet_page"))




