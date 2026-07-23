

"""
==========================================================
Hands-On 6 - Task 3
Identify and Fix the N+1 Problem

Without joinedload():
---------------------
1 query loads all enrollments.
Each enrollment then executes separate
queries to fetch Student and Course.

Total Queries:
1 + N + N

With joinedload():
---------------------
SQLAlchemy performs JOINs and retrieves
Enrollment, Student and Course together.

Total Queries:
1

For 10,000 enrollments:

Without joinedload()
≈ 20,001 SQL Queries

With joinedload()
1 SQL Query

joinedload() eliminates the N+1 problem
and greatly improves application performance.
==========================================================
"""

from sqlalchemy.orm import sessionmaker, joinedload
from models import engine, Enrollment

# -----------------------------------------
# Create Session
# -----------------------------------------

Session = sessionmaker(bind=engine)
session = Session()

# =========================================
# WITHOUT joinedload()
# =========================================

print("=" * 60)
print("WITHOUT joinedload()")
print("=" * 60)

enrollments = session.query(Enrollment).all()

print("\nEnrollment Details:\n")

for enrollment in enrollments:

    print(
        f"Enrollment ID : {enrollment.enrollment_id}"
    )

    print(
        f"Student       : {enrollment.student.first_name} {enrollment.student.last_name}"
    )

    print(
        f"Course        : {enrollment.course.course_name}"
    )

    print(
        f"Grade         : {enrollment.grade}"
    )

    print("-" * 40)

print("\n")
print("=" * 60)
print("Observe the SQL statements printed above.")
print("Multiple SELECT statements are executed.")
print("=" * 60)

# =========================================
# WITH joinedload()
# =========================================

print("\n")
print("=" * 60)
print("WITH joinedload()")
print("=" * 60)

enrollments = (
    session.query(Enrollment)
    .options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    )
    .all()
)

print("\nEnrollment Details:\n")

for enrollment in enrollments:

    print(
        f"Enrollment ID : {enrollment.enrollment_id}"
    )

    print(
        f"Student       : {enrollment.student.first_name} {enrollment.student.last_name}"
    )

    print(
        f"Course        : {enrollment.course.course_name}"
    )

    print(
        f"Grade         : {enrollment.grade}"
    )

    print("-" * 40)

print("\n")
print("=" * 60)
print("Only one SQL query is executed.")
print("joinedload() solved the N+1 problem.")
print("=" * 60)

session.close()

print("\nProgram Executed Successfully.")