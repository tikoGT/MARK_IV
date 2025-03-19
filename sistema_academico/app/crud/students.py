# app/crud/students.py
from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session

from app.db.courses import Student, Enrollment, Grade
from app.schemas.students import StudentCreate, StudentUpdate, EnrollmentCreate, EnrollmentUpdate, GradeCreate, GradeUpdate


# --- Estudiantes ---
def get_student(db: Session, student_id: int) -> Optional[Student]:
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    return db.query(Student).filter(Student.email == email).first()

def get_student_by_identification(db: Session, identification: str) -> Optional[Student]:
    return db.query(Student).filter(Student.identification == identification).first()

def get_students(
    db: Session, skip: int = 0, limit: int = 100, is_active: bool = True
) -> List[Student]:
    return db.query(Student).filter(Student.is_active == is_active).offset(skip).limit(limit).all()

def create_student(
    db: Session, student_in: StudentCreate
) -> Student:
    db_student = Student(
        full_name=student_in.full_name,
        email=student_in.email,
        identification=student_in.identification,
        is_active=student_in.is_active,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(
    db: Session, db_obj: Student, obj_in: Union[StudentUpdate, Dict[str, Any]]
) -> Student:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_student(db: Session, student_id: int) -> bool:
    db_obj = db.query(Student).filter(Student.id == student_id).first()
    if db_obj:
        db_obj.is_active = False
        db.add(db_obj)
        db.commit()
        return True
    return False


# --- Inscripciones ---
def get_enrollment(db: Session, enrollment_id: int) -> Optional[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

def get_enrollments_by_student(
    db: Session, student_id: int, skip: int = 0, limit: int = 100
) -> List[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.student_id == student_id).offset(skip).limit(limit).all()

def get_enrollments_by_section(
    db: Session, section_id: int, skip: int = 0, limit: int = 100
) -> List[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.section_id == section_id).offset(skip).limit(limit).all()

def create_enrollment(
    db: Session, enrollment_in: EnrollmentCreate
) -> Enrollment:
    db_enrollment = Enrollment(
        student_id=enrollment_in.student_id,
        section_id=enrollment_in.section_id,
        enrollment_date=enrollment_in.enrollment_date,
        is_active=enrollment_in.is_active,
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def update_enrollment(
    db: Session, db_obj: Enrollment, obj_in: Union[EnrollmentUpdate, Dict[str, Any]]
) -> Enrollment:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_enrollment(db: Session, enrollment_id: int) -> bool:
    db_obj = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if db_obj:
        db_obj.is_active = False
        db.add(db_obj)
        db.commit()
        return True
    return False


# --- Calificaciones ---
def get_grade(db: Session, grade_id: int) -> Optional[Grade]:
    return db.query(Grade).filter(Grade.id == grade_id).first()

def get_grades_by_student(
    db: Session, student_id: int, skip: int = 0, limit: int = 100
) -> List[Grade]:
    return db.query(Grade).filter(Grade.student_id == student_id).offset(skip).limit(limit).all()

def get_grades_by_exam(
    db: Session, exam_id: int, skip: int = 0, limit: int = 100
) -> List[Grade]:
    return db.query(Grade).filter(Grade.exam_id == exam_id).offset(skip).limit(limit).all()

def get_grades_by_enrollment(
    db: Session, enrollment_id: int, skip: int = 0, limit: int = 100
) -> List[Grade]:
    return db.query(Grade).filter(Grade.enrollment_id == enrollment_id).offset(skip).limit(limit).all()

def create_grade(
    db: Session, grade_in: GradeCreate
) -> Grade:
    db_grade = Grade(
        student_id=grade_in.student_id,
        enrollment_id=grade_in.enrollment_id,
        exam_id=grade_in.exam_id,
        score=grade_in.score,
        comments=grade_in.comments,
        graded_by_id=grade_in.graded_by_id,
        grading_date=grade_in.grading_date,
    )
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

def update_grade(
    db: Session, db_obj: Grade, obj_in: Union[GradeUpdate, Dict[str, Any]]
) -> Grade:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_grade(db: Session, grade_id: int) -> bool:
    db_obj = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False