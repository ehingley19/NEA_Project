from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

# Defining the routes to the view function below
@app.route('/')
@app.route('/index')

# Creating a view function for the home page
def index():
    # Creating a mock teacher using a dictionary
    user = {'username': 'Jamie'}
    # Creating mock students using dictionaries
    students = [
        {
            'pupil': {'firstName': 'Mary', 'surname': 'Jabami'},
            'progress': {'workingAt': 'Year 5', 'quizCount': '30'}
        },
        {
            'pupil': {'firstName': 'Dave', 'surname': 'Evans'},
            'progress': {'workingAt': 'Year 3', 'quizCount': '10'}
        },
    ]
    # Returning a personalised view of the home page by rendering the index.html template
    return render_template('index.html', title='Home Page', user=user, students=students)

# Defining the routes to the view function below
@app.route('/login', methods=['GET', 'POST'])

# Creating a view function for the login page
def login():
    # Instantiating an object 'form' from class LoginForm, which is then passed into the template
    form = LoginForm()
    # Running a method that checks fields against the validators specified in forms.py, which returns True if
    # all fields pass validation, otherwise returning False and re-rendering the form
    if form.validate_on_submit():
        # Showing a message to the user, confirming successful login
        flash('Login requested for user {}'.format(form.username.data))
        return redirect(url_for("index")) 
    return render_template('login.html', title='Log In', form=form)
