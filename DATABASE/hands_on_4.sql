-- Hands-on Exercise 4: Query Optimization

-- Task 1 : Baseline Performance — No Indexes

-- 48. Query Execution Plan

EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e   
JOIN students s ON s.student_id = e.student_id   
JOIN courses c ON c.course_id = e.course_id   
WHERE s.enrollment_year = 2022;

-- Output:

-- EXPLAIN
-- {
--   query_block"": {"
--     "select_id": 1
--     "cost_info": {
--       "query_cost": "2.53"
--     }
--     "nested_loop": [
--       {
--         "table": {
--           "table_name": "s"
--           "access_type": "ALL"
--           "possible_keys": [
--             "PRIMARY"
--           ]
--           "rows_examined_per_scan": 10
--           "rows_produced_per_join": 1
--           "filtered": "10.00"
--           "cost_info": {
--             "read_cost": "1.15"
--             "eval_cost": "0.10"
--             "prefix_cost": "1.25"
--             "data_read_per_join": "824"
--           }
--           "used_columns": [
--             "student_id"
--             "first_name"
--             "last_name"
--             "enrollment_year"
--           ]
--           "attached_condition": "(`college_db`.`s`.`enrollment_year` = 2022)"
--         }
--       }
--       {
--         "table": {
--           "table_name": "e"
--           "access_type": "ref"
--           "possible_keys": [
--             "student_id"
--             "course_id"
--           ]
--           "key": "student_id"
--           "used_key_parts": [
--             "student_id"
--           ]
--           "key_length": "5"
--           "ref": [
--             "college_db.s.student_id"
--           ]
--           "rows_examined_per_scan": 1
--           "rows_produced_per_join": 1
--           "filtered": "100.00"
--           "cost_info": {
--             "read_cost": "0.46"
--             "eval_cost": "0.18"
--             "prefix_cost": "1.89"
--             "data_read_per_join": "58"
--           }
--           "used_columns": [
--             "student_id"
--             "course_id"
--           ]
--           "attached_condition": "(`college_db`.`e`.`course_id` is not null)"
--         }
--       }
--       {
--         "table": {
--           "table_name": "c"
--           "access_type": "eq_ref"
--           "possible_keys": [
--             "PRIMARY"
--           ]
--           "key": "PRIMARY"
--           "used_key_parts": [
--             "course_id"
--           ]
--           "key_length": "4"
--           "ref": [
--             "college_db.e.course_id"
--           ]
--           "rows_examined_per_scan": 1
--           "rows_produced_per_join": 1
--           "filtered": "100.00"
--           "cost_info": {
--             "read_cost": "0.46"
--             "eval_cost": "0.18"
--             "prefix_cost": "2.53"
--             "data_read_per_join": "1K"
--           }
--           "used_columns": [
--             "course_id"
--             "course_name"
--           ]
--         }
--       }
--     ]
--   }
-- }"

-- HOW INDEXING WORKS
-- 1. Understanding Data Storage and Representation
 
-- 	• Logical vs Physical Representation
-- 		a. Logical representation (user's view): Data appears as tables with rows and columns (e.g., Employee ID, Name, Address).
-- 		b. Physical representation (DBMS view): Data is stored differently in data pages, managed by the DBMS.
-- 	• Data Pages
-- 	A data page is typically 8KB in size and contains:
-- 		a. Header (96 bytes): Stores metadata (e.g., page ID, free space, checksum).
-- 		b. Data Records Area (~8060 bytes): Contains actual rows of the table.
-- 		c. Offset Array (36 bytes): An array of pointers to rows, ensuring logical sequence.
-- 	• Row Storage in Data Pages
-- 		○ Rows are stored in the page in the order they are inserted into the table.
-- 		○ Example: In an 8KB page, if rows are 64 bytes each, ~125 rows can fit into one data page. Rows exceeding the 8KB capacity will trigger page splitting.
-- 	• Data Blocks
-- 		○ Data blocks are physical storage units on disk.
-- 		○ Minimum unit for I/O (input/output) operations.
-- 		○ DBMS maps data pages to data blocks, allowing them to save/load pages when needed.
 

-- 2. Role of Indexing in Search Optimization
 
-- 	• Purpose of Indexing
-- 		○ Used to improve query performance by reducing row fetch time.
-- 		○ Without an index, DBMS performs sequential scanning (Big O(n)).
-- 		○ With an index, the search time complexity is reduced to O(log n).
-- 	• How Indexing Works
-- 		○ A column (e.g., Employee ID) is indexed using a B+ Tree:
-- 			i. Leaf nodes store actual column values.
-- 			ii. Root and intermediary nodes are used for navigation only.
-- 		○ Example:
-- 			§ Indexed rows like [19, 25, 30] would result in a balanced B+ Tree.
 

-- 3. How DBMS Manages Data Pages, Indexing, and Rows
 
-- 	• Data Page Selection During Insertions
-- 		a. When a row is inserted, the system uses the B+ Tree to find the most appropriate data page.
-- 		b. If the page is full, DBMS performs page splitting:
-- 			§ Creates a new data page.
-- 			§ Splits data between the old and new data pages.
-- 			§ Updates the index pointers.
-- 	• Offset Array
-- 		○ Ensures logical ordering in data pages independent of physical row order.
-- 		○ Example:
-- 			§ Indexed order of rows: 1 → 2 → 4 → 5.
-- 			§ Offset array rearranges the rows in logical order during traversal.
-- 	• Steps for Query Execution
-- 		a. Load Index Page: Read index pages to locate the B+ Tree structure in memory.
-- 		b. Traverse Index: Use the B+ Tree to find the correct data page.
-- 		c. Load Data Block: Load the data block containing the selected data page.
-- 		d. Access Row: Use the offset array within the data page to fetch the proper row.
 

-- 4. Types of Indexing: Clustered vs Non-Clustered
 
-- 	• Clustered Indexing
-- 		○ Rows are physically ordered in the data page to match the order of the index.
-- 		○ Example:
-- 			§ If Employee ID is indexed, rows in the pages are ordered as 1, 2, 4, 5 in the offset array.
-- 		○ Offset Array Role:
-- 			§ Responsible for ensuring data rows are accessed in index-defined logical order.
-- 		○ Only one clustered index is allowed per table, as it determines row order.
-- 		○ Usually applied to the primary key by default.
-- 	• Non-Clustered Indexing
-- 		○ Does not determine the physical order of rows; instead, maintains an additional B+ Tree on non-primary key columns.
-- 		○ Multiple non-clustered indexes (e.g., for Name, Address, etc.) can exist in a table.
-- 		○ Example:
-- 			§ A secondary index on the Name column creates a separate B+ Tree mapping names to data page pointers.
 

-- 5. Why Avoid Too Many Indexes?
 
-- 	• Storage and Memory Costs:
-- 		○ A new index creates a B+ Tree and occupies additional disk and memory resources.
-- 		○ Index information must fit into index pages, which are stored in data blocks.
-- 	• Update Overhead:
-- 		○ Every time a row is added or deleted, all affected indexes must be:
-- 			i. Updated in B+ trees.
-- 			ii. Updated in index pages.
-- 	• Practical Indexing Guidelines:
-- 		○ Use primary keys for clustered indexing.
-- 		○ Create only necessary secondary indexes on frequently queried columns.
-- 		○ Avoid indexing too many columns, as it increases system overhead.
 

-- In Summary:
	 
-- 	1. Storage Hierarchy: Logical tables → Data Pages → Data Blocks.
-- 	2. Indexing Mechanism: Uses B+ Trees to optimize search, build index pages, and map rows to data.
-- 	3. Clustered Indexing: Ensures row order based on primary key or manually defined clustered key.
-- 	4. Non-clustered Indexing: Allows additional indexing but impacts memory usage and update performance.
-- Design Considerations: Index sparingly and efficiently to avoid performance and storage penalties.

-- ==========================================================
-- 49. Identify Full Table Scan
-- ==========================================================

/*
Analysis of EXPLAIN FORMAT=JSON

1. Students Table (alias: s)
---------------------------------
access_type : ALL

Meaning:
MySQL performs a Full Table Scan on the students table because
there is no index on the enrollment_year column. Therefore,
every row in the students table is scanned to locate students
whose enrollment_year = 2022.

2. Enrollments Table (alias: e)
---------------------------------
access_type : ref

Meaning:
MySQL uses an existing index on student_id to locate matching
rows from the enrollments table. This is more efficient than
a Full Table Scan.

3. Courses Table (alias: c)
---------------------------------
access_type : eq_ref

Meaning:
MySQL performs a Primary Key lookup using course_id.
eq_ref is one of the most efficient join types because
exactly one matching row is retrieved from the courses table.

Observation:
Only the students table performs a Full Table Scan.
This can be optimized by creating an index on
students(enrollment_year).
*/

-- ==========================================================
-- 50. Estimated Cost / Rows Examined
-- ==========================================================

/*
Execution Plan Statistics

Overall Query Cost
-------------------
Query Cost : 2.53

Table Statistics

Students (s)
-------------------
Access Type              : ALL
Rows Examined Per Scan   : 10
Rows Produced Per Join   : 1
Filtered                 : 10%

Enrollments (e)
-------------------
Access Type              : ref
Rows Examined Per Scan   : 1
Rows Produced Per Join   : 1
Filtered                 : 100%

Courses (c)
-------------------
Access Type              : eq_ref
Rows Examined Per Scan   : 1
Rows Produced Per Join   : 1
Filtered                 : 100%

Conclusion

• The students table is the bottleneck because MySQL scans
  every row to evaluate the condition
  WHERE enrollment_year = 2022.

• The enrollments table efficiently uses an index lookup
  (access_type = ref).

• The courses table efficiently uses the PRIMARY KEY
  (access_type = eq_ref).

Recommendation

Create an index on students(enrollment_year) to eliminate
the Full Table Scan and improve query performance.
*/


-- ==========================================================
-- Task 2 : Add Indexes and Compare Plans
-- ==========================================================

-- 51. Create a B-Tree Index

CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);


-- 52. Create a Composite UNIQUE Index

CREATE UNIQUE INDEX idx_enrollment_student_course
ON enrollments(student_id, course_id);


-- 53. Create an Index on course_code

CREATE INDEX idx_courses_course_code
ON courses(course_code);


-- 54. Re-run EXPLAIN

EXPLAIN FORMAT=JSON
SELECT s.first_name,
       s.last_name,
       c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

/*
Compare this execution plan with the baseline.

Expected Changes:

Before Indexing:
----------------
students  -> access_type = ALL (Full Table Scan)

After Indexing:
---------------
students  -> access_type = ref or range

Observation:
The Full Table Scan should be replaced by an Index Scan,
reducing the number of rows examined and improving query
performance.
*/


-- 55. Partial Index (PostgreSQL only)

/*
MySQL does not support Partial Indexes.

PostgreSQL Syntax:

CREATE INDEX idx_student_null_grade
ON enrollments(student_id)
WHERE grade IS NULL;

Equivalent MySQL alternative:
*/

CREATE INDEX idx_student_grade
ON enrollments(student_id, grade);

