from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User
from sqlalchemy import text
from .init import db

routes = Blueprint("routes", __name__)


@routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = User(username=data["username"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"})


@routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@routes.route("/student_info/<string:student_id>", methods=["GET"])
def get_student_info(student_id):
    query = text(
        """
    SELECT ID, name, dept_name, tot_cred FROM student WHERE ID = :student_id
    """
    )
    result = db.session.execute(query, {"student_id": student_id}).mappings().all()
    result = [dict(row) for row in result]
    return jsonify(result)


@routes.route("/student_lectures/<string:student_id>", methods=["GET"])
def get_student_lecture(student_id):
    query = text(
        """
    SELECT 
        course.course_id, 
        course.title AS course_title, 
        course.credits, 
        takes.grade
    FROM 
        takes
    JOIN 
        student ON takes.ID = student.ID
    JOIN 
        section ON takes.course_id = section.course_id AND takes.sec_id = section.sec_id AND takes.semester = section.semester AND takes.year = section.year
    JOIN 
        course ON section.course_id = course.course_id
    WHERE 
        student.ID = :student_id
    """
    )

    result = db.session.execute(query, {"student_id": student_id}).mappings().all()
    lecture = [dict(row) for row in result]
    return jsonify(lecture)
