# Defines the Flask application instance
from app import app

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import Student, Teacher

@app.shell_context_processor
def make_shell_context():
    return {'sa':sa, 'so':so, 'db':db, 'Student':Student, 'Teacher':Teacher}
