# NotaApp - Asistencia Digital Familiar

NotaApp es una aplicación web progresiva (PWA) diseñada para centralizar la información importante de personas mayores o con poca experiencia tecnológica. Permite guardar cuentas digitales, teléfonos de contacto, notas personales protegidas y recordatorios, todo dentro de un entorno seguro y fácil de usar.

## Stack Tecnológico
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
*   **Backend:** Python 3.12 + FastAPI + Pydantic
*   **Base de Datos y Autenticación:** PostgreSQL en la nube mediante Supabase
*   **Contenedores:** Docker y Docker Compose para despliegue uniforme

## Estructura del Proyecto
*   `backend/`: Contiene la API REST, organizada en capas (`routers`, `schemas`, `services`).
*   `frontend/`: Contiene la interfaz de usuario con separación de HTML, CSS y JS.
*   `Dockerfile` y `docker-compose.yml`: Configuración para levantar la aplicación completa.

## Cómo ejecutar el proyecto en local

### Requisitos previos
*   Tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/).
*   Tener una cuenta en [Supabase](https://supabase.com/) con el proyecto creado y las tablas correspondientes.

### Pasos
1. Clonar el repositorio.
2. En la carpeta `backend/`, crear un archivo `.env` con las credenciales de Supabase:
   ```env
   SUPABASE_URL=tu_url_de_supabase
   SUPABASE_KEY=tu_service_role_key