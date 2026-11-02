# NotaApp - Asistencia Digital Familiar

NotaApp es una aplicación web progresiva (PWA) diseñada para ayudar a adultos mayores y personas con poca experiencia tecnológica a centralizar su información importante (cuentas, teléfonos, notas y recordatorios) de forma segura y sencilla.

## Tecnologías
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** Python + FastAPI + Pydantic + Uvicorn
- **Base de Datos:** PostgreSQL alojado en Supabase
- **Seguridad:** Autenticación por JWT, variables de entorno protegidas.

## Cómo ejecutar en local
1. Clonar el repositorio.
2. Crear un entorno virtual: `python -m venv .venv`
3. Activar el entorno: `source .venv/Scripts/activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Configurar el archivo `.env` en la carpeta `backend` con las credenciales de Supabase.
6. Ejecutar el servidor: `uvicorn main:app --reload` (dentro de la carpeta backend).
7. Abrir el navegador en `http://127.0.0.1:8000`

## Funcionalidades Implementadas (Entrega 4/5)
- Login simulado por PIN con generación de Token JWT.
- CRUD completo de Cuentas (con ofuscación de contraseña).
- CRUD de Teléfonos.
- CRUD de Notas.
- CRUD de Recordatorios.
- Dashboard interactivo.