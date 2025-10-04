# Code taken from Grinberg, M (2023) 'The New and Improved Flask Mega-Tutorial (2024 Edition)', p. 29
from flask_wtf import FlaskForm
# Importing the classes that represent the field types that will be used in the form 
from wtforms import StringField, PasswordField, SubmitField
# Importing a presence check validator which will be used in the form
from wtforms.validators import DataRequired

# Creating the user login form as an instance of class FlaskForm
class LoginForm(FlaskForm):
    # Creating the login fields as objects, which are also defined as class variables of class LoginForm
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
