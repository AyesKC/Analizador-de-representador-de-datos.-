# Analizador de representación de datos

Aplicación web en Python 3.12 + Django que relaciona sistemas numéricos,
codificación de caracteres (UTF-8) y ejecución en contenedores.

## Ejecutar con Docker
    docker compose up --build
    # abrir http://localhost:8000

## Ejecutar sin Docker
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python manage.py runserver

## Pruebas
    python manage.py test
