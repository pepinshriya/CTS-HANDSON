from datetime import date

from sqlalchemy.orm import sessionmaker

from models import (
    engine,
    Department,
    Student,
    Course,
    Enrollment
)

# -----------------------------------------------------
# Create Session
# -----------------------------------------------------

Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------------------------------
# INSERT Departments
# -----------------------------------------------------

departments = [
    Department(
        dept_name="Computer Science",
        head_of_dept="Dr. Ramesh Kumar",
        budget=850000
    ),
    Department(
        dept_name="Electronics",
        head_of_dept="Dr. Priya Nair",
        budget=620000
    ),
    Department(
        dept_name="Mechanical",
        head_of_dept="Dr. Suresh Iyer",
        budget=540000
    )
]

session.add_all(departments)
session.commit()

print("Departments Inserted Successfully")

# -----------------------------------------------------
# INSERT Students
# -----------------------------------------------------

students = [

    Student(
        first_name="Mahesh",
        last_name="K",
        email="mahesh@gmail.com",
        date_of_birth=date(2005, 5, 26),
        enrollment_year=2022,
        department_id=1
    ),

    Student(
        first_name="Rahul",
        last_name="Kumar",
        email="rahul@gmail.com",
        date_of_birth=date(2004, 1, 15),
        enrollment_year=2022,
        department_id=1
    ),

    Student(
        first_name="Priya",
        last_name="Sharma",
        email="priya@gmail.com",
        date_of_birth=date(2003, 8, 12),
        enrollment_year=2023,
        department_id=2
    ),

    Student(
        first_name="Anjali",
        last_name="Rao",
        email="anjali@gmail.com",
        date_of_birth=date(2004, 7, 5),
        enrollment_year=2023,
        department_id=3
    ),

    Student(
        first_name="Vikram",
        last_name="Das",
        email="vikram@gmail.com",
        date_of_birth=date(2002, 11, 10),
        enrollment_year=2022,
        department_id=1
    )

]

session.add_all(students)
session.commit()

print("Students Inserted Successfully")

# -----------------------------------------------------
# INSERT Courses
# -----------------------------------------------------

courses = [

    Course(
        course_name="Database Management Systems",
        course_code="CS102",
        credits=3,
        department_id=1
    ),

    Course(
        course_name="Data Structures",
        course_code="CS101",
        credits=4,
        department_id=1
    ),

    Course(
        course_name="Circuit Theory",
        course_code="EC101",
        credits=3,
        department_id=2
    )

]

session.add_all(courses)
session.commit()

print("Courses Inserted Successfully")

# -----------------------------------------------------
# INSERT Enrollments
# -----------------------------------------------------

enrollments = [

    Enrollment(
        student_id=1,
        course_id=1,
        enrollment_date=date(2022, 7, 1),
        grade="A"
    ),

    Enrollment(
        student_id=1,
        course_id=2,
        enrollment_date=date(2022, 7, 1),
        grade="B"
    ),

    Enrollment(
        student_id=2,
        course_id=1,
        enrollment_date=date(2022, 7, 1),
        grade="A"
    ),

    Enrollment(
        student_id=3,
        course_id=3,
        enrollment_date=date(2023, 7, 1),
        grade="B"
    )

]

session.add_all(enrollments)
session.commit()

print("Enrollments Inserted Successfully")

# -----------------------------------------------------
# READ
# Students in Computer Science Department
# -----------------------------------------------------

print("\nStudents in Computer Science Department\n")

students = (
    session.query(Student)
    .join(Department)
    .filter(Department.dept_name == "Computer Science")
    .all()
)

for student in students:
    print(
        student.student_id,
        student.first_name,
        student.last_name
    )

# -----------------------------------------------------
# READ
# Enrollment with Student and Course
# -----------------------------------------------------

print("\nEnrollment Details\n")

enrollments = session.query(Enrollment).all()

for enrollment in enrollments:

    print(
        enrollment.student.first_name,
        "->",
        enrollment.course.course_name,
        "| Grade:",
        enrollment.grade
    )

# -----------------------------------------------------
# UPDATE
# -----------------------------------------------------

student = (
    session.query(Student)
    .filter(Student.email == "mahesh@gmail.com")
    .first()
)

if student:

    student.enrollment_year = 2024

    session.commit()

    print("\nStudent Updated Successfully")

# -----------------------------------------------------
# DELETE
# -----------------------------------------------------

enrollment = (
    session.query(Enrollment)
    .filter(Enrollment.enrollment_id == 4)
    .first()
)

if enrollment:

    session.delete(enrollment)

    session.commit()

    print("Enrollment Deleted Successfully")

# -----------------------------------------------------
# VERIFY
# -----------------------------------------------------

print("\nRemaining Enrollments\n")

all_enrollments = session.query(Enrollment).all()

for enrollment in all_enrollments:

    print(
        enrollment.enrollment_id,
        enrollment.student.first_name,
        enrollment.course.course_name
    )

session.close()

print("\nCRUD Operations Completed Successfully")