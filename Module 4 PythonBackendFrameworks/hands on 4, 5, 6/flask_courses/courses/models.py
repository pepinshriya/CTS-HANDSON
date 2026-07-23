from extension import db


class Department(db.Model):
    __tablename__ = "department"

    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)

    courses = db.relationship(
        "Course",
        back_populates="department"
    )

    def to_dict(self):
        return {
            "department_id": self.department_id,
            "name": self.name,
            "head_of_dept": self.head_of_dept,
            "budget": self.budget
        }


class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("department.department_id"),
        nullable=False
    )

    department = db.relationship(
        "Department",
        back_populates="courses"
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course"
    )

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits,
            "department_id": self.department_id
        }


class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer, nullable=False)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("department.department_id"),
        nullable=False
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student"
    )

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "enrollment_year": self.enrollment_year,
            "department_id": self.department_id
        }


class Enrollment(db.Model):
    __tablename__ = "enrollment"

    enrollment_id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.student_id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.course_id"),
        nullable=False
    )

    enrollment_date = db.Column(db.Date, nullable=False)
    grade = db.Column(db.String(10), nullable=True)

    student = db.relationship(
        "Student",
        back_populates="enrollments"
    )

    course = db.relationship(
        "Course",
        back_populates="enrollments"
    )

    def to_dict(self):
        return {
            "enrollment_id": self.enrollment_id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "enrollment_date": str(self.enrollment_date),
            "grade": self.grade
        }