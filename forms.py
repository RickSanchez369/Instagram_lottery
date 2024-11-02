
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class LotteryChoiceForm(FlaskForm):
    lottery_type = SelectField('Select Lottery Type', choices=[
        ('comments', 'Lottery by Comments'),
        ('likes', 'Lottery by Likes'),
        ('score', 'Lottery by score'),
        ('followers', 'Lottery by Followers')
    ])
    submit = SubmitField('Proceed')
