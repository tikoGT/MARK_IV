# app/schemas/courses.py
from typing import List, Optional
from pydantic import BaseModel


class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    name: Optional[str] = None
    pass


class CourseInDBBase(CourseBase):
    id: int
    created_by_id: int

    class Config:
        orm_mode = True


class Course(CourseInDBBase):
    pass


class SectionBase(BaseModel):
    name: str
    course_id: int
    is_active: Optional[bool] = True


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    name: Optional[str] = None
    course_id: Optional[int] = None


class SectionInDBBase(SectionBase):
    id: int

    class Config:
        orm_mode = True


class Section(SectionInDBBase):
    pass


class MaterialBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_type: str


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(MaterialBase):
    title: Optional[str] = None
    file_type: Optional[str] = None


class MaterialInDBBase(MaterialBase):
    id: int
    file_path: str
    uploaded_by_id: int
    upload_date: str

    class Config:
        orm_mode = True


class Material(MaterialInDBBase):
    pass