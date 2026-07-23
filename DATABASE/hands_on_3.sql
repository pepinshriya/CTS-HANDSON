-- Hands-On 3 : Advanced SQL
-- Subqueries, Views, Stored Procedures & Transactions

USE college_db;

-- ==========================================================
-- Task 1 : Subqueries
-- ==========================================================

-- 35. Students enrolled in more courses than the average

SELECT s.student_id,
       CONCAT(s.first_name,' ',s.last_name) AS student_name
FROM students s
JOIN enrollments e
ON s.student_id = e.student_id

GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(*) >
(
    SELECT AVG(course_count)
    FROM
    (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) avg_table
);

-- ==========================================================

-- 36. Courses where all students received grade 'A'

SELECT c.course_name
FROM courses c
WHERE NOT EXISTS
(
    SELECT *
    FROM enrollments e
    WHERE e.course_id = c.course_id
    AND e.grade <> 'A'
);

-- ==========================================================

-- 37. Highest paid professor in each department

SELECT p.prof_name,
       p.salary,
       d.dept_name
FROM professors p
JOIN departments d
ON p.department_id = d.department_id
WHERE salary =
(
    SELECT MAX(salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);

-- ==========================================================

-- 38. Departments whose average salary is above 85000

SELECT *
FROM
(
    SELECT d.department_id,
           d.dept_name,
           AVG(p.salary) AS avg_salary
    FROM departments d
    JOIN professors p
    ON d.department_id = p.department_id
    GROUP BY d.department_id,d.dept_name
) dept_avg
WHERE avg_salary > 85000;


-- ==========================================================
-- Task 2 : Views
-- ==========================================================

-- 39. Student Enrollment Summary View

CREATE VIEW vw_student_enrollment_summary AS
SELECT
s.student_id,
CONCAT(s.first_name,' ',s.last_name) AS student_name,
d.dept_name,
COUNT(e.course_id) AS total_courses,

ROUND(
AVG(
CASE
WHEN grade='A' THEN 4
WHEN grade='B' THEN 3
WHEN grade='C' THEN 2
WHEN grade='D' THEN 1
WHEN grade='F' THEN 0
END
),2) AS GPA

FROM students s

LEFT JOIN departments d
ON s.department_id=d.department_id

LEFT JOIN enrollments e
ON s.student_id=e.student_id

GROUP BY
s.student_id,
student_name,
d.dept_name;

-- ==========================================================

-- 40. Course Statistics View

CREATE VIEW vw_course_stats AS

SELECT

c.course_name,
c.course_code,

COUNT(e.student_id) AS total_enrollments,

ROUND(
AVG(
CASE

WHEN grade='A' THEN 4
WHEN grade='B' THEN 3
WHEN grade='C' THEN 2
WHEN grade='D' THEN 1
WHEN grade='F' THEN 0

END
),2) avg_gpa

FROM courses c

LEFT JOIN enrollments e

ON c.course_id=e.course_id

GROUP BY
c.course_id,
c.course_name,
c.course_code;

-- ==========================================================

-- 41. Students with GPA above 3

SELECT *
FROM vw_student_enrollment_summary
WHERE GPA>3;

-- ==========================================================

-- 42. Update View

UPDATE vw_student_enrollment_summary
SET student_name='Test'
WHERE student_id=1;

-- Multi-table views are generally not updatable in MySQL.

-- ==========================================================

-- 43. Drop Views

DROP VIEW vw_course_stats;

DROP VIEW vw_student_enrollment_summary;

CREATE VIEW vw_student_enrollment_summary AS

SELECT
student_id,
first_name,
last_name,
department_id

FROM students

WHERE department_id=1

WITH CHECK OPTION;


-- ==========================================================
-- Task 3 : Stored Procedures
-- ==========================================================

DELIMITER $$

CREATE PROCEDURE sp_enroll_student(

IN p_student_id INT,
IN p_course_id INT,
IN p_enrollment_date DATE

)

BEGIN

IF EXISTS(

SELECT *

FROM enrollments

WHERE student_id=p_student_id

AND course_id=p_course_id

)

THEN

SIGNAL SQLSTATE '45000'

SET MESSAGE_TEXT='Student already enrolled';

ELSE

INSERT INTO enrollments

(student_id,course_id,enrollment_date)

VALUES

(p_student_id,p_course_id,p_enrollment_date);

END IF;

END $$

DELIMITER ;

-- ==========================================================

CALL sp_enroll_student(2,5,CURDATE());

-- ==========================================================

CREATE TABLE department_transfer_log(

log_id INT AUTO_INCREMENT PRIMARY KEY,

student_id INT,

old_department INT,

new_department INT,

transfer_date DATETIME

);

-- ==========================================================

DELIMITER $$

CREATE PROCEDURE sp_transfer_student(

IN p_student INT,

IN p_new_department INT

)

BEGIN

DECLARE old_dept INT;

START TRANSACTION;

SELECT department_id

INTO old_dept

FROM students

WHERE student_id=p_student;

UPDATE students

SET department_id=p_new_department

WHERE student_id=p_student;

INSERT INTO department_transfer_log

(student_id,old_department,new_department,transfer_date)

VALUES

(p_student,old_dept,p_new_department,NOW());

COMMIT;

END $$

DELIMITER ;

-- ==========================================================

CALL sp_transfer_student(1,2);

-- ==========================================================
-- 46. Rollback Example
-- ==========================================================

START TRANSACTION;

UPDATE students

SET department_id=2

WHERE student_id=1;

UPDATE students

SET department_id=999

WHERE student_id=2;

ROLLBACK;

-- ==========================================================
-- 47. SAVEPOINT
-- ==========================================================

START TRANSACTION;

INSERT INTO enrollments
(student_id,course_id,enrollment_date)

VALUES
(3,2,CURDATE());

SAVEPOINT first_insert;

INSERT INTO enrollments
(student_id,course_id,enrollment_date)

VALUES
(3,999,CURDATE());

ROLLBACK TO first_insert;

COMMIT;