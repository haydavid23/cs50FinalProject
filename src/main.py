"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_file,json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db
from models import User, Teacher, Subjects, Students,SchoolTerm, StudentsGrades, SubmitedAssignments, AssignedAssignments

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
UPLOAD_FOLDER = './src/pdf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/getGradeBookGradeBysubject', methods=['POST', 'GET'])
def handle_getGradeBookGradeBysubject():
    studentsArray = Students.query.all()
    assignments = SubmitedAssignments.query.all()

    studentAssignments = []
    student = {}

    for students in studentsArray:
        student['Student_Name']=students.name
        for work in assignments:
             if work.studentId == students.id:
                 student[work.assignmentName] = work.grade
        studentAssignments.append(student)
        print(studentAssignments)
        student = {}
    print(studentAssignments)

    response_body = {"hello":"hello"}

    return jsonify(studentAssignments), 200


@app.route('/getAssignmentsBySubject', methods=['POST', 'GET'])
def handle_assignmentsBySubject():

    subjectRequested = request.get_json()
    subject = Subjects.query.filter_by(subject="Math").first()

    assignments = AssignedAssignments.query.filter_by(subjectId=subject.id).all()

    assignmentNames = []
    
    for assignment in assignments:
        assignmentNames.append(assignment.name)

    print(assignmentNames)

    return jsonify(assignmentNames), 200

@app.route('/getAllAssignmentsList', methods=['POST', 'GET'])
def handle_getAllAssignmentsList():

    arr = []

    assignments = AssignedAssignments.query.all()
    for assignment in assignments:
        arr.append(assignment.serialize())

    return jsonify(arr), 200



@app.route('/edit', methods=['POST', 'GET'])
def handle_edit():
    assignments = AssignedAssignments.query.get(5)
    assignments.name = "mathtest3"
    db.session.commit()

    return "succcess", 200

@app.route('/saveAssignedFile', methods=['POST', 'GET'])
def handle_saveFile():

    assignment =  request.files
    form = json.loads(request.form['form'])
    print(form['subject'])
    print(assignment)

    f = assignment['file']
    path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    f.save(path)
    print(path)
   

    insertAssignment = AssignedAssignments(name=form["assignmentName"], 
    subject=form['subject'], note=form['note'], assignmentFile=path)

    db.session.add(insertAssignment)
    db.session.commit()

    return jsonify("SUCCESS"), 200


@app.route('/getAllSubjects', methods=['GET'])
def handle_getAllSubjects():

    subjects = Subjects.query.all()

    jsonSubjects = []

    for subject in subjects:
        jsonSubjects.append(subject.serialize())

    return jsonify(jsonSubjects)


@app.route('/getAssignmentPdf', methods=['POST', 'GET'])
def handle_returnAssignmentPdf():

    filePath = request.get_json()
    print(filePath)

    return send_file('pdf/samplePdf.pdf')


@app.route('/setSchoolTerm', methods=['POST', 'GET'])
def handle_setSchoolTerm():

    currentTerm = SchoolTerm.query.filter_by(current = True).first()
    schoolTerm = request.get_json()

    if schoolTerm["schoolYear"] == "" or schoolTerm["quarter"] == "":
        return jsonify("Please provide valid values")
    else:
        if currentTerm == None:

            setTerm = SchoolTerm(schoolYear=schoolTerm["schoolYear"],quarter=schoolTerm['quarter'], current=True)
            db.session.add(setTerm)
            db.session.commit()
 
            return jsonify("Success"), 200
        else:
            currentTerm.current = False
            db.session.commit()

            setTerm = SchoolTerm(schoolYear=schoolTerm["schoolYear"],quarter=schoolTerm['quarter'], current=True)
            db.session.add(setTerm)
            db.session.commit()

            return jsonify("Success"), 200
 
            


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
