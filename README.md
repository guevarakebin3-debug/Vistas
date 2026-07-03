# DJANGO_PRACTICA

Proyecto Django de práctica con una aplicación `empleados` para gestionar cargos y empleados.

## Descripción

Este proyecto contiene un sitio Django con:
- App `empleados` registrada en `INSTALLED_APPS`
- Plantillas para CRUD de empleados y cargos
- Base de datos SQLite local

## Requisitos

- Python 3.11+ (u otra versión compatible con Django 6.0.6)
- `pip`

## Instalación

1. Crear y activar un entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Aplicar migraciones:

```bash
python manage.py migrate
```

4. Ejecutar el servidor:

```bash
python manage.py runserver
```

5. Abrir en el navegador:

```text
http://127.0.0.1:8000/
```

## Estructura del proyecto

- `manage.py`: comando principal de Django
- `Djangoproyecto/`: configuración del proyecto
- `empleados/`: aplicación de ejemplo con modelos, vistas, formularios y plantillas
- `requirements.txt`: dependencias utilizadas

## Uso de Git / GitHub

1. Inicializar el repositorio si aún no existe:

```bash
git init
```

2. Agregar archivos y hacer commit:

```bash
git add .
git commit -m "Initial commit"
```

3. Crear un repositorio remoto en GitHub y conectar el remoto:

```bash
git remote add origin https://github.com/USUARIO/NOMBRE_REPO.git
```

4. Subir al remoto:

```bash
git branch -M main
git push -u origin main
```
