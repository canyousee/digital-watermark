from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm):
    username=StringField('Name',validators=[DataRequired()])
    #id= StringField('Id',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    username=StringField('Name',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignInForm(FlaskForm):
    username=StringField('Name',validators=[DataRequired()])
    #id= StringField('Id',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])