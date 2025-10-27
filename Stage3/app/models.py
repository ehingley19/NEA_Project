from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
# UserMixin is a class that automatically adds implementations required by Flask_Login in a User class
from flask_login import UserMixin

# Defining the Teacher class that my Teacher database will be an instance of
class Teacher(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    forename: so.Mapped[str] = so.mapped_column(sa.String(50))
    surname: so.Mapped[str] = so.mapped_column(sa.String(50))
    username: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(100), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    year_group: so.Mapped[str] = so.mapped_column(sa.String(1))

    class_of_students: so.WriteOnlyMapped['Student'] = so.relationship(back_populates='class_teacher')

    # Defining how to print objects of this class
    def __repr__(self):
        return f'<Teacher {self.forename} {self.surname} ({self.username})>'
    
    # Defining methods for setting and checking Teacher account passwords and their hashes
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return f"teacher:{self.id}"

# Defining the Student class that my Student database will be an instance of
class Student(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    forename: so.Mapped[str] = so.mapped_column(sa.String(50))
    surname: so.Mapped[str] = so.mapped_column(sa.String(50))
    username: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(100), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    teacher_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Teacher.id, name="fk_student_teacher_id"),
        index=True
        )

    class_teacher: so.Mapped['Teacher'] = so.relationship(back_populates='class_of_students')

    # Defining how to print objects of this class
    def __repr__(self):
        return f'<Student {self.forename} {self.surname} ({self.username})>'

    # Defining methods for setting and checking Teacher account passwords and their hashes
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return f"student:{self.id}"

@login.user_loader
def load_user(composite_id):
    userType, userId = composite_id.split(":", 1)
    if userType == "teacher":
        return db.session.get(Teacher, int(userId))
    elif userType == "student":
        return db.session.get(Student, int(userId))
    return None
