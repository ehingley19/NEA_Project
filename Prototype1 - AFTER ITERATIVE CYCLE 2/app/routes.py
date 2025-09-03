from flask import render_template
from app import app

# Creating a route to the home page
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
