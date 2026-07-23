# Hands-On 2 – SDLC vs TDLC, V-Model & Agile QA Integration

# Task 1 – V-Model Mapping

## Step 9: V-Model Diagram

```
                    SDLC (Development)

             Requirements
                  │
                  │
           System Design
                  │
                  │
        Architecture Design
                  │
                  │
           Module Design
                  │
                  │
                Coding
                  ▲
                  │
            Unit Testing
                  │
                  │
        Integration Testing
                  │
                  │
          System Testing
                  │
                  │
      Acceptance Testing

               TDLC (Testing)
```

### SDLC ↔ TDLC Mapping

| SDLC Phase | Corresponding TDLC Phase |
|------------|--------------------------|
| Requirements | Acceptance Testing |
| System Design | System Testing |
| Architecture Design | Integration Testing |
| Module Design | Unit Testing |
| Coding | Implementation |

---

# Step 10: Test Artifacts Produced

| SDLC Phase | Test Artifact Produced |
|------------|------------------------|
| Requirements | Acceptance Test Plan |
| System Design | System Test Plan |
| Architecture Design | Integration Test Plan |
| Module Design | Unit Test Cases |
| Coding | Executable Source Code |

---

# Step 11: Entry and Exit Criteria

## Unit Testing

### Entry Criteria
- Module implementation completed.
- Unit test cases prepared.
- Development environment available.

### Exit Criteria
- All unit test cases executed.
- No Critical or High severity defects remain.
- Unit test report completed.

---

## Integration Testing

### Entry Criteria
- Individual modules successfully pass unit testing.
- Integration environment is ready.
- Integration test cases prepared.

### Exit Criteria
- Module communication verified.
- Integration defects resolved.
- Integration testing report completed.

---

## System Testing

### Entry Criteria
- Complete application integrated.
- System test cases prepared.
- Test environment configured.

### Exit Criteria
- All system test cases executed.
- No unresolved Critical or High defects.
- System testing completed successfully.

---

## User Acceptance Testing (Acceptance Testing)

### Entry Criteria
- System Testing completed successfully.
- Business requirements finalized.
- UAT environment ready.

### Exit Criteria
- Users approve the application.
- Business requirements satisfied.
- Customer signs off for production deployment.

---

# Step 12: QA Engagement in the V-Model

QA should participate before testing begins.

### 1. Requirements Review

QA reviews the Software Requirements Specification (SRS) to:
- Identify ambiguous requirements.
- Ensure requirements are testable.
- Clarify missing information.
- Prepare Acceptance Test Plans early.

---

### 2. Design Review

QA participates during System and Architecture Design to:
- Review system design.
- Identify potential risks.
- Prepare Integration and System Test Cases.
- Verify that the design supports testing.

Early QA involvement helps identify defects before coding begins, reducing the overall cost of fixing issues.



# Task 2 – Agile QA and Shift-Left Testing

## Step 13: Problems with Waterfall Testing

In the traditional Waterfall model, testing starts only after development is completed. This can create several challenges for the Course Management API project.

### Problem 1: Late Defect Detection
Defects are discovered only after development is finished. Fixing them at this stage is expensive and time-consuming.

### Problem 2: Increased Development Cost
Changes made after implementation require additional coding, testing, and deployment effort, increasing the overall project cost.

### Problem 3: Delayed Product Delivery
Critical defects found during the testing phase can delay the release schedule and affect project timelines.

---

# Step 14: QA Role in Agile Ceremonies

## Sprint Planning
- Understand user stories.
- Define acceptance criteria.
- Estimate testing effort.
- Identify test scenarios.

## Daily Stand-up
- Report testing progress.
- Discuss blockers.
- Coordinate with developers.
- Update defect status.

## Sprint Review
- Verify completed user stories.
- Demonstrate tested features.
- Validate acceptance criteria.
- Collect stakeholder feedback.

## Retrospective
- Analyze issues faced during the sprint.
- Suggest process improvements.
- Discuss testing challenges.
- Improve collaboration for future sprints.

---

# Step 15: Shift-Left Testing Practices

Shift-Left Testing means starting testing activities as early as possible in the Software Development Life Cycle (SDLC).

### 1. Requirement Review for Testability
QA reviews the Software Requirements Specification (SRS) before development begins to identify ambiguities and ensure requirements are testable.

### 2. Writing Test Cases Before Coding (TDD/BDD)
Prepare test cases before implementation so developers clearly understand the expected behavior.

### 3. Static Code Analysis
Use static analysis tools to identify coding issues, security vulnerabilities, and coding standard violations before execution.

### 4. API Contract Testing Before Integration
Validate API request and response contracts before integrating different system components, reducing integration defects.

---

# Step 16: Acceptance Criteria (Given-When-Then Format)

## Scenario 1: Happy Path

**Given**
- The college administrator is on the Create Course page.

**When**
- The administrator enters valid course details and submits the form.

**Then**
- The course is created successfully.
- A success message is displayed.
- The new course appears in the course list.

---

## Scenario 2: Duplicate Course Code

**Given**
- A course with the same course code already exists.

**When**
- The administrator submits another course using the existing course code.

**Then**
- The system displays an appropriate validation error.
- The duplicate course is not created.

---

## Scenario 3: Missing Required Fields

**Given**
- The administrator leaves one or more mandatory fields empty.

**When**
- The administrator submits the form.

**Then**
- Validation errors are displayed.
- The course is not created until all required fields are completed.
