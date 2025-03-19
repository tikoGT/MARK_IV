# app/api/exams.py
import os
import uuid
import datetime
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import crud
from app.api.auth import get_current_active_user
from app.database import get_db
from app.schemas.exams import Exam, ExamCreate, Question, QuestionCreate, ExamVariant
from app.schemas.users import User
from app.services.document_processor import DocumentProcessor
from app.services.exam_generator import ExamGenerator

router = APIRouter()


class ExamConfig(BaseModel):
    title: str
    description: Optional[str] = None
    exam_type: str
    num_questions: int = 20
    num_concepts: int = 10
    num_options: int = 4
    difficulty_distribution: dict = {"easy": 0.3, "medium": 0.5, "hard": 0.2}
    question_type_distribution: dict = {"multiple_choice": 0.7, "open": 0.3}
    generate_variants: bool = False
    num_variants: int = 1


@router.get("/", response_model=List[Exam])
def read_exams(
    db: Session = Depends(get_db),
    course_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtener todos los exámenes, opcionalmente filtrados por curso
    """
    if course_id:
        # Aquí necesitaríamos una función para obtener exámenes por curso
        # Por ahora, retornamos una lista vacía
        exams = []
    else:
        # Aquí necesitaríamos una función para obtener todos los exámenes
        # Por ahora, retornamos una lista vacía
        exams = []
    return exams


@router.post("/generate", response_model=Exam)
async def generate_exam(
    background_tasks: BackgroundTasks,
    course_id: int = Form(...),
    config: ExamConfig = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Generar un examen basado en los materiales de un curso
    """
    # Verificar que el curso existe
    course = crud.get_course(db=db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Obtener materiales del curso
    materials = crud.get_materials_by_course(db=db, course_id=course_id)
    
    if not materials:
        raise HTTPException(
            status_code=400, 
            detail="El curso no tiene materiales para generar un examen"
        )
    
    # Procesar materiales
    processed_materials = []
    for material in materials:
        processed_content = DocumentProcessor.process_document(material.file_path)
        processed_materials.append(processed_content)
    
    # Crear configuración del examen
    exam_config = {
        'title': config.title,
        'description': config.description,
        'num_questions': config.num_questions,
        'num_concepts': config.num_concepts,
        'num_options': config.num_options,
        'difficulty_distribution': config.difficulty_distribution,
        'question_type_distribution': config.question_type_distribution
    }
    
    # Generar examen
    try:
        generated_exam = ExamGenerator.create_exam_from_materials(
            processed_materials, 
            exam_config
        )
        
        # Crear directorios para exámenes si no existen
        exam_dir = f"storage/exams/{course_id}"
        os.makedirs(exam_dir, exist_ok=True)
        
        # Generar nombre único para el archivo
        exam_id = str(uuid.uuid4())
        exam_file = f"{exam_dir}/{exam_id}.docx"
        answer_key_file = f"{exam_dir}/{exam_id}_answers.docx"
        
        # Generar archivos DOCX
        ExamGenerator.generate_exam_docx(generated_exam, exam_file, include_answers=False)
        ExamGenerator.generate_exam_docx(generated_exam, answer_key_file, include_answers=True)
        
        # Generar hoja de respuestas
        answer_sheet_file = f"{exam_dir}/{exam_id}_answer_sheet.docx"
        ExamGenerator.generate_answer_sheet(generated_exam, answer_sheet_file)
        
        # Crear examen en la base de datos
        exam_create = ExamCreate(
            title=config.title,
            description=config.description,
            course_id=course_id,
            exam_type=config.exam_type,
            creation_date=datetime.datetime.utcnow().isoformat(),
            questions=[]
        )
        
        # Agregar preguntas
        for question_data in generated_exam["questions"]:
            options = []
            if question_data.get("question_type") == "multiple_choice" and "options" in question_data:
                for option_text in question_data["options"]:
                    is_correct = option_text == question_data.get("answer", "")
                    options.append({
                        "content": option_text,
                        "is_correct": is_correct
                    })
            
            question = QuestionCreate(
                content=question_data["content"],
                question_type=question_data["question_type"],
                difficulty=question_data["difficulty"],
                points=question_data["points"],
                options=options
            )
            exam_create.questions.append(question)
        
        # Crear examen (esto requeriría una función en CRUD que no tenemos implementada)
        # Por ahora, retornamos un examen simulado
        exam = {
            "id": 1,
            "title": config.title,
            "description": config.description,
            "course_id": course_id,
            "created_by_id": current_user.id,
            "exam_type": config.exam_type,
            "creation_date": datetime.datetime.utcnow().isoformat(),
            "file_path": exam_file,
            "answer_key_path": answer_key_file,
            "questions": generated_exam["questions"],
            "exam_variants": []
        }
        
        # Si se solicitaron variantes, generarlas
        if config.generate_variants and config.num_variants > 1:
            # Aquí se implementaría la generación de variantes
            # Por ahora, solo simulamos
            for i in range(config.num_variants):
                variant_id = f"{exam_id}_variant_{i+1}"
                variant_file = f"{exam_dir}/{variant_id}.docx"
                variant_answer_file = f"{exam_dir}/{variant_id}_answers.docx"
                
                # Simular la creación de archivos (en una implementación real se generarían variantes)
                with open(exam_file, 'rb') as src:
                    with open(variant_file, 'wb') as dst:
                        dst.write(src.read())
                
                with open(answer_key_file, 'rb') as src:
                    with open(variant_answer_file, 'wb') as dst:
                        dst.write(src.read())
                
                exam["exam_variants"].append({
                    "id": i+1,
                    "exam_id": 1,
                    "variant_code": chr(65 + i),  # A, B, C, ...
                    "file_path": variant_file,
                    "answer_key_path": variant_answer_file
                })
        
        return exam
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el examen: {str(e)}"
        )


@router.get("/download/{exam_id}")
async def download_exam(
    exam_id: int,
    include_answers: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Descargar un examen generado
    """
    # Aquí necesitaríamos obtener el examen de la base de datos
    # Por ahora, simulamos con una ruta de archivo fija
    
    # En una implementación real buscaríamos el examen en la BD
    # exam = crud.get_exam(db=db, exam_id=exam_id)
    # if not exam:
    #     raise HTTPException(status_code=404, detail="Examen no encontrado")
    
    # Simular archivo de examen
    file_path = "storage/exams/1/example.docx"
    
    if include_answers:
        file_path = "storage/exams/1/example_answers.docx"
    
    # Verificar que el archivo existe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@router.get("/answer-sheet/{exam_id}")
async def download_answer_sheet(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Descargar la hoja de respuestas de un examen
    """
    # Simulamos con una ruta de archivo fija
    file_path = "storage/exams/1/example_answer_sheet.docx"
    
    # Verificar que el archivo existe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )