from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Teacher(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    forename: so.Mapped[str] = so.mapped_column(sa.String(50))
    surname: so.Mapped[str] = so.mapped_column(sa.String(50))
    username: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(100), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    year_group: so.Mapped[str] = so.mapped_column(sa.String(1))

    class_of_students: so.WriteOnlyMapped['Student'] = so.relationship(back_populates='class_teacher')

    def __repr__(self):
        return f'<Teacher {self.forename} {self.surname} ({self.username})>'

class Student(db.Model):
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

    def __repr__(self):
        return f'<Student {self.forename} {self.surname} ({self.username})>'
