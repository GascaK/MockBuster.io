from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from wtforms.widgets.core import TextArea
from mbuster.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[
                                DataRequired(), 
                                Length(min=2, max=20)
                                ])
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                                    ])
    password = PasswordField('Password', validators=[
                                            DataRequired(),
                                            ])
    confirm_password = PasswordField('Confirm Password', validators=[
                                            DataRequired(),
                                            EqualTo('password')
                                            ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email has already been used.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                            ])
    password = PasswordField('Password', validators=[
                                            DataRequired(),
                                            ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                            ])
    submit = SubmitField('Request Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account found with that email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
                                            DataRequired(),
                                            ])
    confirm_password = PasswordField('Confirm Password', validators=[
                                            DataRequired(),
                                            EqualTo('password')
                                            ])
    submit = SubmitField('Reset Password')

class AddMovieForm(FlaskForm):
    movie_title = StringField('Title',
                        validators=[
                            DataRequired(),
                        ])
    stock = BooleanField('Checked Out')
    submit = SubmitField('Add')
    
class UserMovieForm(FlaskForm):
    delete_submit = SubmitField('X')
    
class ContactForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    subject = StringField('Subject',
                        validators=[
                            DataRequired(),
                            Length(min=2, max=20)
                            ])
    content = TextAreaField('Text')
    submit = SubmitField('Send')