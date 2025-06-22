from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('მომხმარებელი', validators=[DataRequired()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    submit = SubmitField('შესვლა')

class RegistrationForm(FlaskForm):
    username = StringField('მომხმარებელი', validators=[DataRequired()])
    email = StringField('ელფოსტა', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    submit = SubmitField('რეგისტრაცია')

class ProductForm(FlaskForm):
    name = StringField('პროდუქტის სახელი', validators=[DataRequired()])
    description = TextAreaField('აღწერა', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('დამატება')
