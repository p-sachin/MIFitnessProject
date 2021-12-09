from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.fields.core import FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from web_app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken, choose another one')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken, choose another one')
        



class LoginForm(FlaskForm):
        email = StringField('Email',
                            validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember = BooleanField('Remember Me')
        submit = SubmitField('Login')


class PersonalForm(FlaskForm):
        fname = StringField('First Name',validators=[DataRequired()])
        lname = StringField('Last Name',validators=[DataRequired()])
        age = IntegerField('Age',
                            validators=[DataRequired()])
        height = FloatField('Height (cm)', validators=[DataRequired()])
        weight = FloatField('Weight (kg)', validators=[DataRequired()])
        gender = StringField('Gender (M,F)',validators=[DataRequired(),Length(min=1,max=2)])
        submit = SubmitField('Save')

class UploadForm(FlaskForm):
    csv = FileField('upload csv',validators=[FileAllowed(['csv'])])
    submit = SubmitField('Save')
