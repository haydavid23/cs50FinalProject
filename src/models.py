from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    gradeLevel = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    
    def __repr__(self):
        return '<Teachers %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "gradeLevel": self.gradeLevel,
            "username": self.username
            # do not serialize the password, its a security breach
        }

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    gradeLevel = db.Column(db.String(80), unique=False, nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Students %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "username": self.username
 
            # do not serialize the password, its a security breach
        }

class StudentsClassGrades(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer,  nullable=False)
    subjectId = db.Column(db.Integer, nullable=False)
    schoolTermId = db.Column(db.Integer, nullable=False)
    gradeAvg = db.Column(db.Float, unique=False, nullable=True)
    gradeLetter = db.Column(db.String(5), unique=False, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('studentId', 'subjectId','schoolTermId'),
    )

    def __repr__(self):
        return '<StudentsGrades %r>' % self.studentId

    def serialize(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "subjectId": self.subjectId,
            "schoolTermId": self.schoolTermId,
            "gradeAvg": self.gradeAvg,
            "gradeLetter": self.gradeLetter   
 
            # do not serialize the password, its a security breach
        }



class SubmitedAssignments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, unique=False, nullable=False)
    subjectId = db.Column(db.Integer, unique=False, nullable=False)
    assignmentName = db.Column(db.String(100), unique=False, nullable=False)
    grade = db.Column(db.Float, unique=False, nullable=True)
    submittedFile = db.Column(db.String(80), unique=False, nullable=True)
    submitedDate = db.Column(db.DateTime,unique=True, nullable=True,default=db.func.current_timestamp())
    schoolTermId = db.Column(db.Integer, unique=False, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('studentId', 'subjectId','assignmentName'),
    )


    def __repr__(self):
        return '<SubmitedAssignments %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "subjectId": self.subjectId,
            "studentId": self.studentId,
            "assignmentName": self.assignmentName,
            "submitedDate": self.submitedDate,
            "submittedFile": self.submittedFile,
            "schoolTermId": self.schoolTermId,
            "grade": self.grade

            # do not serialize the password, its a security breach
        }

class SchoolTerm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quarter= db.Column(db.String(20), unique=False, nullable=False)
    schoolYear = db.Column(db.String(20), unique=False, nullable=False)
    current = db.Column(db.Boolean, unique=False, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('quarter', 'schoolYear'),
    )

    def __repr__(self):
        return '<SchoolTerm %r>' % self.schoolYear

    def serialize(self):
        return {
            "id":self.id,
            "quarter": self.quarter,
            "schoolYear": self.schoolYear,
            "current":self.current


            # do not serialize the password, its a security breach
        }


class AssignedAssignments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignmentName = db.Column(db.String(30), unique=False, nullable=False)
    subjectId = db.Column(db.Integer, unique=False, nullable=False)
    note = db.Column(db.String(80), unique=False, nullable=True)
    assignmentFile = db.Column(db.String(80), unique=False, nullable=True)
    dueDate = db.Column(db.DateTime, unique=False, nullable=True)
    assignedDate = db.Column(db.DateTime, unique=False, nullable=False, default=db.func.current_timestamp())
    schoolTermId = db.Column(db.Integer, unique=False, nullable=False)
    submittable = db.Column(db.Boolean, unique=False, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('assignmentName', 'schoolTermId'),
    )

    def __repr__(self):
        return '<AssignedAssignments %r>' % self.assignmentName

    def serialize(self):
        return {
            "id": self.id,
            "assignmentName":self.assignmentName,
            "subjectId": self.subjectId,
            "note": self.note,
            "assignmentFile": self.assignmentFile,
            "dueDate": self.dueDate,
            "assignedDate":self.assignedDate,
            "schoolTermId":self.schoolTermId,
            "submittable": self.submittable
            }


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(30), unique=True, nullable=False)


    def __repr__(self):
        return '<Subjects %r>' % self.subject

    def serialize(self):
        return {
            "id": self.id,
            "subject": self.subject
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    userName = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
 
    def __repr__(self):
        return '<User %r>' % self.user

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
            # do not serialize the password, its a security breach
        }
