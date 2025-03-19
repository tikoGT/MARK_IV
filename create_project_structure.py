# create_project_structure.py
import os
import sys

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Creada carpeta: {path}")

def create_file(path, content=""):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Creado archivo: {path}")

def create_project_structure(base_dir):
    # Directorios principales
    create_directory(os.path.join(base_dir, "app"))
    create_directory(os.path.join(base_dir, "app", "api"))
    create_directory(os.path.join(base_dir, "app", "core"))
    create_directory(os.path.join(base_dir, "app", "crud"))
    create_directory(os.path.join(base_dir, "app", "db"))
    create_directory(os.path.join(base_dir, "app", "schemas"))
    create_directory(os.path.join(base_dir, "app", "services"))
    create_directory(os.path.join(base_dir, "app", "static", "css"))
    create_directory(os.path.join(base_dir, "app", "static", "js"))
    create_directory(os.path.join(base_dir, "app", "static", "images"))
    create_directory(os.path.join(base_dir, "templates"))
    create_directory(os.path.join(base_dir, "templates", "courses"))
    create_directory(os.path.join(base_dir, "templates", "students"))
    create_directory(os.path.join(base_dir, "templates", "exams"))
    create_directory(os.path.join(base_dir, "storage", "courses"))
    create_directory(os.path.join(base_dir, "storage", "exams"))
    create_directory(os.path.join(base_dir, "alembic", "versions"))
    create_directory(os.path.join(base_dir, "tests"))

    # Archivos de inicialización
    for module in ["app", "app/api", "app/core", "app/crud", "app/db", "app/schemas", "app/services", "tests"]:
        create_file(os.path.join(base_dir, module, "__init__.py"))

    # Archivos principales
    requirements_content = """fastapi==0.75.1
uvicorn==0.17.6
sqlalchemy==1.4.36
pydantic==1.9.0
passlib==1.7.4
python-jose==3.3.0
python-multipart==0.0.5
bcrypt==3.2.0
alembic==1.7.7
jinja2==3.1.1
aiofiles==0.8.0
python-dotenv==0.20.0
PyPDF2==2.6.0
python-docx==0.8.11
pillow==9.1.0
"""
    create_file(os.path.join(base_dir, "requirements.txt"), requirements_content)

    env_content = """# Variables de entorno
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./app.db
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
"""
    create_file(os.path.join(base_dir, ".env"), env_content)

    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
*.egg-info/
*.egg

# IDE
.idea/
.vscode/
*.swp

# SQLite
*.db
*.sqlite3

# Environment variables
.env

# Storage
storage/*/
"""
    create_file(os.path.join(base_dir, ".gitignore"), gitignore_content)

if __name__ == "__main__":
    base_dir = sys.argv[1] if len(sys.argv) > 1 else "sistema_academico"
    create_project_structure(base_dir)
    print(f"Estructura creada en: {base_dir}")