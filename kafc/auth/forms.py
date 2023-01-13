from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class SignUpForm(FlaskForm):
	login = StringField(validators=[DataRequired(), 
									Length(min=3, max=50)], 
						render_kw={"placeholder": "Login"})

	password = PasswordField(validators=[DataRequired(), 
										 Length(min=8, max=100)],
							 render_kw={"placeholder": "Password"})

	repeat_password = PasswordField(validators=[DataRequired(), 
												Length(min=8, max=100), 
												EqualTo("password",
                                                         message="Паролі повинні співпадати")],
							 		render_kw={"placeholder": "Repeat Password"})

	submit = SubmitField("Sign up")	


class LoginForm(FlaskForm):

	login = StringField(validators=[DataRequired(), 
		   							Length(min=3, max=50)], 
						render_kw={"placeholder": "Login"})

	password = PasswordField(validators=[DataRequired(), 
										 Length(min=8, max=100)],
							 render_kw={"placeholder": "Password"})

	submit = SubmitField("Login")	