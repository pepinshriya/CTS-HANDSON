"""
Hands-On 1
Task 1 : Understand the Request-Response Cycle
=========================================================
"""

# =========================================================
# 1. Request-Response Cycle
# =========================================================

"""
The Request-Response Cycle describes how a web framework
handles an HTTP request and returns a response.

Flow:

Browser
   |
   | HTTP Request
   v
URL Router
   |
   v
View
   |
   v
Model
   |
   v
Database
   |
   v
Model
   |
   v
View
   |
   v
HTTP Response
   |
   v
Browser

Explanation:

1. The browser sends an HTTP request.
2. Django's URL Router matches the requested URL.
3. The corresponding View function/class is executed.
4. The View interacts with the Model if database access is required.
5. The Model communicates with the database.
6. Retrieved data is returned to the View.
7. The View prepares an HTTP response.
8. The browser receives the response.
"""

# =========================================================
# 2. Middleware
# =========================================================

"""
Middleware is software that executes before and after the
View during the request-response cycle.

Its responsibilities include:

- Authentication
- Security checks
- Session management
- Logging
- Request modification
- Response modification

Position in Request Cycle:

Browser
    |
Middleware
    |
URL Router
    |
View
    |
Database
    |
View
    |
Middleware
    |
Browser

Built-in Middleware Examples

1. SecurityMiddleware
   - Adds important security protections.
   - Can enforce HTTPS and add security headers.

2. SessionMiddleware
   - Creates and manages user sessions.
   - Allows Django to remember logged-in users.
"""

# =========================================================
# 3. WSGI vs ASGI
# =========================================================

"""
WSGI
-----

WSGI stands for Web Server Gateway Interface.

It acts as a bridge between the web server and
the Django application.

Characteristics:
- Synchronous processing
- One request per worker at a time
- Suitable for traditional web applications

Examples:
- Django (default)
- Flask

---------------------------------------------------------

ASGI
-----

ASGI stands for Asynchronous Server Gateway Interface.

It supports asynchronous programming and modern protocols
such as WebSockets.

Characteristics:
- Async request handling
- Better for long-running I/O operations
- Supports WebSockets
- Higher concurrency for async workloads

Examples:
- FastAPI
- Django (when using ASGI)

Django creates both:

wsgi.py
    Used for WSGI deployment.

asgi.py
    Used for ASGI deployment.
"""

# =========================================================
# 4. MVC vs MVT
# =========================================================

"""
MVC

Model
    Handles database operations.

View
    Displays data to users.

Controller
    Handles incoming requests and coordinates
    between Model and View.

---------------------------------------------------------

Django follows MVT

Model
    Database layer.

View
    Handles requests and business logic.

Template
    Displays data to users.

MVC Mapping

MVC Model      -> Django Model
MVC Controller -> Django View
MVC View       -> Django Template

Django's View performs the role of the Controller,
while the Template performs the role of the View
in traditional MVC.
"""

# manage.py
# Command-line utility used to manage Django project tasks.

# settings.py
# Contains the global configuration and settings for the Django project.

# urls.py
# Maps incoming URLs to their corresponding view functions or classes.

# wsgi.py
# Exposes the WSGI application for deployment using WSGI servers.

# asgi.py
# Exposes the ASGI application for asynchronous deployment using ASGI servers.


from courses.models import Department

# Retrieve all departments
Department.objects.all()

# Retrieve one department
Department.objects.get(id=1)

# Filter departments
Department.objects.filter(
    department_name="Computer Science"
)

# First department
Department.objects.first()

# Check existence
Department.objects.filter(
    department_name="Computer Science"
).exists()