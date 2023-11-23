from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
import re
from lip.model import User



class PasswordValidation:
    def __init__(self, uppercase=True, lowercase=True, digits=True, special=True):
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.digits = digits
        self.special = special

    def __call__(self, _, field):
        password = field.data

        if self.uppercase and not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter.')

        if self.lowercase and not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter.')

        if self.digits and not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one digit.')

        if self.special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character.')

class UsernameValidation:
    def __call__(self, _, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

class EmailValidation:
    def __call__(self, _, field):
        email_address = User.query.filter_by(email_address=field.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')
        
class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=10, max=30), DataRequired(), UsernameValidation()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired(), EmailValidation()])
    password1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired(), PasswordValidation()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')