# app/api/students.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.auth import get_current_active_user
from app.database import get_db
from app.schemas.students import Student, StudentCreate, StudentUpdate
from app.schemas.users import User

router = APIRouter()


@router.get("/", response_model=List[Student])
def read_students(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener todos los estudiantes
    """
    students = crud.get_students(db, skip=skip, limit=limit)
    return students


@router.post("/", response_model=Student)
def create_student(
    *,
    db: Session = Depends(get_db),
    student_in: StudentCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Crear nuevo estudiante
    """
    student = crud.get_student_by_email(db, email=student_in.email)
    if student:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un estudiante con este correo electrónico",
        )
    student = crud.get_student_by_identification(db, identification=student_in.identification)
    if student:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un estudiante con esta identificación",
        )
    student = crud.create_student(db=db, student_in=student_in)
    return student


@router.get("/{student_id}", response_model=Student)
def read_student(
    *,
    db: Session = Depends(get_db),
    student_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener un estudiante por ID
    """
    student = crud.get_student(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return student


@router.put("/{student_id}", response_model=Student)
def update_student(
    *,
    db: Session = Depends(get_db),
    student_id: int,
    student_in: StudentUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Actualizar estudiante
    """
    student = crud.get_student(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Verificar email único
    if student_in.email and student_in.email != student.email:
        existing = crud.get_student_by_email(db, email=student_in.email)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un estudiante con este correo electrónico",
            )
    
    # Verificar identificación única
    if student_in.identification and student_in.identification != student.identification:
        existing = crud.get_student_by_identification(db, identification=student_in.identification)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un estudiante con esta identificación",
            )
    
    student = crud.update_student(db=db, db_obj=student, obj_in=student_in)
    return student


@router.delete("/{student_id}", response_model=bool)
def delete_student(
    *,
    db: Session = Depends(get_db),
    student_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Desactivar estudiante
    """
    student = crud.get_student(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    result = crud.delete_student(db=db, student_id=student_id)
    return result