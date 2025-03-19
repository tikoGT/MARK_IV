# app/crud/__init__.py
from app.crud.users import get_by_email, get_by_id, create, update, authenticate, is_active, is_superuser
from app.crud.courses import (
    get_course, get_courses, get_courses_by_user, create_course, update_course, delete_course,
    get_section, get_sections_by_course, create_section, update_section, delete_section,
    get_material, get_materials_by_course, create_material, update_material, 
    add_material_to_course, remove_material_from_course
)
from app.crud.students import (
    get_student, get_student_by_email, get_student_by_identification, get_students, 
    create_student, update_student, delete_student,
    get_enrollment, get_enrollments_by_student, get_enrollments_by_section,
    create_enrollment, update_enrollment, delete_enrollment,
    get_grade, get_grades_by_student, get_grades_by_exam, get_grades_by_enrollment,
    create_grade, update_grade, delete_grade
)