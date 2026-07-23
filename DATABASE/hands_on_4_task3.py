"""
Hands-on Exercise 4
Task 3: Identify and Fix the N+1 Problem

Tasks:
56. Simulate the N+1 Problem
57. Fix using a JOIN query
58. Compare execution time and number of queries
59. Document the difference
"""

import mysql.connector
import time

# ==========================================================
# Database Connection
# ==========================================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vijayavarathan",
    database="college_db"
)

cursor = connection.cursor()

# ==========================================================
# Task 56 - N+1 Problem
# ==========================================================

print("=" * 70)
print("TASK 56 : N+1 QUERY PROBLEM")
print("=" * 70)

query_count = 0

start_time = time.time()

# First Query
cursor.execute("SELECT * FROM enrollments")
query_count += 1

enrollments = cursor.fetchall()

print("\nEnrollment Details\n")

for enrollment in enrollments:

    student_id = enrollment[1]

    cursor.execute(
        """
        SELECT first_name, last_name
        FROM students
        WHERE student_id = %s
        """,
        (student_id,)
    )

    student = cursor.fetchone()

    query_count += 1

    print(
        f"Enrollment ID : {enrollment[0]} | "
        f"Student : {student[0]} {student[1]} | "
        f"Course ID : {enrollment[2]}"
    )

end_time = time.time()

n_plus_one_time = end_time - start_time

print("\nQueries Executed :", query_count)
print("Execution Time   : {:.6f} seconds".format(n_plus_one_time))

# ==========================================================
# Task 57 - Fix Using JOIN
# ==========================================================

print("\n" + "=" * 70)
print("TASK 57 : FIX USING A SINGLE JOIN QUERY")
print("=" * 70)

query_count = 0

start_time = time.time()

cursor.execute("""
SELECT
    e.enrollment_id,
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
    ON s.student_id = e.student_id
JOIN courses c
    ON c.course_id = e.course_id
""")

rows = cursor.fetchall()

query_count += 1

end_time = time.time()

join_time = end_time - start_time

print("\nEnrollment Details\n")

for row in rows:
    print(
        f"Enrollment ID : {row[0]} | "
        f"Student : {row[1]} {row[2]} | "
        f"Course : {row[3]}"
    )

print("\nQueries Executed :", query_count)
print("Execution Time   : {:.6f} seconds".format(join_time))

# ==========================================================
# Task 58 - Performance Comparison
# ==========================================================

print("\n" + "=" * 70)
print("TASK 58 : PERFORMANCE COMPARISON")
print("=" * 70)

print(f"N+1 Queries Executed : {len(enrollments) + 1}")
print("JOIN Queries Executed: 1")

print("\nExecution Time")
print("------------------------------")
print("N+1 Query Time : {:.6f} seconds".format(n_plus_one_time))
print("JOIN Query Time: {:.6f} seconds".format(join_time))

print("\nDatabase Round Trips Saved :", len(enrollments))

# ==========================================================
# Task 59 - Documentation
# ==========================================================

print("\n" + "=" * 70)
print("TASK 59")
print("=" * 70)

print("""
For 10,000 enrollments:

N+1 Version
------------
1 query to fetch enrollments
+
10,000 queries to fetch student names
=
10,001 Total Queries

JOIN Version
------------
Only 1 Query

Extra Queries Issued by N+1 Version:
10,000

Conclusion:
Using a JOIN eliminates thousands of unnecessary
database round-trips and significantly improves
application performance.
""")

cursor.close()
connection.close()