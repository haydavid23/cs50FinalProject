"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import datetime
from flask import Flask, request, jsonify, url_for, send_file,json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from models import User, Teachers, Subjects, Students,SchoolTerm, StudentsClassGrades, SubmitedAssignments, AssignedAssignments

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
UPLOAD_FOLDER = './src/assignedAssignments'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/test')
def test():
    
    studentsArray = Students.query.all()
    submitted_assignments = SubmitedAssignments.query.filter_by(schoolTermId=210, subjectId=1).all()
    print(submitted_assignments)
    studentAssignments = []
    student = {}

    for students in studentsArray:
        student['Student_Name']=students.name
        for work in submitted_assignments:
             if work.studentId == students.id:
                 student[work.assignmentName] = work.grade
        studentAssignments.append(student)
   
        student = {}

    return jsonify(studentAssignments), 200

    # submited = SubmitedAssignments(studentId=2,subjectId=1, assignmentName="hw", schoolTermId=210)
    # db.session.add(submited)
    # db.session.commit()
    
    return "inserted"

@app.route('/registerUser',methods=['POST', 'GET'])
def registerUser():
    form=request.get_json()
    usernames = None

    #checking all required data is submited
    for key in form:
        if form[key] == "" or form[key]==None:
            return jsonify("Please submit all required information")
    
    if form["userType"] == "student":
        usernames = Students.query.all()
    else:
        usernames = Teachers.all()

    #checking if username already exist
    for username in usernames:
        if form["username"] == username.username:
            return jsonify("Username already Exist")

    #student username insert
    if form["userType"] == "student":
        try:

            #gets current school term id
            schoolTermId = SchoolTerm.query.filter_by(current=True).first()
            termId = schoolTermId.id
            print(termId)

            # insert student in student table
            newStudent = Students(name=form["name"],lastName=form["lastName"],username=form["username"], password=form["password"])
            db.session.add(newStudent)
            db.session.commit()

            #add student to student grade table
            studentId = Students.query.filter_by(username=form["username"]).first()
            print(studentId.id)
            for x in range(6):
                studentGrade = StudentsClassGrades(studentId=studentId.id,subjectId=x+1,schoolTermId=termId)
                db.session.add(studentGrade)
                db.session.commit()

        except:
            db.session.rollback()
            return jsonify("Unexpected database error")
    
    #adds student to student class grade table
    # if form["userType"] == "student":
    #     student = Students(name=form["name"],lastName=form["lastName"],username=form["username"], password=form["password"])
    #     db.session.add(student)
    #     db.session.commit()
    
    return jsonify("user successfully registered")


@app.route('/loginUser',methods=['POST', 'GET'])
def loginUser():
    form=request.get_json()
    username= None

    #checks required info submited
    for key in form:
        if form[key] == "" or form[key] == None:
            return jsonify("Please provide all required information")
    
    if form["userType"]=="student":
        username = Students.query.filter_by(username=form["username"], password=form["password"]).first()
    else:
         username = Teachers.query.filter_by(username=form["username"], password=form["password"]).first()

    
    if username != None:
        return jsonify("Login success")
    
    else:
        return jsonify("Wrong username and/or password for the selected user type")



@app.route('/getGradeBookGradeBysubject', methods=['POST', 'GET'])
def handle_getGradeBookGradeBysubject():
    form= request.get_json()
    subjectId = form['subjectId']
    schoolTermId = form['schoolTermId']


    studentsArray = Students.query.all()
    submitted_assignments = SubmitedAssignments.query.filter_by(subjectId=subjectId,schoolTermId=schoolTermId).all()
    classGrade = StudentsClassGrades.query.filter_by(subjectId=subjectId, schoolTermId=schoolTermId).all()
    studentAssignments = []
    student = {}


    for students in studentsArray:
        student['Student Name']=students.name
        for work in submitted_assignments:
            if work.studentId == students.id:
                 student[work.assignmentName] = work.grade       
        for grade in classGrade:
  
            if grade.studentId == students.id:
                student["Avg Grade"] = grade.gradeAvg
                student["Grade Letter"]= grade.gradeLetter
        studentAssignments.append(student)

   
        student = {}

    return jsonify(studentAssignments), 200


@app.route('/getAssignedAssignmentsBySubject', methods=['POST', 'GET'])
def handle_assignmentsBySubject():

    subjectRequested = request.get_json()
    print(subjectRequested)
    subjectId = subjectRequested['subjectId']
    schoolTermId = subjectRequested['schoolTermId']
    print(schoolTermId)

    assignments = AssignedAssignments.query.filter_by(subjectId=subjectId,schoolTermId=schoolTermId).all()


    assignmentLst = []
    
    for assignment in assignments:
        assignmentLst.append(assignment.serialize())

    print(assignmentLst)

    return jsonify(assignmentLst), 200


@app.route('/getAllAssignedAssignments', methods=['POST', 'GET'])
def handle_getAllAssignments():

    arr = []

    assignments = AssignedAssignments.query.all()
    for assignment in assignments:
        arr.append(assignment.serialize())

    return jsonify(arr), 200



@app.route('/saveAssignedAssignmentFile', methods=['POST', 'GET'])
def handle_saveAssignedAssignmentFile():

    assignment =  request.files
    form = json.loads(request.form['form'])

 
    #checking if date exist
    if form["dueDate"] != "Invalid Date":
        #need to check if date is correct format once received
        date_time_str = form["dueDate"]
        date_time_obj = datetime.datetime.strptime(date_time_str, '%m/%d/%Y').date()
    else:
        date_time_obj = None
   
   #checking if file exist
    if assignment:
        try:
            f = assignment['file']
            path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(path)
        except:
            return jsonify("Failed to save PDF file"),500
    else:
        path = None
    
    try:
        print(form['schoolTermId'])

        insertAssignment = AssignedAssignments(name=form['assignmentName'],subjectId=form['subjectId'], note=form['note'], assignmentFile=path, schoolTermId=form['schoolTermId'],dueDate=date_time_obj, submittable=form["submittable"])
        db.session.add(insertAssignment)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify("Error! Please provide all required data"),500
       

    return jsonify("Assignment Added Successfully!"), 200


@app.route('/getAllSubjects', methods=['GET'])
def handle_getAllSubjects():

    subjects = Subjects.query.all()

    jsonSubjects = []

    for subject in subjects:
        jsonSubjects.append(subject.serialize())

    return jsonify(jsonSubjects)


@app.route('/getAssignedAssignmentPdf', methods=['POST', 'GET'])
def handle_returnAssignedAssignmentPdf():

    try:
        filePath = request.get_json()

        newPath = filePath["path"].replace("./src/","")

    except:
        return jsonify("Error! Could not retrieve assignment File")

    return send_file(newPath)

  


@app.route('/setSchoolTerm', methods=['POST', 'GET'])
def handle_setSchoolTerm():

    currentTerm = SchoolTerm.query.filter_by(current = True).first()
    schoolTerm = request.get_json()

    if schoolTerm['schoolYear'] == "" or schoolTerm["quarter"] == "":
        return jsonify("Please provide valid values")
    else:
        if currentTerm == None:
                setTerm = SchoolTerm(schoolYear=schoolTerm["schoolYear"],quarter=schoolTerm['quarter'], current=True)
                db.session.add(setTerm)
                db.session.commit()
                
                #returns added school term
                currentTerm = SchoolTerm.query.filter_by(current = True).first()
                term = currentTerm.serialize()
                return jsonify(term),200
         
        else:
            currentTerm.current = False

            try:
                setTerm = SchoolTerm(schoolYear=schoolTerm["schoolYear"],quarter=schoolTerm['quarter'], current=True)
                db.session.add(setTerm)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                return jsonify("Error! Duplicate Entry")

            currentTerm = SchoolTerm.query.filter_by(current = True).first()
            term = currentTerm.serialize()
            return jsonify(term),200
    
    

@app.route('/getCurrentSchoolTerm', methods=['POST', 'GET'])
def handle_getCurrentSchoolTerm():

        currentTerm = SchoolTerm.query.filter_by(current = True).first()

        if currentTerm == None:
            return jsonify("No active school year")
        else:
            term = currentTerm.serialize()
            return jsonify(term), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
