"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db
from models import User, Teacher, Students, StudentsGrades, SubmitedAssigments

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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    studentsArray = Students.query.all()
    assigments = SubmitedAssigments.query.all()

    studentAssigments = []
    student = {}

    for students in studentsArray:
        student['Student_Name']=students.name
        for work in assigments:
             if work.studentId == students.id:
                 student[work.assigmentName] = work.grade
        studentAssigments.append(student)
        print(studentAssigments)
        student = {}
    print(studentAssigments)

    response_body = {"hello":"hello"}

    return jsonify(studentAssigments), 200


@app.route('/add', methods=['POST', 'GET'])
def handle_add():

    test = StudentsGrades(studentId=1, subject="math", gradeLevel="9", semester="q2", grade="A")
    db.session.add(test)
    db.session.commit()


    return 'test', 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
