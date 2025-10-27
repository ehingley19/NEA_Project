from flask_wtf import FlaskForm
# Importing the classes that represent the field types that will be used in the form 
from wtforms import StringField, PasswordField, SubmitField
# Importing validators that will be used in the form
from wtforms.validators import ValidationError, DataRequired, Email
import sqlalchemy as sa
from app import db
from app.models import Teacher, Student
from flask import current_app
import os
import random

# Creating the student and teacher login form as an instance of class FlaskForm
class LoginForm(FlaskForm):
    # Creating the login fields as objects, which are also defined as class variables of class LoginForm
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

# Creating the teacher account creation form as an instance of class FlaskForm
class CreateTeacherForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    year_group = StringField('Your Classes\' Year Group', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        query = sa.select(Teacher).where(Teacher.username == username.data)
        teacher = db.session.scalar(query)
        if teacher is not None:
            raise ValidationError('A teacher with that username already exists.')
    
    def validate_email(self, email):
        query = sa.select(Teacher).where(Teacher.email == email.data)
        teacher = db.session.scalar(query)
        if teacher is not None:
            raise ValidationError('A teacher with that email already exists.')
    
    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        hasUpper = False
        hasLower = False
        hasDigit = False
        for character in password.data:
            if character.isupper():
                hasUpper = True
            elif character.islower():
                hasLower = True
            elif character.isdigit():
                hasDigit = True
        if hasUpper == False or hasLower == False:
            raise ValidationError('Password must contain an upper and lowercase letter.')
        if hasDigit == False:
            raise ValidationError('Password must contain a number.')
    
    def validate_year_group(self, year_group):
        if len(year_group.data) != 1 or year_group.data.isnumeric() == False:
            raise ValidationError('Year group must be a single digit.')
        elif int(year_group.data) < 1 or int(year_group.data) > 6:
            raise ValidationError('Year group must be from 1 to 6.')

# Creating the student account creation form as an instance of class FlaskForm
class CreateStudentForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    teacher_id = StringField('Your Teacher\'s ID', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        query = sa.select(Student).where(Student.username == username.data)
        student = db.session.scalar(query)
        if student is not None:
            raise ValidationError('A student with that username already exists')
    
    def validate_email(self, email):
        query = sa.select(Student).where(Student.email == email.data)
        student = db.session.scalar(query)
        if student is not None:
            raise ValidationError('A student with that email already exists')
    
    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        hasUpper = False
        hasLower = False
        hasDigit = False
        for character in password.data:
            if character.isupper():
                hasUpper = True
            elif character.islower():
                hasLower = True
            elif character.isdigit():
                hasDigit = True
        if hasUpper == False or hasLower == False:
            raise ValidationError('Password must contain an upper and lowercase letter')
        if hasDigit == False:
            raise ValidationError('Password must contain a number')
    
    def validate_teacher_id(self, teacher_id):
        query = sa.select(Teacher).where(Teacher.id == teacher_id.data)
        teacher = db.session.scalar(query)
        if teacher is None:
            raise ValidationError('Teacher ID does not link to an existing teacher')

# Creating the student account creation form as an instance of class FlaskForm
class TopicTestForm(FlaskForm):
    question1 = StringField('Question 1')
    question2 = StringField('Question 2')
    question3 = StringField('Question 3')
    question4 = StringField('Question 4')
    question5 = StringField('Question 5')
    question6 = StringField('Question 6')
    question7 = StringField('Question 7')
    question8 = StringField('Question 8')
    question9 = StringField('Question 9')
    question10 = StringField('Question 10')
    submit = SubmitField('Mark Topic Test')
    
    def __init__(self, year = None, filename = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reading the given file and converting it into an array called questionList
        if year and filename:
            filepath = os.path.join(current_app.root_path, "question_sets", year, filename)
            file = open(filepath, "r", encoding = "utf-8")
            questionList = []
            for line in file:
                line = line.strip()
                question, answer = line.split("|", 1)
                questionList.append([question, answer])
            file.close()
            # Changing label of each question to a random question from questionList
            self.questionsUsed = []
            for i in range(1, 11):
                field = getattr(self, f"question{i}")
                number = random.randint(0, len(questionList)-1)
                field.label.text = questionList[number][0]
                # Remembering the questions asked and their respective answers
                self.questionsUsed.append(questionList[number])
