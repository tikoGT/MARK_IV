# main.py
import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.database import Base, engine, SessionLocal, get_db
from app.core.config import settings
from app.api import api_router
from app import crud
from app.schemas.users import UserCreate

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar plantillas
templates = Jinja2Templates(directory="templates")

# Incluir routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Crear usuario administrador si no existe
@app.on_event("startup")
def create_superuser():
    db = SessionLocal()
    try:
        user = crud.get_by_email(db, email=settings.ADMIN_EMAIL)
        if not user:
            user_in = UserCreate(
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                full_name="Administrador",
                is_superuser=True,
            )
            crud.create(db, obj_in=user_in)
    finally:
        db.close()

# Rutas frontend
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": {"full_name": "Administrador"}})

@app.get("/courses")
async def courses(request: Request):
    return templates.TemplateResponse("courses/index.html", {"request": request, "user": {"full_name": "Administrador"}})

@app.get("/sections")
async def sections(request: Request):
    return templates.TemplateResponse("sections/index.html", {"request": request, "user": {"full_name": "Administrador"}})

@app.get("/students")
async def students(request: Request):
    return templates.TemplateResponse("students/index.html", {"request": request, "user": {"full_name": "Administrador"}})

@app.get("/exams")
async def exams(request: Request):
    return templates.TemplateResponse("exams/index.html", {"request": request, "user": {"full_name": "Administrador"}})

@app.get("/settings")
async def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request, "user": {"full_name": "Administrador"}})


# Carpetas de almacenamiento
os.makedirs("storage/courses", exist_ok=True)
os.makedirs("storage/exams", exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)