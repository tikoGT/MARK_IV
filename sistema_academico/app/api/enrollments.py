# app/api/enrollments.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.auth import get_current_active_user
from app.database import get_db
from app.schemas.students import Enrollment, EnrollmentUpdate, Grade, GradeCreate
from app.schemas.users import User

router = APIRouter()


@router.get("/", response_model=List[Enrollment])
def read_enrollments(
    db: Session = Depends(get_db),
    student_id: int = None,
    section_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener todas las inscripciones, opcionalmente filtradas por estudiante o sección
    """
    if student_id:
        enrollments = crud.get_enrollments_by_student(db, student_id=student_id, skip=skip, limit=limit)
    elif section_id:
        enrollments = crud.get_enrollments_by_section(db, section_id=section_id, skip=skip, limit=limit)
    else:
        # Aquí necesitaríamos una función para obtener todas las inscripciones
        # Por ahora, retornamos una lista vacía
        enrollments = []
    return enrollments


@router.get("/{enrollment_id}", response_model=Enrollment)
def read_enrollment(
    *,
    db: Session = Depends(get_db),
    enrollment_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener una inscripción por ID
    """
    enrollment = crud.get_enrollment(db=db, enrollment_id=enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return enrollment


@router.put("/{enrollment_id}", response_model=Enrollment)
def update_enrollment(
    *,
    db: Session = Depends(get_db),
    enrollment_id: int,
    enrollment_in: EnrollmentUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Actualizar inscripción
    """
    enrollment = crud.get_enrollment(db=db, enrollment_id=enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    
    # Si se está cambiando el estudiante o la sección, verificar que existan
    if enrollment_in.student_id and enrollment_in.student_id != enrollment.student_id:
        student = crud.get_student(db, student_id=enrollment_in.student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    if enrollment_in.section_id and enrollment_in.section_id != enrollment.section_id:
        section = crud.get_section(db, section_id=enrollment_in.section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Sección no encontrada")
    
    enrollment = crud.update_enrollment(db=db, db_obj=enrollment, obj_in=enrollment_in)
    return enrollment


@router.delete("/{enrollment_id}", response_model=bool)
def delete_enrollment(
    *,
    db: Session = Depends(get_db),
    enrollment_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Desactivar inscripción
    """
    enrollment = crud.get_enrollment(db=db, enrollment_id=enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    result = crud.delete_enrollment(db=db, enrollment_id=enrollment_id)
    return result


@router.get("/{enrollment_id}/grades", response_model=List[Grade])
def read_enrollment_grades(
    *,
    db: Session = Depends(get_db),
    enrollment_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener todas las calificaciones de una inscripción
    """
    enrollment = crud.get_enrollment(db=db, enrollment_id=enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    
    grades = crud.get_grades_by_enrollment(
        db=db, enrollment_id=enrollment_id, skip=skip, limit=limit
    )
    return grades


@router.post("/{enrollment_id}/grades", response_model=Grade)
def create_enrollment_grade(
    *,
    db: Session = Depends(get_db),
    enrollment_id: int,
    exam_id: int,
    score: float,
    comments: str = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Registrar una calificación para una inscripción
    """
    import datetime
    
    # Verificar que la inscripción existe
    enrollment = crud.get_enrollment(db=db, enrollment_id=enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    
    # Verificar que el examen existe
    exam = crud.get_exam(db=db, exam_id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Examen no encontrado")
    
    # Verificar si ya existe una calificación para este examen
    grades = crud.get_grades_by_enrollment(db=db, enrollment_id=enrollment_id)
    for grade in grades:
        if grade.exam_id == exam_id:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una calificación para este examen",
            )
    
    # Crear calificación
    grade_in = GradeCreate(
        student_id=enrollment.student_id,
        enrollment_id=enrollment_id,
        exam_id=exam_id,
        score=score,
        comments=comments,
        graded_by_id=current_user.id,
        grading_date=datetime.datetime.utcnow().isoformat(),
    )
    
    grade = crud.create_grade(db=db, grade_in=grade_in)
    return grade