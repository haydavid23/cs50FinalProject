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
from sqlalchemy import exc,desc
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
SUBMITTED_UPLOAD_FOLDER = './src/submittedAssignments'
app.config['SUBMITTED_UPLOAD_FOLDER'] = SUBMITTED_UPLOAD_FOLDER


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
            for x in range(6):
                studentGrade = StudentsClassGrades(studentId=studentId.id,subjectId=x+1,schoolTermId=termId)
                db.session.add(studentGrade)
                db.session.commit()

        except:
            db.session.rollback()
            return jsonify("Unexpected database error")
    

    
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


@app.route('/getPdfForGradeBook',methods=['POST', 'GET'])
def getPdfForGradeBook():

    form= request.get_json()
    studentPdfs = []
    studentAssignment = {}

    studentPdfFile = SubmitedAssignments.query.filter_by(subjectId=form['subjectId'],schoolTermId=form['schoolTermId'], studentId=form['studentId']).all()


    assignmentsArray = AssignedAssignments.query.filter_by(subjectId=form['subjectId'],schoolTermId=form['schoolTermId']).all()


    for assignment in assignmentsArray:
        studentAssignment['assignmentName']=assignment.assignmentName
        studentAssignment['submittedFile']=None
        studentAssignment['submitttedDate']=None
        for pdf in studentPdfFile:
            if pdf.assignmentName == assignment.assignmentName:
                studentAssignment['assignmentName']=assignment.assignmentName
                studentAssignment['submittedFile']=pdf.submittedFile
                studentAssignment['submitttedDate']=pdf.submitedDate
          
        studentPdfs.append(studentAssignment)
        studentAssignment  = {}
              
        
    print(studentPdfs)
    return  jsonify(studentPdfs),200



@app.route('/getGradeBookGradeBysubject', methods=['POST', 'GET'])
def handle_getGradeBookGradeBysubject():
    form= request.get_json()
    print(form)
    subjectId = form['subjectId']
    schoolTermId = form['schoolTermId']


    studentsArray = Students.query.all()
    submitted_assignments = SubmitedAssignments.query.filter_by(subjectId=subjectId,schoolTermId=schoolTermId).all()
    classGrade = StudentsClassGrades.query.filter_by(subjectId=subjectId, schoolTermId=schoolTermId).all()
    studentAssignments = []
    student = {}


    for students in studentsArray:
        student['Student Name']=students.name
        student['id'] = students.id
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
    subjectId = subjectRequested['subjectId']
    schoolTermId = subjectRequested['schoolTermId']


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
        print(form)

        insertAssignment = AssignedAssignments(assignmentName=form['assignmentName'],subjectId=form['subjectId'], note=form['note'], assignmentFile=path, schoolTermId=form['schoolTermId'],dueDate=date_time_obj, submittable=form["submittable"])
        db.session.add(insertAssignment)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify("Error! Please provide all required data"),500
       

    return jsonify("Assignment Added Successfully!"), 200


@app.route('/saveSubmittedAssignmentFile', methods=['POST', 'GET'])
def handle_saveSubmittedAssignmentFile():

    assignment =  request.files
    form = json.loads(request.form['form'])
    print(form)
    

    if assignment:
        try:
            f = assignment['file']
            path = os.path.join(app.config['SUBMITTED_UPLOAD_FOLDER'], f.filename)
            f.save(path)
            
            submittedAssignment = SubmitedAssignments(studentId=form['studentId'],subjectId=form['subjectId'],schoolTermId=form['schoolTermid'],assignmentName=form['assignmentName'],submittedFile=path)
            db.session.add(submittedAssignment)
            db.session.commit()

            return jsonify("Assignment Submitted!"),200
        except:
            return jsonify("Failed to save PDF file"),500

    return jsonify("Empty assignment. Please submit an assignment"),500


@app.route('/getAllSubjects', methods=['GET'])
def handle_getAllSubjects():

    subjects = Subjects.query.all()

    jsonSubjects = []

    for subject in subjects:
        jsonSubjects.append(subject.serialize())

    return jsonify(jsonSubjects)


@app.route('/updateGradeBook', methods=['POST','GET'])
def handle_updateGradeBook():

    form = request.get_json()

    
    try:
    #updates submitted assignment grade.
        for student in form:
            print(student)
            for assignment,grade in student["assignments"].items():
            
                submittedAssignment = SubmitedAssignments.query.filter_by(studentId=student["id"],subjectId=student['subjectId'], 
                schoolTermId=student["schoolTermId"], assignmentName=assignment).first()
                if submittedAssignment == None and grade !=0:
                    return jsonify("Make sure " + assignment + " for " + student['Student Name'] +  " is submitted before grading it")
                
                #checking grade is valid
                try:
                    if grade <0 or grade > 100:
                        return jsonify("Invalid grade number") 
                except:
                    return jsonify("Grade must be a number") 

                if submittedAssignment != None:
                    submittedAssignment.grade = grade
                    db.session.commit()

                classGrade = StudentsClassGrades.query.filter_by(studentId=student["id"],subjectId=student["subjectId"],schoolTermId=student["schoolTermId"]).first()
                classGrade.gradeAvg = student["Avg Grade"]
                classGrade.gradeLetter = student["Grade Letter"]

    except IntegrityError as e:
        db.session.rollback()
        return jsonify("Error saving grade. Please try again")



            # {'id': 13, 'Student Name': 'David', 'Avg Grade': 16.67, 'Grade Letter': 'F', 
            # 'assignments': {'hw1': 50, 'hw2': 0, 'test1': 0}, 'subjectId': 1, 'schoolTermId': 213}


  
    return jsonify("Grade Book Saved Succesfully!")


@app.route('/getAssignmentPdf', methods=['POST', 'GET'])
def handle_returnAssignmentPdf():
   
    try:
        filePath = request.get_json()
        newPath = filePath["path"].replace("./src/","")
        return send_file(newPath)

    except:
        return jsonify("Error! Could not retrieve assignment File")

 

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


@app.route('/getAssignmentsForStudent', methods=['POST', 'GET'])
def handle_getAssignmentsForStudents():
    
    form=request.get_json()
    subjectId = form['subjectId']
    schoolTermId = form['schoolTermId']
    studentId= form['studentId']

    studentAssignments = []
    assign = None
  

    assignedAssignments = AssignedAssignments.query.filter_by(subjectId = subjectId, schoolTermId=schoolTermId).order_by(desc(AssignedAssignments.assignedDate)).all()
    

    submittedAssignments = SubmitedAssignments.query.filter_by(subjectId = subjectId, schoolTermId=schoolTermId,studentId=studentId).all()

    for assignment in assignedAssignments:
        assign = {**assignment.serialize()}
        for submitted in submittedAssignments:
            if assignment.assignmentName == submitted.assignmentName:
                assign = {**assignment.serialize(),**submitted.serialize()}
        studentAssignments.append(assign)
        
        

   
    return jsonify(studentAssignments), 200


@app.route('/loginStudent', methods=['POST'])
def loginStudent():

    form=request.get_json()
    student= None

    #checks required info submited
    for key in form:
        if form[key] == "" or form[key] == None:
            return jsonify("Please provide all required information")
    
    student= Students.query.filter_by(username=form["username"], password=form["password"]).first()
    
    if student != None:
        print(student.serialize())
        return jsonify(student.serialize())
    
    else:
        return jsonify("Wrong username and/or password for the selected user type")



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
