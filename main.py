from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Numeric, ForeignKey


app = Flask(__name__)
api = Api(app)


# Указываете путь к вашей базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///univdb-sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CourseModel(db.Model):
    __tablename__ = "course"
    course_id = Column(String(8), primary_key=True)
    title = Column(String(50))
    dept_name = Column(String(20))
    credits = Column(Numeric(2,0))  # SQLAlchemy doesn't support check constraints directly on columns.

    def __repr__(self):
        return 'course_id={}, title={}, dept_name={}, credits={}'.format(self.course_id, self.title, self.dept_name, self.credits)



course_field = {
    'course_id': fields.String,
    'title': fields.String,
    'dept_name': fields.String,
    'credits': fields.Integer
}


class Course(Resource):
    @marshal_with(course_field)
    def get(self, course_id):
        course = CourseModel.query.get(course_id)
        if not course:
            abort(404, message="Course {} doesn't exist".format(course_id))
        return course

    @marshal_with(course_field)
    def delete(self, course_id):
        course = CourseModel.query.get(course_id)
        if not course:
            abort(404, message="Course {} doesn't exist".format(course_id))
        db.session.delete(course)
        db.session.commit()
        return '', 204
    
    @marshal_with(course_field)
    def post(self, course_id):
        parser = reqparse.RequestParser()
        parser.add_argument('course_id', type=str, required=True)
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('dept_name', type=str, required=True)
        parser.add_argument('credits', type=int, required=True)
        data = parser.parse_args()

        existing_course = CourseModel.query.filter_by(course_id=course_id).first()
        if existing_course:
            abort(400, message=f"Course with id {course_id} already exists")

        course = CourseModel(course_id=course_id,
                             title=data['title'],
                             dept_name=data['dept_name'],
                             credits=data['credits'])
        db.session.add(course)
        db.session.commit()
        return course, 201

    @marshal_with(course_field)
    def put(self, course_id):
        parser = reqparse.RequestParser()
        parser.add_argument('course_id', type=str)
        parser.add_argument('title', type=str)
        parser.add_argument('dept_name', type=str)
        parser.add_argument('credits', type=int)
        data = parser.parse_args()

        course = CourseModel.query.get(course_id)
        if not course:
            abort(404, message="Course {} doesn't exist".format(course_id))
        for key, value in data.items():
            setattr(course, key, value)
        db.session.commit()
        return course, 200

api.add_resource(Course, '/courses/<string:course_id>')

class AllCourses(Resource):
    @marshal_with(course_field)
    def get(self):
        courses = CourseModel.query.all()
        if not courses:
            print("No courses found")
            abort(404, message="No courses found")
        for course in courses:
            print(course)
        return courses

api.add_resource(AllCourses, '/courses')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=8000, host="localhost")


