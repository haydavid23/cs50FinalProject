from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    gradeLevel = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    
    def __repr__(self):
        return '<Teacher %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "name": self.lastName,
            "name": self.gradeLevel,
            "name": self.username,
            "name": self.teacherId
            # do not serialize the password, its a security breach
        }

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    gradeLevel = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Students %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "name": self.lastName,
            "name": self.gradeLevel,
            "name": self.username
 
            # do not serialize the password, its a security breach
        }

class StudentsGrades(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer,  nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    gradeLevel = db.Column(db.String(80), unique=False, nullable=False)
    semesterId = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(80), unique=False, nullable=False)

    # __table_args__ = (
    #     db.UniqueConstraint('studentId', 'subject','semesterId'),
    # )

    def __repr__(self):
        return '<StudentsGrades %r>' % self.grade

    def serialize(self):
        return {
            "id": self.id,
            "name": self.studentId,
            "name": self.subject,
            "name": self.gradeLevel,
            "name": self.grade
 
            # do not serialize the password, its a security breach
        }



class SubmitedAssigments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, unique=False, nullable=False)
    subject = db.Column(db.String(100), unique=False, nullable=False)
    assigmentName = db.Column(db.String(100), unique=False, nullable=False)
    grade = db.Column(db.Float, unique=False, nullable=True)
    semesterId = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<SubmitedAssigments %r>' % self.assigmentName

    def serialize(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "studentId": self.studentId,
            "assigmentName": self.assigmentName,
            "grade": self.grade

            # do not serialize the password, its a security breach
        }

class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quarter= db.Column(db.String(20), unique=False, nullable=False)
    schoolYear = db.Column(db.String(20), unique=False, nullable=False)


    def __repr__(self):
        return '<Semester %r>' % self.schoolYear

    def serialize(self):
        return {
            "id": self.id,
            "quarter": self.quarter,
            "schoolYear": self.schoolYear,


            # do not serialize the password, its a security breach
        }


class AssignedAssigments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=True)
    subject = db.Column(db.String(10), unique=False, nullable=True)
    assigmentFile = db.Column(db.LargeBinary, unique=False, nullable=True)
    dueDate = db.Column(db.DateTime, unique=False, nullable=True)
    semesterId = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<AssignedAssigments %r>' % self.name

    def serialize(self):
        return {
            "name": self.id,
            "subject": self.subject,
            "dueDate": self.dueDate,
            "semesterId": self.semesterId

           
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
