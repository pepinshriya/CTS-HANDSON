from fastapi.middleware.cors import CORSMiddleware

from typing import Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt


from security import get_password_hash,create_access_token,verify_password,oauth2_scheme,SECRET_KEY,ALGORITHM



from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status,
)
from contextlib import asynccontextmanager

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, init_db
from models import Course, Enrollment, Student, User
from schemas import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
    EnrollmentUpdate,
    StudentCreate,
    StudentResponse,
    StudentUpdate,
    UserLogin,
    UserRegister,
    UserResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Course Management API",
    description="""
REST API for managing Departments,
Courses, Students and Enrollments.
""",
    version="1.0.0",
    contact={
        "name": "Maheshkumar K",
        "email": "mahesh@example.com",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================================================
# Helper Functions
# ===================================================

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    """
    Standardized error response for all HTTP exceptions.
    """

    if (
        isinstance(exc.detail, dict)
        and "error" in exc.detail
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "ERROR",
                "message": str(exc.detail),
                "field": None,
            }
        },
    )

def error_response(
    code: str,
    message: str,
    field: str | None = None,
):
    """
    Standardized error response required by Hands-On 8 Step 85.
    """
    return {
        "error": {
            "code": code,
            "message": message,
            "field": field,
        }
    }


def build_pagination(
    *,
    page: int,
    page_size: int,
    total: int,
    results,
    base_url: str,
):
    """
    DRF-style pagination response.
    """

    next_url = None
    previous_url = None

    if page * page_size < total:
        next_url = (
            f"{base_url}?page={page + 1}"
            f"&page_size={page_size}"
        )

    if page > 1:
        previous_url = (
            f"{base_url}?page={page - 1}"
            f"&page_size={page_size}"
        )

    return {
        "count": total,
        "next": next_url,
        "previous": previous_url,
        "results": results,
    }


# ===================================================
# Root Endpoint
# ===================================================

@app.get("/")
async def root():
    return {
        "message": "Course Management API is running."
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error_response(
            "INVALID_TOKEN",
            "Could not validate credentials",
        ),
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user

# ===================================================
# Courses CRUD
# API Versioning:
# URL Versioning  : /api/v1/courses/
# Header Versioning: Accept: application/vnd.api+json;version=1
# ===================================================


@app.post(
    "/api/v1/auth/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
    summary="Register a new user",
)
async def register_user(
    user: UserRegister,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    # Check if email already exists
    result = await db.execute(
        select(User).where(
            User.email == user.email
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_response(
                "EMAIL_ALREADY_EXISTS",
                "Email is already registered",
                "email",
            ),
        )

    # bcrypt is intentionally slow, making brute-force attacks
    # much harder than MD5 or SHA-256.

    hashed_password = get_password_hash(user.password)

    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=1,
    )

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    response.headers[
        "Location"
    ] = f"/api/v1/users/{new_user.id}"

    return new_user

@app.get(
    "/api/v1/courses/",
    status_code=status.HTTP_200_OK,
    tags=["Courses"],
    summary="Get all courses",
)
async def get_courses(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Course)

    if department_id is not None:
        query = query.where(
            Course.department_id == department_id
        )

    if search:
        search_text = f"%{search}%"

        query = query.where(
            or_(
                Course.name.ilike(search_text),
                Course.code.ilike(search_text),
            )
        )

    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    offset = (page - 1) * page_size

    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)

    courses = result.scalars().all()

    return build_pagination(
        page=page,
        page_size=page_size,
        total=total,
        results=courses,
        base_url="/api/v1/courses/",
    )


@app.get(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
    tags=["Courses"],
)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                "NOT_FOUND",
                f"Course with id {course_id} does not exist",
            ),
        )

    return course


@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
)
async def create_course(
    course: CourseCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),

):
    new_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id,
    )

    db.add(new_course)

    await db.commit()

    await db.refresh(new_course)

    response.headers[
        "Location"
    ] = f"/api/v1/courses/{new_course.id}/"

    return new_course


@app.put(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
    tags=["Courses"],
)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                "NOT_FOUND",
                "Course not found",
            ),
        )

    course.name = course_data.name
    course.code = course_data.code
    course.credits = course_data.credits
    course.department_id = course_data.department_id

    await db.commit()
    await db.refresh(course)

    return course


# ================================
# PATCH Endpoint (Step 79)
# ================================

@app.patch(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
    tags=["Courses"],
)
async def patch_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                "NOT_FOUND",
                "Course not found",
            ),
        )

    if course_data.name is not None:
        course.name = course_data.name

    if course_data.code is not None:
        course.code = course_data.code

    if course_data.credits is not None:
        course.credits = course_data.credits

    if course_data.department_id is not None:
        course.department_id = (
            course_data.department_id
        )

    await db.commit()

    await db.refresh(course)

    return course


@app.delete(
    "/api/v1/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"],
)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                "NOT_FOUND",
                "Course not found",
            ),
        )

    await db.delete(course)

    await db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@app.get(
    "/api/v1/courses/{course_id}/students/",
    response_model=list[StudentResponse],
    tags=["Courses"],
)
async def get_course_students(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Student)
        .join(Enrollment)
        .where(
            Enrollment.course_id == course_id
        )
    )

    return result.scalars().all()


@app.get(
    "/api/v1/students/",
    status_code=status.HTTP_200_OK,
    tags=["Students"],
)
async def get_students(
    page: int = 1,
    page_size: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Student)

    if department_id is not None:
        query = query.where(
            Student.department_id == department_id
        )

    total = await db.scalar(
        select(func.count()).select_from(query.subquery())
    )

    offset = (page - 1) * page_size

    result = await db.execute(
        query.offset(offset).limit(page_size)
    )

    students = result.scalars().all()

    return build_pagination(
        page=page,
        page_size=page_size,
        total=total,
        results=students,
        base_url="/api/v1/students/",
    )

@app.get(
    "/api/v1/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Students"],
)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                "NOT_FOUND",
                f"Student with id {student_id} does not exist",
            ),
        )

    return student

    

@app.post(
    "/api/v1/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
async def create_student(
    student: StudentCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    new_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        enrollment_year=student.enrollment_year,
        department_id=student.department_id,
    )

    db.add(new_student)

    await db.commit()

    await db.refresh(new_student)

    response.headers[
        "Location"
    ] = f"/api/v1/students/{new_student.id}/"

    return new_student


@app.patch(
    "/api/v1/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Students"],
)
async def patch_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                "NOT_FOUND",
                "Student not found",
            ),
        )

    if student_data.first_name is not None:
        student.first_name = student_data.first_name

    if student_data.last_name is not None:
        student.last_name = student_data.last_name

    if student_data.email is not None:
        student.email = student_data.email

    if student_data.enrollment_year is not None:
        student.enrollment_year = student_data.enrollment_year

    if student_data.department_id is not None:
        student.department_id = student_data.department_id

    await db.commit()
    await db.refresh(student)

    return student

@app.delete(
    "/api/v1/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Student).where(
            Student.id == student_id
        )
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(
                code="NOT_FOUND",
                message=f"Student with id {student_id} does not exist",
            ),
        )

    await db.delete(student)

    await db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

@app.get(
    "/api/v1/enrollments/",
    status_code=status.HTTP_200_OK,
    response_model=None,
    tags=["Enrollments"],
)
async def get_enrollments(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db),
):
    query = select(Enrollment)

    total = await db.scalar(
        select(func.count()).select_from(query.subquery())
    )

    offset = (page - 1) * page_size

    result = await db.execute(
        query.offset(offset).limit(page_size)
    )

    enrollments = result.scalars().all()

    return build_pagination(
        page=page,
        page_size=page_size,
        total=total,
        results=enrollments,
        base_url="/api/v1/enrollments/",
    )


@app.get(
    "/api/v1/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Enrollments"],
)
async def get_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(
                "NOT_FOUND",
                f"Enrollment with id {enrollment_id} does not exist",
            ),
        )

    return enrollment


@app.post(
    "/api/v1/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        grade=enrollment.grade,
    )

    db.add(new_enrollment)

    await db.commit()

    await db.refresh(new_enrollment)

    response.headers[
        "Location"
    ] = f"/api/v1/enrollments/{new_enrollment.id}/"

    result = await db.execute(
        select(Student).where(
            Student.id == enrollment.student_id
        )
    )

    student = result.scalar_one_or_none()

    # if student:
    #     background_tasks.add_task(
    #         send_confirmation_email,
    #         student.email,
    #     )

    return new_enrollment


@app.patch(
    "/api/v1/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Enrollments"],
)
async def patch_enrollment(
    enrollment_id: int,
    enrollment_data: EnrollmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(
                "NOT_FOUND",
                "Enrollment not found",
            ),
        )

    if enrollment_data.student_id is not None:
        enrollment.student_id = enrollment_data.student_id

    if enrollment_data.course_id is not None:
        enrollment.course_id = enrollment_data.course_id

    if enrollment_data.grade is not None:
        enrollment.grade = enrollment_data.grade

    await db.commit()

    await db.refresh(enrollment)

    return enrollment


@app.delete(
    "/api/v1/enrollments/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"],
)
async def delete_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(
                "NOT_FOUND",
                f"Enrollment with id {enrollment_id} does not exist",
            ),
        )

    await db.delete(enrollment)

    await db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

@app.put(
    "/api/v1/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Enrollments"],
)
async def update_enrollment(
    enrollment_id: int,
    enrollment_data: EnrollmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(
                "NOT_FOUND",
                f"Enrollment with id {enrollment_id} does not exist",
            ),
        )

    # PUT = Full Update
    enrollment.student_id = enrollment_data.student_id
    enrollment.course_id = enrollment_data.course_id
    enrollment.grade = enrollment_data.grade

    await db.commit()
    await db.refresh(enrollment)

    return enrollment



@app.post(
    "/api/v1/auth/login/",
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
    summary="Login user",
)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(
            User.email == user.email
        )
    )

    db_user = result.scalar_one_or_none()

    if (
        db_user is None
        or not verify_password(
            user.password,
            db_user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response(
                "INVALID_CREDENTIALS",
                "Invalid email or password",
            ),
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error_response(
            "INVALID_TOKEN",
            "Could not validate credentials",
        ),
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user



# =====================================================
# OAuth2 Authorization Code Flow vs JWT Login
#
# OAuth2 Authorization Code Flow:
# - User authenticates with an external Identity Provider
#   (Google, GitHub, Microsoft, etc.).
# - The provider returns an authorization code.
# - The backend exchanges the code for an access token.
# - The application never receives the user's password.
#
# JWT Login (this assignment):
# - User logs in directly using email and password.
# - FastAPI verifies the credentials.
# - The application generates and returns a JWT.
# - The JWT is used for authentication on future requests.
# =====================================================