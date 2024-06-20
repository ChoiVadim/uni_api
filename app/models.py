from .init import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Department(db.Model):
    __tablename__ = "department"
    dept_name = db.Column(db.String(20), primary_key=True)
    building = db.Column(db.String(15))
    budget = db.Column(db.Numeric(12, 2), nullable=False)


class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.String(8), primary_key=True)
    title = db.Column(db.String(50))
    dept_name = db.Column(
        db.String(20), db.ForeignKey("department.dept_name"), nullable=True
    )
    credits = db.Column(db.Numeric(2, 0), nullable=False)


class Instructor(db.Model):
    __tablename__ = "instructor"
    ID = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    dept_name = db.Column(
        db.String(20), db.ForeignKey("department.dept_name"), nullable=True
    )
    salary = db.Column(db.Numeric(8, 2), nullable=False)


class Section(db.Model):
    __tablename__ = "section"
    course_id = db.Column(
        db.String(8), db.ForeignKey("course.course_id"), primary_key=True
    )
    sec_id = db.Column(db.String(8), primary_key=True)
    semester = db.Column(db.String(6), primary_key=True)
    year = db.Column(db.Numeric(4, 0), primary_key=True)
    building = db.Column(
        db.String(15), db.ForeignKey("classroom.building"), nullable=True
    )
    room_number = db.Column(
        db.String(7), db.ForeignKey("classroom.room_number"), nullable=True
    )
    time_slot_id = db.Column(db.String(4))


class Student(db.Model):
    __tablename__ = "student"
    ID = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    dept_name = db.Column(
        db.String(20), db.ForeignKey("department.dept_name"), nullable=True
    )
    tot_cred = db.Column(db.Numeric(3, 0), nullable=False)


class Takes(db.Model):
    __tablename__ = "takes"
    ID = db.Column(db.String(5), db.ForeignKey("student.ID"), primary_key=True)
    course_id = db.Column(
        db.String(8), db.ForeignKey("section.course_id"), primary_key=True
    )
    sec_id = db.Column(db.String(8), primary_key=True)
    semester = db.Column(db.String(6), primary_key=True)
    year = db.Column(db.Numeric(4, 0), primary_key=True)
    grade = db.Column(db.String(2))


class Classroom(db.Model):
    __tablename__ = "classroom"
    building = db.Column(db.String(15), primary_key=True)
    room_number = db.Column(db.String(7), primary_key=True)
    capacity = db.Column(db.Numeric(4, 0))


class Teaches(db.Model):
    __tablename__ = "teaches"
    ID = db.Column(db.String(5), db.ForeignKey("instructor.ID"), primary_key=True)
    course_id = db.Column(
        db.String(8), db.ForeignKey("section.course_id"), primary_key=True
    )
    sec_id = db.Column(db.String(8), primary_key=True)
    semester = db.Column(db.String(6), primary_key=True)
    year = db.Column(db.Numeric(4, 0), primary_key=True)
