from flask import render_template, flash, redirect, url_for, session, request
from app import app, db
from app.forms import LoginForm, CreateTeacherForm, CreateStudentForm, TopicTestForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app.models import Teacher, Student

# Function that redirects students trying to access teacher pages, and teachers trying to access student pages
def student_teacher_redirect(user):
    if not current_user.is_authenticated:
        return redirect(url_for(f'{user}_login'))
    composite_id = current_user.get_id()
    userType = composite_id.split(":", 1)
    if userType[0] != user:
        return redirect(url_for('index'))
    return None

# Function that handles creating topic tests and storing their results
def handle_topic_test(year, filename, title):
    if student_teacher_redirect("student"):
        return student_teacher_redirect("student")
    questionsUsed = None
    # If the form is being submitted, the questions that were used are retrieved from session, which prevented
    # them from being overwritten
    if request.method == "POST" and "questionsUsed" in session:
        questionsUsed = session["questionsUsed"]
        form = TopicTestForm()
        form.questionsUsed = questionsUsed
    # Otherwise, a new form is generated and the questions used are saved in session, to be retrieved later
    else:
        form = TopicTestForm(year, filename)
        session["questionsUsed"] = form.questionsUsed
    
    if form.validate_on_submit():
        # Checking if the student has tried to resubmit the same test, and redirecting if so
        if "questionsUsed" not in session or questionsUsed is None:
            flash("You cannot resubmit the same test")
            return redirect(url_for('student_portal'))
        results = []
        score = 0
        # Storing the question, student's answer, correct answer and mark for each question in a dictionary
        for i in range(10):
            question, correctAnswer = questionsUsed[i]
            studentAnswer =  getattr(form, f"question{i+1}").data
            if studentAnswer == correctAnswer:
                isCorrect = True
                score += 1
            else:
                isCorrect = False
            results.append({
                "question": question,
                "studentAnswer": studentAnswer,
                "correctAnswer": correctAnswer,
                "isCorrect": isCorrect
            })
        # Saving the dictionary, title and score in a Flask session to access in the topic_results page
        session["results"] = results
        session["title"] = title
        session["score"] = score
        # Removing the stored questionsUsed from session to stop students from resubmitting the same test
        session.pop("questionsUsed", None)
        return redirect(url_for('topic_test_results'))
    return render_template('topic_test.html', title=title, form=form)

# Defining the routes to the view function below
@app.route('/')
@app.route('/index')
# Creating a view function for the home page
def index():
    return render_template('index.html', title='Home Page')

# Defining the routes to the view function below
@app.route('/teacher_login', methods=['GET', 'POST'])
# Creating a view function for the teacher login page
def teacher_login():
    # Redirecting the user back to the home page if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Instantiating an object 'form' from class LoginForm, which is then passed into the template
    form = LoginForm()
    # Running a method that checks fields against the validators specified in forms.py, which returns True if
    # all fields pass validation, otherwise returning False and re-rendering the form
    if form.validate_on_submit():
        query = sa.select(Teacher).where(Teacher.username == form.username.data)
        user = db.session.scalar(query)
        # Running a lookup validation check on username and password in the Teacher database
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('teacher_login'))
        # Logging user in if lookup check is passed then redirecting the user
        login_user(user)
        return redirect(url_for('teacher_portal'))
    return render_template('login.html', title='Teacher Login', form=form)

# Defining the routes to the view function below
@app.route('/student_login', methods=['GET', 'POST'])
# Creating a view function for the student login page
def student_login():
    # Redirecting the user back to the home page if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Instantiating an object 'form' from class LoginForm, which is then passed into the template
    form = LoginForm()
    # Running a method that checks fields against the validators specified in forms.py, which returns True if
    # all fields pass validation, otherwise returning False and re-rendering the form
    if form.validate_on_submit():
        query = sa.select(Student).where(Student.username == form.username.data)
        user = db.session.scalar(query)
        # Running a lookup validation check on username and password in the Student database
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('student_login'))
        # Logging user in if lookup check is passed then redirecting the user
        login_user(user)
        return redirect(url_for('student_portal'))
    return render_template('login.html', title='Student Login', form=form)

# Defining the routes to the view function below
@app.route('/logout')
# Creating a view function for the logout function
def logout():
    logout_user()
    return redirect(url_for('index'))

# Defining the routes to the view function below
@app.route('/create_teacher_account', methods=['GET', 'POST'])
# Creating a view function for the create teacher account page
def create_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateTeacherForm()
    if form.validate_on_submit():
        # Creating new teacher instance from data collected from the account creation form
        newTeacher = Teacher(
            forename=form.forename.data, surname=form.surname.data, username=form.username.data, email=form.email.data, year_group=form.year_group.data
        )
        newTeacher.set_password(form.password.data)
        # Submitting the new teacher account into the Teacher database
        db.session.add(newTeacher)
        db.session.commit()
        flash('Teacher account creation successful')
        return redirect(url_for('teacher_login'))
    return render_template('create_teacher.html', title='Create Teacher Account', form=form)

# Defining the routes to the view function below
@app.route('/create_student_account', methods=['GET', 'POST'])
# Creating a view function for the create student account page
def create_student():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateStudentForm()
    if form.validate_on_submit():
        # Creating new student instance from data collected from the account creation form
        newStudent = Student(
            forename=form.forename.data, surname=form.surname.data, username=form.username.data, email=form.email.data, teacher_id=form.teacher_id.data
        )
        newStudent.set_password(form.password.data)
        # Submitting the new teacher account into the Student database
        db.session.add(newStudent)
        db.session.commit()
        flash('Student account creation successful')
        return redirect(url_for('student_login'))
    return render_template('create_student.html', title='Create Student Account', form=form)

# Defining the routes to the view function below
@app.route('/teacher_portal')
# Creating a view function for the teacher portal
def teacher_portal():
    if student_teacher_redirect("teacher"):
        return student_teacher_redirect("teacher")
    return render_template('teacher_portal.html', title='Teacher Portal')

# Defining the routes to the view function below
@app.route('/student_portal')
# Creating a view function for the student portal
def student_portal():
    if student_teacher_redirect("student"):
        return student_teacher_redirect("student")
    return render_template('student_portal.html', title='Student Portal')

# Defining the routes to the view function below
@app.route('/year_1_addition_and_subtraction', methods=['GET', 'POST'])
# Creating a view function for the Year 1 'Addition and subtraction' topic test
def yr1_addition_and_subtraction():
    return handle_topic_test("year1", "addition_subtraction.txt", "Year 1 Topic Test - Addition and subtraction")

# Defining the routes to the view function below
@app.route('/year_2_addition_and_subtraction', methods=['GET', 'POST'])
# Creating a view function for the Year 2 'Addition and subtraction' topic test
def yr2_addition_and_subtraction():
    return handle_topic_test("year2", "addition_subtraction.txt", "Year 2 Topic Test - Addition and subtraction")

# Defining the routes to the view function below
@app.route('/year_3_addition_and_subtraction', methods=['GET', 'POST'])
# Creating a view function for the Year 3 'Addition and subtraction' topic test
def yr3_addition_and_subtraction():
    return handle_topic_test("year3", "addition_subtraction.txt", "Year 3 Topic Test - Addition and subtraction")

# Defining the routes to the view function below
@app.route('/year_4_addition_and_subtraction', methods=['GET', 'POST'])
# Creating a view function for the Year 4 'Addition and subtraction' topic test
def yr4_addition_and_subtraction():
    return handle_topic_test("year4", "addition_subtraction.txt", "Year 4 Topic Test - Addition and subtraction")

# Defining the routes to the view function below
@app.route('/year_5_addition_and_subtraction', methods=['GET', 'POST'])
# Creating a view function for the Year 5 'Addition and subtraction' topic test
def yr5_addition_and_subtraction():
    return handle_topic_test("year5", "addition_subtraction.txt", "Year 5 Topic Test - Addition and subtraction")

# Defining the routes to the view function below
@app.route('/year_6_addition_and_subtraction', methods=['GET', 'POST'])
# Creating a view function for the Year 6 'Addition and subtraction' topic test
def yr6_addition_and_subtraction():
    return handle_topic_test("year6", "addition_subtraction.txt", "Year 6 Topic Test - Addition and subtraction")

# Defining the routes to the view function below
@app.route('/topic_test_results')
# Creating a view function for the topic test results page
def topic_test_results():
    results = session.get("results", None)
    if results is None:
        return redirect(url_for('student_portal'))
    title = session.get("title", "Topic Test Results")
    score = session.get("score", "N/A")
    return render_template('topic_test_results.html', title=title, score=score, results=results)
