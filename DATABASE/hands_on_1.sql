
-- Hands-On 1
-- Task 1: Create Database and Tables

CREATE DATABASE college_db;

USE college_db;

-- ===========================================
-- Departments Table
-- ===========================================

CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

-- ===========================================
-- Students Table
-- ===========================================

CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,

    CONSTRAINT fk_student_department
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);

-- ===========================================
-- Courses Table
-- ===========================================

CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,

    CONSTRAINT fk_course_department
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);

-- ===========================================
-- Enrollments Table
-- ===========================================

CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),

    CONSTRAINT fk_enrollment_student
    FOREIGN KEY (student_id)
    REFERENCES students(student_id),

    CONSTRAINT fk_enrollment_course
    FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
);

-- ===========================================
-- Professors Table
-- ===========================================

CREATE TABLE professors (
    professor_id INT PRIMARY KEY AUTO_INCREMENT,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),

    CONSTRAINT fk_professor_department
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);


--Task 2: Verify Normalisation

/*
1NF (First Normal Form):
- All tables contain atomic (single-valued) attributes.
- Each column stores only one value, and there are no repeating groups.
- Example of a 1NF violation would be storing multiple phone numbers
  in a single phone_number column separated by commas.

2NF (Second Normal Form):
- All non-key attributes are fully dependent on the entire primary key.
- In the enrollments table, the candidate key is (student_id, course_id).
- The attributes enrollment_date and grade depend on the complete
  enrollment record, not on student_id or course_id individually.
- Therefore, the schema satisfies 2NF.

3NF (Third Normal Form):
- There are no transitive dependencies.
- Department information (dept_name, hod_name, budget) is stored only
  in the departments table.
- The students, courses, and professors tables store only department_id
  as a foreign key instead of duplicating department details.
- This reduces redundancy and maintains data consistency.

Conclusion:
The college_db schema satisfies 1NF, 2NF, and 3NF by ensuring
atomic values, full functional dependency, and elimination of
transitive dependencies.
*/