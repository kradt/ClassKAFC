import flask_login
from flask import Blueprint, render_template, redirect, flash, url_for, request, send_file
from sqlalchemy.exc import DataError

from ..database import db
from kafc.schemas.task_schema import TaskCreate
from kafc.schemas.lesson_schema import LessonBase
from .forms import NameForm, LessonForm, TaskForm
from . import cabinet_service
from ..botapp import bot_service, bot, tasks as bot_tasks

cab_bp = Blueprint(name="cab_bp", template_folder="templates", static_folder="static", import_name=__name__)


# ---- Remove Data Functionality ----

# Handler for remove user task
@cab_bp.route("/remove_task/<int:id>", methods=["GET"])
@flask_login.login_required
def remove_task(id):
    # Check if the task has a file inside it
    file = cabinet_service.get_file_by_task_id(db=db.session, user_uuid=flask_login.current_user.uuid, id=id)
    if file:
        file.drop_file()
    cabinet_service.delete_task_by_id(db=db.session, user_uuid=flask_login.current_user.uuid, id=id)
    return redirect(url_for(".cabinet_page"))


# Handler for remove user lesson
@cab_bp.route("/remove-lesson", methods=["POST"])
@flask_login.login_required
def remove_lesson():
    lesson = request.form["lesson"]
    try:
        cabinet_service.remove_user_lesson(
            db=db.session,
            user_uuid=flask_login.current_user.uuid,
            lesson_name=lesson)
    except ValueError:
        flash("У вас немає такого предмету")
    return redirect(url_for(".cabinet_page"))


# ---- Update Data Functionality ----

# Handler for update user lesson
@cab_bp.route("/update_user", methods=["POST"])
@flask_login.login_required
def update_user():
    lesson = request.form.get("lesson")
    name = request.form.get("name")
    try:
        cabinet_service.update_user(db=db.session, user_uuid=flask_login.current_user.uuid, lesson_name=lesson,
                                    name=name)
    except DataError:
        flash("Схоже, ви ввели завелике значення!")
    return redirect(url_for(".cabinet_page"))


# ---- Task Functionality ----

# Page and Handler for create new task
@cab_bp.route("/send-task", methods=["GET", "POST"])
@flask_login.login_required
def send_task():
    form = TaskForm(lessons=flask_login.current_user.lessons)
    if form.validate_on_submit():
        # If lesson didn't chose it value equal "0"
        lesson = form.lesson.data
        if not lesson or lesson == "0":
            flash("Перед тим як відправляти завдання, добавте свій предмет в особистому кабінеті")
        else:
            bot_tasks.save_task_to_base_and_send_to_students.delay(
                                            title=form.title.data, 
                                            description=form.description.data, 
                                            group=form.group.data, 
                                            lesson=lesson,
                                            user_uuid=flask_login.current_user.uuid,
                                            file=form.file.data.read() if form.file.data else None,
                                            filename=form.file.data.filename if form.file.data else None)
            
            return redirect(url_for(".cabinet_page", from_task=True))
    return render_template("send_task.html", form=form, user=flask_login.current_user)


# Task page
@cab_bp.route("/task/<int:id>")
@flask_login.login_required
def task_page(id):
    task = cabinet_service.get_task_by_id(db.session, user_uuid=flask_login.current_user.uuid, id=id)
    if not task:
        return redirect(url_for(".cabinet_page"))
    return render_template("task_page.html", task=task)


# Handler for download file from task
@cab_bp.route("/task/<int:id>/download")
@flask_login.login_required
def download_file(id):
    file = cabinet_service.get_file_by_task_id(db.session, user_uuid=flask_login.current_user.uuid, id=id)
    if file:
        return send_file(file.download_file(), download_name=file.file_name)


# ---- Home Page and Info ----

# Home page user
@cab_bp.route("/")
@cab_bp.route("/<int(min=1):page>")
@flask_login.login_required
def cabinet_page(page=1):
    tasks = cabinet_service.get_all_tasks(db=db.session, user_uuid=flask_login.current_user.uuid, page=page)
    # If method called from sending task, param: from_task equal to 1
    # In html document java script code check is param and if it equal 1 show modal message about success sending task
    from_task = 0
    if request.args.get("from_task"):
        from_task = 1
    return render_template("home.html", name_form=NameForm(), lesson_form=LessonForm(),
                           user=flask_login.current_user, tasks=tasks, from_task=from_task)


# Info Page
@cab_bp.route("/info")
@flask_login.login_required
def info_page():
    return render_template("info_page.html")
