import uuid
import datetime
import io
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy.ext.declarative import DeclarativeMeta

from . import db
from .. import manage_s3


BaseModel: DeclarativeMeta = db.Model

user_lesson = db.Table(
    "user_lesson",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("lesson_id", db.ForeignKey("lesson.id"))
)


class User(BaseModel, UserMixin):
    """
        Table User - it's Parent table of relationship, It has all data about user
        have many-to-one relationship with Table Task
        User have many-to-many relationship with Table Lesson
    """
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    name = db.Column(db.String(50), default=None)
    role = db.Column(db.String(20), default=None)

    lessons = db.relationship("Lesson", secondary=user_lesson, back_populates="teachers")
    tasks = db.relationship("Task", back_populates="author", lazy="joined", order_by="desc(Task.date_publish)")

    def __init__(self, username: str, password: str, role: str | None = None) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.uuid = str(uuid.uuid4())
        self.role = role

    def __repr__(self) -> str:
        return f"<User {self.username} >"

    def get_id(self) -> str:
        return self.uuid


class Lesson(BaseModel):
    """
        Table lesson - it's table which have all lessons
        Table lesson have relation many to many with User table
    """
    __tablename__ = 'lesson'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    teachers = db.relationship("User", secondary=user_lesson, back_populates="lessons")

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Lesson {self.name}>"


class File(BaseModel):
    """
        Table File have link of file which added to Task
        File have relationship with task, and File it's Child of Task Table
    """
    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(150))
    obj_name = db.Column(db.String(50), unique=True)
    fileid = db.Column(db.String(100), default=None)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))

    task = db.relationship("Task", back_populates="file", uselist=False)

    def __init__(self, file_name: str, file_data: bytes, fileid: str | None = None) -> None:
        self.file_name = file_name
        self.obj_name = str(uuid.uuid4()) + "." + self.file_name.split(".")[-1]
        self.fileid = fileid
        self.upload_fileobj(file_data, self.obj_name)

    def __repr__(self) -> str:
        return f"<File {self.id}>"

    @staticmethod
    def upload_fileobj(file: bytes, filename: str) -> None:
        manage_s3.upload_file(io.BytesIO(file), filename)

    def drop_file(self):
        manage_s3.drop_file(self.obj_name)

    def download_file(self):
        return manage_s3.download_file(self.obj_name)


class Task(BaseModel):
    """
        Table Task have all data about Task sent to users
        Task have relationship with User and File tables
        Task it's Parent Table of File Table and Child Table of User Table
    """
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    group = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    date_publish = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"))

    lesson = db.relationship("Lesson", backref="tasks", lazy="joined", uselist=False)
    file = db.relationship("File", back_populates="task", lazy="joined", uselist=False)
    author = db.relationship("User", back_populates="tasks", uselist=False)

    def __init__(self, title: str, group: int, description: str) -> None:
        self.uuid = str(uuid.uuid4())
        self.title = title
        self.group = group
        self.description = description
        self.date_publish = datetime.datetime.now().strftime("%y-%m-%d %H:%M")

    def __repr__(self) -> str:
        return f"<Task {self.title}>"


class BotUser(BaseModel):
    __tablename__ = "bot_user"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(100))
    group = db.Column(db.Integer, default=351)

    def __init__(self, user_id: str, username: str, group: int = 351) -> None: 
        self.user_id = user_id
        self.username = username
        self.group = group

    def __repr__(self) -> str:
        return f"<User {self.username}"
