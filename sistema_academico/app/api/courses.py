# app/api/courses.py
import os
import shutil
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud
from app.api.auth import get_current_active_user
from app.database import get_db
from app.schemas.courses import Course, CourseCreate, CourseUpdate, Material, MaterialCreate
from app.schemas.users import User

router = APIRouter()


def save_upload_file(file_path: str, file: UploadFile):
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


@router.get("/", response_model=List[Course])
def read_courses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener todos los cursos
    """
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses


@router.post("/", response_model=Course)
def create_course(
    *,
    db: Session = Depends(get_db),
    course_in: CourseCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Crear nuevo curso
    """
    course = crud.create_course(db=db, course_in=course_in, user_id=current_user.id)
    return course


@router.get("/{course_id}", response_model=Course)
def read_course(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener un curso por ID
    """
    course = crud.get_course(db=db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return course


@router.put("/{course_id}", response_model=Course)
def update_course(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    course_in: CourseUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Actualizar curso
    """
    course = crud.get_course(db=db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    course = crud.update_course(db=db, db_obj=course, obj_in=course_in)
    return course


@router.delete("/{course_id}", response_model=bool)
def delete_course(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Desactivar curso
    """
    course = crud.get_course(db=db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    result = crud.delete_course(db=db, course_id=course_id)
    return result


@router.post("/{course_id}/materials", response_model=Material)
async def create_course_material(
    background_tasks: BackgroundTasks,
    course_id: int,
    title: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Subir material para un curso
    """
    course = crud.get_course(db=db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Determinar tipo de archivo
    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()
    file_type = "unknown"
    
    if file_extension in [".pdf"]:
        file_type = "pdf"
    elif file_extension in [".doc", ".docx"]:
        file_type = "docx"
    elif file_extension in [".ppt", ".pptx"]:
        file_type = "pptx"
    elif file_extension in [".txt"]:
        file_type = "txt"
    else:
        raise HTTPException(
            status_code=400, 
            detail="Tipo de archivo no soportado. Use PDF, DOCX, PPTX o TXT."
        )
    
    # Crear directorio del curso si no existe
    course_dir = f"storage/courses/{course_id}"
    os.makedirs(course_dir, exist_ok=True)
    
    # Construir ruta para guardar el archivo
    import uuid
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"{course_dir}/{unique_filename}"
    
    # Guardar archivo en background para no bloquear
    background_tasks.add_task(save_upload_file, file_path, file)
    
    # Crear material en la base de datos
    material_in = MaterialCreate(
        title=title,
        description=description,
        file_type=file_type
    )
    material = crud.create_material(
        db=db,
        material_in=material_in,
        user_id=current_user.id,
        file_path=file_path,
        course_id=course_id
    )
    
    return material


@router.get("/{course_id}/materials", response_model=List[Material])
def read_course_materials(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener todos los materiales de un curso
    """
    course = crud.get_course(db=db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    materials = crud.get_materials_by_course(
        db=db, course_id=course_id, skip=skip, limit=limit
    )
    return materials