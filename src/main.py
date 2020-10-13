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
from sqlalchemy.orm.util import join as join
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
    print(form)

    #checking all required data is submited
    for key in form:
        if form[key] == "" or form[key]==None:
            return jsonify("Please submit all required information")
    
    if form["userType"] == "student":
        usernames = Students.query.all()
    elif form["userType"] == "teacher":
        usernames = Teachers.query.all()

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

    elif form["userType"] == "teacher":
        try:
            # insert new teacher in teacher table
            newTeacher = Teachers(name=form["name"],lastName=form["lastName"],username=form["userName"], password=form["password"])
            db.session.add(newTeacher)
            db.session.commit()
        
        except:
            db.session.rollback()
            return jsonify("Unexpected database error")

    username = None
    if form["userType"]=="student":
        username = Students.query.filter_by(username=form["username"]).first()
    elif form['userType'] == 'teacher':
        username = Teachers.query.filter_by(username=form["userName"]).first()
    
    return jsonify(username.serialize())
    # return jsonify("user successfully registered")


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
    elif form['userType'] == 'admin':
         username = Teachers.query.filter_by(username=form["username"], password=form["password"]).first()

    
    if username != None:
        return jsonify(username.serialize())
    
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
              
        

    return  jsonify(studentPdfs),200



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



@app.route('/deleteAssignedAssignment', methods=['POST', 'GET'])
def handle_deleteAssignedAssignment():

    form = request.get_json()
    studentIds = []
    assignedAssignmentsTotal = None

    students = Students.query.all()

    # assignedAssignmentsTotal=AssignedAssignments.query.filter_by(subjectId=form['subjectId'],schoolTermId=form["schoolTermId"]).count()
  

    for student in students:
        studentIds.append(student.serialize()["id"])


    try:
        # assignedAssignments = AssignedAssignments.query.filter_by(id=form['assignmentId']).first()
        assignedAssignments = AssignedAssignments.query.filter_by(id=form['assignmentId']).delete()
        subAssignments = SubmitedAssignments.query.all()



        submittedAssignments = SubmitedAssignments.query.filter_by(subjectId=form['subjectId'], assignmentName =form['assignmentName']).delete()
        # db.session.delete(assignedAssignments)

        avgGrade = 0
        db.session.commit()

        assignedAssignmentsTotal=AssignedAssignments.query.filter_by(subjectId=form['subjectId'],schoolTermId=form["schoolTermId"]).count()

        gradeLetter = None
    
        for studentId in studentIds:
            studentAssignments = SubmitedAssignments.query.filter_by(subjectId=form['subjectId'], studentId=studentId).all()
            studentClassGrades = StudentsClassGrades.query.filter_by(studentId=studentId).first()
        
            for assignment in studentAssignments:
                print(assignment.serialize())
                avgGrade += assignment.serialize()["grade"]
                
            print(avgGrade)
            avgGrade = avgGrade / assignedAssignmentsTotal
            studentClassGrades.gradeAvg = avgGrade
            
            print(avgGrade)

            def gradeLetter(avgGrade):
                if avgGrade >=0 and avgGrade < 60:
                    return "F"
                elif avgGrade >=60 and avgGrade <70:
                    return "D"
                elif avgGrade >=70 and avgGrade <80:
                    return "C"
                elif avgGrade >=80 and avgGrade <90:
                    return "B"
                elif avgGrade >=90 and avgGrade <100:
                    return "A"
                else:
                    return "N/A"

            studentClassGrades.gradeLetter = gradeLetter(avgGrade)
            db.session.commit()
            avgGrade = 0


        return jsonify("Assignment Deleted"), 200
    except:
        db.session.rollback()
        return jsonify("Error! Unable to delete assignment."),500
        
    #updates student grades avg
    # try:
    #     avgGrade = 0
    #     gradeLetter = None
    
    #     for studentId in studentIds:
    #         studentAssignments = SubmitedAssignments.query.filter_by(subjectId=form['subjectId'], studentId=studentId).all()
    #         studentClassGrades = StudentsClassGrades.query.filter_by(studentId=studentId).first()
        
    #         for assignment in studentAssignments:
    #             avgGrade += assignment.serialize()["grade"]
                
  
    #         avgGrade = avgGrade / assignedAssignmentsTotal
    #         studentClassGrades.gradeAvg = avgGrade
            
    #         print(avgGrade)

    #         def gradeLetter(avgGrade):
    #             if avgGrade >=0 and avgGrade < 60:
    #                 return "F"
    #             elif avgGrade >=60 and avgGrade <70:
    #                 return "D"
    #             elif avgGrade >=70 and avgGrade <80:
    #                 return "C"
    #             elif avgGrade >=80 and avgGrade <90:
    #                 return "B"
    #             elif avgGrade >=90 and avgGrade <100:
    #                 return "A"
    #             else:
    #                 return "N/A"

    #         studentClassGrades.gradeLetter = gradeLetter(avgGrade)
    #         db.session.commit()
    #         avgGrade = 0
               
     


    # except:
    #     jsonify("Error"), 500
    
    return jsonify("Avg Grade Updated"), 200




@app.route('/getStudentClassGrades', methods=['POST', 'GET'])
def handle_getStudentClassGrades():

    form = request.get_json()
  
    studentId = form['studentid']
    schoolTermId = form['currentTermId']

    # studentGrades = StudentsClassGrades.query.filter_by(studentId=studentId,schoolTermId=schoolTermId).all()
    
    studentGrades = db.session.query(Subjects,StudentsClassGrades).join(
    StudentsClassGrades, Subjects.id == StudentsClassGrades.subjectId).filter_by(studentId=studentId,schoolTermId=schoolTermId).all()

  
    gradesArr = []

    for classGrade in studentGrades:
        gradesArr.append({**classGrade[1].serialize(),**classGrade[0].serialize()})
        
    return jsonify(gradesArr), 200




@app.route('/getAssignedAssignmentsBySubject', methods=['POST', 'GET'])
def handle_assignmentsBySubject():

    subjectRequested = request.get_json()
    subjectId = subjectRequested['subjectId']
    schoolTermId = subjectRequested['schoolTermId']


    assignments = AssignedAssignments.query.filter_by(subjectId=subjectId,schoolTermId=schoolTermId).all()


    assignmentLst = []
    
    for assignment in assignments:
        assignmentLst.append(assignment.serialize())



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


        insertAssignment = AssignedAssignments(assignmentName=form['assignmentName'],subjectId=form['subjectId'], note=form['note'], assignmentFile=path, schoolTermId=form['schoolTermId'],dueDate=date_time_obj, submittable=form["submittable"])
        db.session.add(insertAssignment)
        db.session.commit()

        #logic to adjust avg grade
        students = Students.query.all()

    #loop each student, then each submitted assignment and calculate avg grade.
        # for student in students:
        #     submittedAssignments = submitted_assignments.query.filter_by().all()

    except:
        db.session.rollback()
        return jsonify("Error! Please provide all required data"),500
       

    return jsonify("Assignment Added Successfully!"), 200


@app.route('/saveSubmittedAssignmentFile', methods=['POST', 'GET'])
def handle_saveSubmittedAssignmentFile():

    assignment =  request.files
    form = json.loads(request.form['form'])

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
            for assignment,grade in student["assignments"].items():
                submittedAssignment = SubmitedAssignments.query.filter_by(studentId=student["id"],subjectId=student['subjectId'], 
                schoolTermId=student["schoolTermId"], assignmentName=assignment).first()

                # if submittedAssignment == None and grade !=None or submittedAssignment == None  :
                #     return jsonify("Make sure " + assignment + " for " + student['Student Name'] +  " is submitted before grading it")
                
                if submittedAssignment is not None:
                    if grade is not None:
                        if grade <0 or grade > 100:
                            return jsonify("Grade must be a number")
                    submittedAssignment.grade = grade
                    db.session.commit()

     
                classGrade = StudentsClassGrades.query.filter_by(studentId=student["id"],subjectId=student["subjectId"],schoolTermId=student["schoolTermId"]).first()
                classGrade.gradeAvg = student["Avg Grade"]
                classGrade.gradeLetter = student["Grade Letter"]
                db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return jsonify("Error saving grade. Please try again")


  
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

            try:
                #adds school term to students class grades table     
                students = Students.query.all()
                currentTerm = SchoolTerm.query.filter_by(current = True).first()
                term = currentTerm.serialize()

                for student in students:
                    studentId = student.serialize()
                    for x in range(6):
                        studentGrade = StudentsClassGrades(studentId=studentId["id"],subjectId=x+1,schoolTermId=term["id"])
                        db.session.add(studentGrade)
                        db.session.commit()

            
            except:
                db.session.rollback()
                return jsonify("Error!")

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


# @app.route('/loginStudent', methods=['POST'])
# def loginStudent():

#     form=request.get_json()
#     student= None

#     #checks required info submited
#     for key in form:
#         if form[key] == "" or form[key] == None:
#             return jsonify("Please provide all required information")
    
#     # student= Students.query.filter_by(username=form["username"], password=form["password"]).first()
        
#     if form["userType"]=="student":
#         username = Students.query.filter_by(username=form["username"], password=form["password"]).first()
#     elif form[userType] == 'admin':
#          username = Teachers.query.filter_by(username=form["userName"], password=form["password"]).first()
    
#     if username != None:
#         return jsonify(username.serialize())
    
#     else:
#         return jsonify("Wrong username and/or password for the selected user type")



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
