# Hands-On 3 – Test Automation Process, Lifecycle & Framework Types

# Task 1 – Automation Decision and Test Case Selection

## Step 17: Criteria for Deciding Whether a Test Case Should Be Automated

Automation is beneficial when tests are repetitive, stable, and executed frequently. The following criteria help determine whether a test case is a good candidate for automation.

### 1. Frequency of Execution
Tests that are executed repeatedly, such as regression tests, are ideal for automation.

**Application to Scenario:**
The `POST /api/courses/` endpoint is tested after every code change, making it a strong candidate for automation.

---

### 2. Repetitive Nature
Tests that require the same steps every time can be automated to save effort and reduce human error.

**Application to Scenario:**
Sending the same API request and verifying the response is repetitive and suitable for automation.

---

### 3. Stable Functionality
Features that do not change frequently are good automation candidates because automated scripts require less maintenance.

**Application to Scenario:**
Course creation is a core feature that remains relatively stable, making it appropriate for automation.

---

### 4. High Business Risk
Critical functionalities should always be automated to ensure they continue working after every release.

**Application to Scenario:**
If course creation fails, the application cannot function correctly. Therefore, this test has high business value.

---

### 5. Time Savings
Automation is useful when manual execution is time-consuming and repeated frequently.

**Application to Scenario:**
Automating course creation reduces testing time and enables continuous regression testing.

---

# Step 18: Automate or Manual Decision

| Test Case | Decision | Justification |
|------------|----------|---------------|
| Regression test for all CRUD endpoints after every code change | Automate | Frequently executed and repetitive. |
| Exploratory testing of a new search feature | Manual | Requires human observation and creativity. |
| Performance test with 100 concurrent users | Automate | Performance testing requires automated tools to simulate multiple users. |
| UI test for the login form | Automate | Frequently executed during regression testing. |
| Verify Swagger API documentation | Manual | Documentation changes infrequently and requires human review. |
| Smoke test after deployment | Automate | Quickly verifies whether the application is operational after deployment. |

---

# Step 19: Test Automation ROI

### Definition

**Return on Investment (ROI)** measures whether the time and effort spent creating automation are justified by the time saved during repeated executions.

### Given

- Automation Development Time = 4 hours
- Manual Execution Time = 30 minutes (0.5 hour)

### Break-Even Calculation

```
4 ÷ 0.5 = 8 runs
```

After **8 executions**, the automation has recovered its development cost.

### Maintenance Overhead

After the **10th execution**, each automated run requires an additional **20% maintenance effort**.

Maintenance per run:

```
0.5 × 20% = 0.1 hour
```

Effective saving after maintenance:

```
0.5 - 0.1 = 0.4 hour per run
```

Even with maintenance, automation continues to provide long-term time savings.

---

# Step 20: Flaky Test

### Definition

A flaky test is a test that passes sometimes and fails at other times without any changes to the application.

---

### Example

A Selenium test clicks a button immediately after page load.

Sometimes:
- Page loads quickly → Test passes.

Other times:
- Page loads slowly → Test fails because the element is not yet available.

---

### Strategies to Prevent Flaky Tests

#### 1. Use Explicit Waits
Wait until an element is visible or clickable before interacting with it.

#### 2. Use Stable Locators
Prefer ID or CSS selectors over fragile absolute XPath expressions.

#### 3. Ensure Test Independence
Each test should execute independently without depending on another test's data or execution order.


# Step 21: Automation Framework Types

| Framework | Description | Advantage | Disadvantage | Course Management Example |
|-----------|-------------|-----------|--------------|---------------------------|
| Linear | All automation steps are written sequentially in a single script. | Simple and easy to understand. | Difficult to maintain as the project grows. | Automating only the Create Course feature in a small project. |
| Modular | The application is divided into independent modules, each with reusable automation scripts. | High code reusability and easier maintenance. | Requires planning and module management. | Separate modules for Login, Course Management, Student Management, and Reports. |
| Data-Driven | Test logic is separated from test data, allowing multiple datasets to be executed using the same test script. | Supports multiple test datasets with minimal code duplication. | External test data requires maintenance. | Login testing with 50 different user credentials stored in Excel. |
| Keyword-Driven | Test execution is controlled using predefined keywords that represent actions. | Allows non-technical users to design test cases. | Framework implementation is more complex. | Business users define login and course creation tests using keywords. |
| Hybrid | Combines Modular, Data-Driven, and Keyword-Driven approaches into a single framework. | Highly scalable, reusable, and maintainable. | Initial development is more complex. | Enterprise-level Course Management automation framework combining reusable modules, external test data, and shared utilities. |


# Step 22: Framework Recommendation

For the given Course Management frontend scenario, the recommended approach is a **Hybrid Framework** because it combines the strengths of multiple framework types.

### Requirement Analysis

| Requirement | Recommended Framework | Justification |
|-------------|-----------------------|---------------|
| Test login with 50 different user/password combinations | Data-Driven Framework | The same login test can be executed using multiple datasets stored in Excel, CSV, or JSON files. |
| Reuse login steps across 20 test cases | Modular Framework | A reusable login module avoids code duplication and simplifies maintenance. |
| Support both technical and non-technical team members | Keyword-Driven Framework | Non-technical users can define test cases using keywords without writing Selenium code. |

### Final Recommendation

A **Hybrid Framework** is recommended because it combines:

- Modular Framework
- Data-Driven Framework
- Keyword-Driven Framework

This approach provides reusable automation scripts, external test data management, better maintainability, scalability, and support for both technical and non-technical team members.


# Step 23: Hybrid Framework Structure

A recommended Hybrid Automation Framework for the Course Management application is shown below.

```text
course_management_framework/
│
├── tests/
│   ├── test_login.py
│   ├── test_courses.py
│   └── test_students.py
│
├── pages/
│   ├── login_page.py
│   ├── course_page.py
│   └── student_page.py
│
├── data/
│   ├── login_data.xlsx
│   └── courses.json
│
├── utils/
│   ├── browser.py
│   ├── excel_reader.py
│   ├── waits.py
│   └── screenshots.py
│
├── reports/
│
├── config/
│   └── config.json
│
├── requirements.txt
└── README.md
```

### Justification

- **tests/** contains all automated test scripts.
- **pages/** stores reusable Page Object classes.
- **data/** contains external test data for Data-Driven testing.
- **utils/** provides reusable helper functions such as browser setup and screenshot capture.
- **reports/** stores execution reports and screenshots.
- **config/** centralizes application settings such as the base URL and browser configuration.

This structure improves code reusability, maintainability, scalability, and supports enterprise-level Selenium automation projects.