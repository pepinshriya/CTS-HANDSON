sql
-- ==========================================================
-- Hands-On 2 : Writing SQL Queries - DML, Joins & Aggregation
-- Database : college_db
-- ==========================================================

USE college_db;

-- ==========================================================
-- Task 1 : Insert, Update and Delete Data
-- ==========================================================

-- 15. Insert Sample Data
-- (Paste the sample INSERT statements from the exercise book here)

-- 16. Insert Two Additional Students
INSERT INTO students
(first_name, last_name, email, date_of_birth, department_id, enrollment_year)
VALUES
('Mahesh', 'Kumar', 'mahesh.kumar@college.edu', '2005-05-26', 1, 2023),
('Rahul', 'Sharma', 'rahul.sharma@college.edu', '2004-10-15', 2, 2023);

-- 17. Update Grade
UPDATE enrollments
SET grade = 'B'
WHERE student_id = 5
AND course_id = 1;

-- 18. Delete Enrollments with NULL Grade
DELETE FROM enrollments
WHERE grade IS NULL;

-- 19. Verify Row Counts
SELECT COUNT(*) AS total_students
FROM students;

SELECT COUNT(*) AS total_enrollments
FROM enrollments;


-- ==========================================================
-- Task 2 : Single Table Queries
-- ==========================================================

-- 20. Students enrolled in 2022
SELECT *
FROM students
WHERE enrollment_year = 2022
ORDER BY last_name;

-- 21. Courses with more than 3 credits
SELECT *
FROM courses
WHERE credits > 3
ORDER BY credits DESC;

-- 22. Professors with salary between 80,000 and 95,000
SELECT *
FROM professors
WHERE salary BETWEEN 80000 AND 95000;

-- 23. Students whose email ends with @college.edu
SELECT *
FROM students
WHERE email LIKE '%@college.edu';

-- 24. Count students by enrollment year
SELECT enrollment_year,
       COUNT(*) AS total_students
FROM students
GROUP BY enrollment_year;


-- ==========================================================
-- Task 3 : Multi Table Joins
-- ==========================================================

-- 25. Student name with department
SELECT CONCAT(s.first_name,' ',s.last_name) AS student_name,
       d.dept_name
FROM students s
INNER JOIN departments d
ON s.department_id = d.department_id;

-- 26. Student name with enrolled course
SELECT CONCAT(s.first_name,' ',s.last_name) AS student_name,
       c.course_name
FROM enrollments e
INNER JOIN students s
ON e.student_id = s.student_id
INNER JOIN courses c
ON e.course_id = c.course_id;

-- 27. Students not enrolled in any course
SELECT CONCAT(s.first_name,' ',s.last_name) AS student_name
FROM students s
LEFT JOIN enrollments e
ON s.student_id = e.student_id
WHERE e.student_id IS NULL;

-- 28. Courses with total enrollments
SELECT c.course_name,
       COUNT(e.student_id) AS total_students
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

-- 29. Departments with professors and salary
SELECT d.dept_name,
       p.prof_name,
       p.salary
FROM departments d
LEFT JOIN professors p
ON d.department_id = p.department_id;


-- ==========================================================
-- Task 4 : Aggregations and Grouping
-- ==========================================================

-- 30. Total enrollments per course
SELECT c.course_name,
       COUNT(e.enrollment_id) AS enrollment_count
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

-- 31. Average professor salary by department
SELECT d.dept_name,
       ROUND(AVG(p.salary),2) AS average_salary
FROM departments d
LEFT JOIN professors p
ON d.department_id = p.department_id
GROUP BY d.department_id, d.dept_name;

-- 32. Departments with budget greater than 600000
SELECT *
FROM departments
WHERE budget > 600000;

-- 33. Grade distribution for CS101
SELECT e.grade,
       COUNT(*) AS total_students
FROM enrollments e
INNER JOIN courses c
ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY e.grade;

-- 34. Departments having more than 2 students
SELECT d.dept_name,
       COUNT(s.student_id) AS total_students
FROM departments d
INNER JOIN students s
ON d.department_id = s.department_id
GROUP BY d.department_id, d.dept_name
HAVING COUNT(s.student_id) > 2;
