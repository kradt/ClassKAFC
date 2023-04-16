from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField(
        validators=[Length(min=3, max=100)],
        render_kw={"placeholder": "Ім'я По батькові"})

    submit = SubmitField("Зберегти")


class LessonForm(FlaskForm):
    lesson = StringField(
        validators=[Length(min=3)],
        render_kw={"placeholder": "Предмет"})

    submit = SubmitField("Зберегти")


class TaskForm(FlaskForm):
    title = StringField(
        validators=[DataRequired(), Length(min=3)],
        render_kw={"placeholder": "Введіть заголовок для завдання"})

    description = StringField(widget=TextArea(), render_kw={"placeholder": "Опишіть Завдання"})

    file = FileField(
        validators=[FileAllowed(["jpg", "pdf", "png", "mp3", "mp4", "docx", "doc", "zip", "txt", "pptx"],
                                "Not allowed file type")],
        render_kw={"id": "customFile"})
    # TODO: create multiply groups
    group = SelectField(choices=["351"], coerce=int)
    lesson = SelectField(coerce=str)

    submit = SubmitField("Відправити завдання")

    def __init__(self, lessons, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if lessons:
            choices = [(i.name, i.name) for i in lessons]
        else:
            choices = [("0", "Ви ще не добавляли предмети в особистому кабінеті")]
        self.lesson.choices = choices
