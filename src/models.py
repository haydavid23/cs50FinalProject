from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    gradeLevel = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    TeacherId = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Student %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "name": self.lastName,
            "name": self.gradeLevel,
            "name": self.username,
            "name": self.teacherId,
            # do not serialize the password, its a security breach
        }


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    gradeLevel = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    studentId = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Student %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "name": self.lastName,
            "name": self.gradeLevel,
            "name": self.username,
            "name": self.studentId,
            # do not serialize the password, its a security breach
        }


class Assigments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, nullable=False)
    teacherId = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(25), nullable=False)
    assigmentName = db.Column(db.String(100), unique=True, nullable=False)
    classfication = db.Column(db.String(50), unique=False, nullable=False)
    dueDate = db.Column(db.DateTime, unique=False, nullable=False)
    grade = db.Column(db.String(10), unique=False, nullable=False)
    note = db.Column(db.String(50), unique=False, nullable=True)
    

    def __repr__(self):
        return '<Assigments %r>' % self.subject

    def serialize(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "studentId": self.teacherId,
            "subject": self.subject,
            "assigmentName": self.assigmentName,
            "dueDate": self.dueDate,
            "classification": self.classification,
            "grade": self.grade,
            "note": self.note,
            # do not serialize the password, its a security breach
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    gradeLevel = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    studentId = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Student %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "name": self.lastName,
            "name": self.gradeLevel,
            "name": self.username,
            "name": self.studentId,
            # do not serialize the password, its a security breach
        }
