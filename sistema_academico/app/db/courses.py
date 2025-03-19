# app/db/courses.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

# Tabla intermedia para relación muchos a muchos entre Course y Material
course_material = Table(
    'course_material',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('material_id', Integer, ForeignKey('materials.id'))
)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relaciones
    created_by = relationship("User", back_populates="courses")
    sections = relationship("Section", back_populates="course")
    materials = relationship("Material", secondary=course_material, back_populates="courses")
    exams = relationship("Exam", back_populates="course")

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    course = relationship("Course", back_populates="sections")
    enrollments = relationship("Enrollment", back_populates="section")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    identification = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    enrollments = relationship("Enrollment", back_populates="student")
    grades = relationship("Grade", back_populates="student")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    section_id = Column(Integer, ForeignKey("sections.id"))
    enrollment_date = Column(String)  # Se almacenará como fecha ISO
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    student = relationship("Student", back_populates="enrollments")
    section = relationship("Section", back_populates="enrollments")
    grades = relationship("Grade", back_populates="enrollment")

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    file_path = Column(String)
    file_type = Column(String)  # 'pdf', 'docx', etc.
    uploaded_by_id = Column(Integer, ForeignKey("users.id"))
    upload_date = Column(String)  # Se almacenará como fecha ISO
    
    # Relaciones
    uploaded_by = relationship("User")
    courses = relationship("Course", secondary=course_material, back_populates="materials")

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey("courses.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    exam_type = Column(String)  # 'parcial', 'final', 'repaso'
    creation_date = Column(String)  # Se almacenará como fecha ISO
    file_path = Column(String)  # Ruta al archivo generado
    answer_key_path = Column(String)  # Ruta a la plantilla de respuestas
    
    # Relaciones
    course = relationship("Course", back_populates="exams")
    created_by = relationship("User")
    questions = relationship("Question", back_populates="exam")
    exam_variants = relationship("ExamVariant", back_populates="exam")
    grades = relationship("Grade", back_populates="exam")

class ExamVariant(Base):
    __tablename__ = "exam_variants"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    variant_code = Column(String)  # Como "A", "B", etc.
    file_path = Column(String)
    answer_key_path = Column(String)
    
    # Relaciones
    exam = relationship("Exam", back_populates="exam_variants")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    content = Column(Text)
    question_type = Column(String)  # 'multiple_choice', 'open', 'calculation'
    difficulty = Column(String)  # 'easy', 'medium', 'hard'
    points = Column(Float)
    
    # Relaciones
    exam = relationship("Exam", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question")

class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    content = Column(Text)
    is_correct = Column(Boolean, default=False)
    
    # Relaciones
    question = relationship("Question", back_populates="options")

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    score = Column(Float)
    comments = Column(Text)
    graded_by_id = Column(Integer, ForeignKey("users.id"))
    grading_date = Column(String)  # Se almacenará como fecha ISO
    
    # Relaciones
    student = relationship("Student", back_populates="grades")
    enrollment = relationship("Enrollment", back_populates="grades")
    exam = relationship("Exam", back_populates="grades")
    graded_by = relationship("User")