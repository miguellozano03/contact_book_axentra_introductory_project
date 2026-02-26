@echo off
SETLOCAL

REM Crear virtualenv si no existe
IF NOT EXIST env (
    echo Creating virtual environment...
    python -m venv env
)

REM Activar virtualenv
call env\Scripts\activate

REM Instalar dependencias
echo Installing dependencies...
pip install -r requirements.txt

REM Ir a src
cd src || exit /b

REM Aplicar migraciones
echo Applying migrations...
alembic upgrade head

REM Levantar server
echo Starting server...
uvicorn app.main:app --reload