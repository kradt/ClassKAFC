from sqlalchemy.orm import Session
from werkzeug.datastructures import FileStorage

from kafc.database import models
from kafc.schemas.task_schema import TaskCreate


# ---- Task Functionality ----

# function create new task by TaskCreate schema
def create_task(db: Session, task: TaskCreate, user_uuid: str, file: FileStorage | None = None) -> models.Task:
	user = db.query(models.User).filter_by(uuid=user_uuid).first()
	db_task = models.Task(title=task.title, description=task.description, group=task.group)

	lesson = db.query(models.Lesson).filter_by(name=task.lesson.name).first()
	# If the file was transferred, create file object and add him to task
	if file:
		db_file = models.File(file_name=str(file.filename), file_data=file.read())
		db_task.file = db_file

	db_task.lesson = lesson
	user.tasks.append(db_task)
	db.add(user)
	db.commit()
	db.refresh(db_task)
	return db_task


# function delete task and file inside him
def delete_task_by_id(db: Session, user_uuid: str, id: int) -> None:
	task = get_task_by_id(db, user_uuid, id)
	if task:
		db.delete(task)
	file = task.file
	if file:
		db.delete(file)
	db.commit()


# function returning all tasks by user for pagination process
def get_all_tasks(db: Session, user_uuid: str, page: int = 1, limit: int = 5) -> dict:
	tasks: dict = db.query(models.Task) \
		.join(models.User) \
		.filter_by(uuid=user_uuid) \
		.filter(models.Task.author_id == models.User.id) \
		.order_by(models.Task.date_publish.desc()) \
		.paginate(per_page=limit, page=page)

	return tasks


# function returning particular task by id
def get_task_by_id(db: Session, user_uuid: str, id: int) -> models.Task:
	task = db.query(models.Task) \
		.filter_by(id=id) \
		.join(models.User) \
		.filter_by(uuid=user_uuid) \
		.filter(models.Task.author_id == models.User.id) \
		.first()

	return task
	

# ---- User functionality ----

# function update user data
def update_user(
		db: Session,
		user_uuid: str,
		name: str | None = None,
		lesson_name: str | None = None) -> models.User | None:

	user = db.query(models.User).filter_by(uuid=user_uuid).first()
	if not user:
		return None
	if name:
		user.name = name
	if lesson_name:
		# If another user already has this lesson, we don't need to create a new one
		lesson_already_in_base = db.query(models.Lesson).filter_by(name=lesson_name).first() 
		user.lessons.append(lesson_already_in_base if lesson_already_in_base else models.Lesson(name=lesson_name))
	db.add(user)
	db.commit()
	return user


# function remove lesson from user
def remove_user_lesson(db: Session, user_uuid: str, lesson_name: str) -> models.User | None:
	user = db.query(models.User).filter_by(uuid=user_uuid).first()
	lesson = db.query(models.Lesson).filter_by(name=lesson_name).first()
	if not lesson:
		return None
	user.lessons.remove(lesson)
	db.add(user)
	db.commit()
	return user


# ---- File Functionality ----

# function getting file
def get_file_by_task_id(db: Session, user_uuid: str, id: int) -> models.File:
	task = get_task_by_id(db, user_uuid, id)
	return task.file
