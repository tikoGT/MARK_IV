# app/crud/courses.py
from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session

from app.db.courses import Course, Section, Material
from app.schemas.courses import CourseCreate, CourseUpdate, SectionCreate, SectionUpdate, MaterialCreate, MaterialUpdate


# --- Cursos ---
def get_course(db: Session, course_id: int) -> Optional[Course]:
    return db.query(Course).filter(Course.id == course_id).first()

def get_courses(
    db: Session, skip: int = 0, limit: int = 100, is_active: bool = True
) -> List[Course]:
    return db.query(Course).filter(Course.is_active == is_active).offset(skip).limit(limit).all()

def get_courses_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Course]:
    return db.query(Course).filter(Course.created_by_id == user_id).offset(skip).limit(limit).all()

def create_course(
    db: Session, course_in: CourseCreate, user_id: int
) -> Course:
    db_course = Course(
        name=course_in.name,
        description=course_in.description,
        is_active=course_in.is_active,
        created_by_id=user_id,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(
    db: Session, db_obj: Course, obj_in: Union[CourseUpdate, Dict[str, Any]]
) -> Course:
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

def delete_course(db: Session, course_id: int) -> bool:
    db_obj = db.query(Course).filter(Course.id == course_id).first()
    if db_obj:
        db_obj.is_active = False
        db.add(db_obj)
        db.commit()
        return True
    return False


# --- Secciones ---
def get_section(db: Session, section_id: int) -> Optional[Section]:
    return db.query(Section).filter(Section.id == section_id).first()

def get_sections_by_course(
    db: Session, course_id: int, skip: int = 0, limit: int = 100
) -> List[Section]:
    return db.query(Section).filter(Section.course_id == course_id).offset(skip).limit(limit).all()

def create_section(
    db: Session, section_in: SectionCreate
) -> Section:
    db_section = Section(
        name=section_in.name,
        course_id=section_in.course_id,
        is_active=section_in.is_active,
    )
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section

def update_section(
    db: Session, db_obj: Section, obj_in: Union[SectionUpdate, Dict[str, Any]]
) -> Section:
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

def delete_section(db: Session, section_id: int) -> bool:
    db_obj = db.query(Section).filter(Section.id == section_id).first()
    if db_obj:
        db_obj.is_active = False
        db.add(db_obj)
        db.commit()
        return True
    return False


# --- Materiales ---
def get_material(db: Session, material_id: int) -> Optional[Material]:
    return db.query(Material).filter(Material.id == material_id).first()

def get_materials_by_course(
    db: Session, course_id: int, skip: int = 0, limit: int = 100
) -> List[Material]:
    course = db.query(Course).filter(Course.id == course_id).first()
    if course:
        return course.materials[skip:skip+limit]
    return []

def create_material(
    db: Session, material_in: MaterialCreate, user_id: int, file_path: str, course_id: int = None
) -> Material:
    import datetime
    
    db_material = Material(
        title=material_in.title,
        description=material_in.description,
        file_type=material_in.file_type,
        file_path=file_path,
        uploaded_by_id=user_id,
        upload_date=datetime.datetime.utcnow().isoformat(),
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    
    # Si se especifica un curso, asociar el material
    if course_id:
        course = db.query(Course).filter(Course.id == course_id).first()
        if course:
            course.materials.append(db_material)
            db.commit()
    
    return db_material

def update_material(
    db: Session, db_obj: Material, obj_in: Union[MaterialUpdate, Dict[str, Any]]
) -> Material:
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

def add_material_to_course(db: Session, material_id: int, course_id: int) -> bool:
    material = db.query(Material).filter(Material.id == material_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if material and course:
        if material not in course.materials:
            course.materials.append(material)
            db.commit()
            return True
    return False

def remove_material_from_course(db: Session, material_id: int, course_id: int) -> bool:
    material = db.query(Material).filter(Material.id == material_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if material and course and material in course.materials:
        course.materials.remove(material)
        db.commit()
        return True
    return False