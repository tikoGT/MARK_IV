# app/api/materials.py
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import mimetypes

from app import crud
from app.api.auth import get_current_active_user
from app.database import get_db
from app.schemas.users import User

router = APIRouter()

@router.get("/{material_id}/download")
async def download_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Descargar un material por su ID"""
    material = crud.get_material(db=db, material_id=material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    
    if not os.path.exists(material.file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    filename = os.path.basename(material.file_path)
    
    content_type = None
    if material.file_type == 'pdf':
        content_type = 'application/pdf'
    elif material.file_type in ['doc', 'docx']:
        content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    else:
        content_type, _ = mimetypes.guess_type(material.file_path)
    
    return FileResponse(
        path=material.file_path,
        filename=filename,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename=\"{filename}\""}
    )

@router.get("/{material_id}/view")
async def view_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Ver un material en el navegador"""
    material = crud.get_material(db=db, material_id=material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    
    if not os.path.exists(material.file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    content_type = None
    if material.file_type == 'pdf':
        content_type = 'application/pdf'
        return FileResponse(
            path=material.file_path,
            media_type=content_type,
            headers={"Content-Disposition": "inline"}
        )
    else:
        filename = os.path.basename(material.file_path)
        return FileResponse(
            path=material.file_path,
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename=\"{filename}\""}
        )