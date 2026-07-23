from typing import List, Optional

from pydantic import BaseModel, EmailStr


class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int


class DepartmentResponse(BaseModel):
    id: int
    name: str
    courses: List[CourseResponse]


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    enrollment_year: int
    department_id: int

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    enrollment_year: int
    department_id: int
class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    enrollment_year: Optional[int] = None
    department_id: Optional[int] = None

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    grade: str


class EnrollmentUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    grade: Optional[str] = None

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    grade: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str