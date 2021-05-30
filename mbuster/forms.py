from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
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

class AddMovieForm(FlaskForm):
    movie_title = StringField('Title',
                        validators=[
                            DataRequired(),
                        ])
    stock = BooleanField('Checked Out')
    submit = SubmitField('Add')
    
class UserMovieForm(FlaskForm):
    delete_submit = SubmitField('X')
    