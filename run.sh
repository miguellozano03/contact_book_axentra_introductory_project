#!/bin/bash

if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python -m venv env
fi

# Activar virtualenv
source env/bin/activate

# Instalar dependencias
echo "Installing dependencies..."
pip install -r requirements.txt

# Ir a src
cd src || exit

# Aplicar migraciones
echo "Applying migrations..."
alembic upgrade head

# Levantar server
echo "Starting server..."
uvicorn app.main:app --reload