# app/api/sections.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.auth import get_current_active_user
from app.database import get_db
from app.schemas.courses import Section, SectionCreate, SectionUpdate
from app.schemas.students import Enrollment, EnrollmentCreate
from app.schemas.users import User

router = APIRouter()


@router.get("/", response_model=List[Section])
def read_sections(
    db: Session = Depends(get_db),
    course_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener todas las secciones, opcionalmente filtradas por curso
    """
    if course_id:
        sections = crud.get_sections_by_course(db, course_id=course_id, skip=skip, limit=limit)
    else:
        # Aquí necesitaríamos una función para obtener todas las secciones
        # Por ahora, retornamos una lista vacía
        sections = []
    return sections


@router.post("/", response_model=Section)
def create_section(
    *,
    db: Session = Depends(get_db),
    section_in: SectionCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Crear nueva sección
    """
    # Verificar que el curso exista
    course = crud.get_course(db, course_id=section_in.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    section = crud.create_section(db=db, section_in=section_in)
    return section


@router.get("/{section_id}", response_model=Section)
def read_section(
    *,
    db: Session = Depends(get_db),
    section_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener una sección por ID
    """
    section = crud.get_section(db=db, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return section


@router.put("/{section_id}", response_model=Section)
def update_section(
    *,
    db: Session = Depends(get_db),
    section_id: int,
    section_in: SectionUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Actualizar sección
    """
    section = crud.get_section(db=db, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    
    # Si se está cambiando el curso, verificar que exista
    if section_in.course_id and section_in.course_id != section.course_id:
        course = crud.get_course(db, course_id=section_in.course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    section = crud.update_section(db=db, db_obj=section, obj_in=section_in)
    return section


@router.delete("/{section_id}", response_model=bool)
def delete_section(
    *,
    db: Session = Depends(get_db),
    section_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Desactivar sección
    """
    section = crud.get_section(db=db, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    result = crud.delete_section(db=db, section_id=section_id)
    return result


@router.get("/{section_id}/enrollments", response_model=List[Enrollment])
def read_section_enrollments(
    *,
    db: Session = Depends(get_db),
    section_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener todas las inscripciones de una sección
    """
    section = crud.get_section(db=db, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    
    enrollments = crud.get_enrollments_by_section(
        db=db, section_id=section_id, skip=skip, limit=limit
    )
    return enrollments


@router.post("/{section_id}/enrollments", response_model=Enrollment)
def create_section_enrollment(
    *,
    db: Session = Depends(get_db),
    section_id: int,
    student_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Inscribir un estudiante en una sección
    """
    import datetime
    
    # Verificar que la sección existe
    section = crud.get_section(db=db, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    
    # Verificar que el estudiante existe
    student = crud.get_student(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Verificar si ya está inscrito
    enrollments = crud.get_enrollments_by_section(db=db, section_id=section_id)
    for enrollment in enrollments:
        if enrollment.student_id == student_id and enrollment.is_active:
            raise HTTPException(
                status_code=400,
                detail="El estudiante ya está inscrito en esta sección",
            )
    
    # Crear inscripción
    enrollment_in = EnrollmentCreate(
        student_id=student_id,
        section_id=section_id,
        enrollment_date=datetime.datetime.utcnow().isoformat(),
        is_active=True,
    )
    
    enrollment = crud.create_enrollment(db=db, enrollment_in=enrollment_in)
    return enrollment