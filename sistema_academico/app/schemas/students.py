# app/schemas/students.py
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    full_name: str
    email: EmailStr
    identification: str
    is_active: Optional[bool] = True


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    identification: Optional[str] = None


class StudentInDBBase(StudentBase):
    id: int

    class Config:
        orm_mode = True


class Student(StudentInDBBase):
    pass


class EnrollmentBase(BaseModel):
    student_id: int
    section_id: int
    enrollment_date: str
    is_active: Optional[bool] = True


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(EnrollmentBase):
    student_id: Optional[int] = None
    section_id: Optional[int] = None
    enrollment_date: Optional[str] = None


class EnrollmentInDBBase(EnrollmentBase):
    id: int

    class Config:
        orm_mode = True


class Enrollment(EnrollmentInDBBase):
    pass


class GradeBase(BaseModel):
    student_id: int
    enrollment_id: int
    exam_id: int
    score: float
    comments: Optional[str] = None
    graded_by_id: int
    grading_date: str


class GradeCreate(GradeBase):
    pass


class GradeUpdate(GradeBase):
    student_id: Optional[int] = None
    enrollment_id: Optional[int] = None
    exam_id: Optional[int] = None
    score: Optional[float] = None
    graded_by_id: Optional[int] = None
    grading_date: Optional[str] = None


class GradeInDBBase(GradeBase):
    id: int

    class Config:
        orm_mode = True


class Grade(GradeInDBBase):
    pass