# app/schemas/exams.py
from typing import List, Optional
from pydantic import BaseModel


class QuestionOptionBase(BaseModel):
    content: str
    is_correct: bool = False


class QuestionOptionCreate(QuestionOptionBase):
    pass


class QuestionOptionUpdate(QuestionOptionBase):
    content: Optional[str] = None
    is_correct: Optional[bool] = None


class QuestionOptionInDBBase(QuestionOptionBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


class QuestionOption(QuestionOptionInDBBase):
    pass


class QuestionBase(BaseModel):
    content: str
    question_type: str
    difficulty: str
    points: float


class QuestionCreate(QuestionBase):
    options: Optional[List[QuestionOptionCreate]] = None


class QuestionUpdate(QuestionBase):
    content: Optional[str] = None
    question_type: Optional[str] = None
    difficulty: Optional[str] = None
    points: Optional[float] = None
    options: Optional[List[QuestionOptionCreate]] = None


class QuestionInDBBase(QuestionBase):
    id: int
    exam_id: int

    class Config:
        orm_mode = True


class Question(QuestionInDBBase):
    options: List[QuestionOption] = []


class ExamVariantBase(BaseModel):
    variant_code: str
    file_path: str
    answer_key_path: str


class ExamVariantCreate(ExamVariantBase):
    pass


class ExamVariantUpdate(ExamVariantBase):
    variant_code: Optional[str] = None
    file_path: Optional[str] = None
    answer_key_path: Optional[str] = None


class ExamVariantInDBBase(ExamVariantBase):
    id: int
    exam_id: int

    class Config:
        orm_mode = True


class ExamVariant(ExamVariantInDBBase):
    pass


class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: int
    exam_type: str
    creation_date: str


class ExamCreate(ExamBase):
    questions: Optional[List[QuestionCreate]] = None


class ExamUpdate(ExamBase):
    title: Optional[str] = None
    course_id: Optional[int] = None
    exam_type: Optional[str] = None
    creation_date: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None


class ExamInDBBase(ExamBase):
    id: int
    created_by_id: int
    file_path: Optional[str] = None
    answer_key_path: Optional[str] = None

    class Config:
        orm_mode = True


class Exam(ExamInDBBase):
    questions: List[Question] = []
    exam_variants: List[ExamVariant] = []