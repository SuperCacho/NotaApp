# 📱 NotaApp - Asistencia Digital Familiar

![Estado del Proyecto](https://img.shields.io/badge/Estado-Entrega%20Final-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.142-teal)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 📖 Descripción del Proyecto

**NotaApp** es una Aplicación Web Progresiva (PWA) diseñada específicamente para actuar como un gestor de información personal centralizado. Su objetivo principal es asistir a adultos mayores y personas con poca experiencia tecnológica, permitiéndoles guardar, organizar y encontrar información crucial de manera sencilla y segura.

A diferencia de los gestores de contraseñas tradicionales, NotaApp pone el foco en la **accesibilidad visual y la simplicidad de uso**, ofreciendo una interfaz intuitiva con botones grandes, categorías claras y un modelo de roles que permite a un familiar o cuidador (Asistente) ayudar al dueño de los datos (Titular).

## ✨ Funcionalidades Principales

El sistema cuenta con un CRUD completo (Crear, Leer, Editar y Eliminar) para los siguientes módulos:

*   **🔒 Cuentas Digitales:** Almacenamiento seguro de servicios (correos, redes sociales, streaming) con contraseñas enmascaradas visualmente.
*   **📞 Teléfonos Importantes:** Agenda de contactos categorizada (Familiares, Médicos, Emergencias, Servicios) con botónera de acceso rápido.
*   **📝 Notas Protegidas:** Espacio para almacenar información breve y sensible (ej. pólizas de seguro, datos médicos), organizada por categorías.
*   **⏰ Recordatorios:** Gestión de eventos futuros vinculados a fechas y horas específicas, con estados de urgencia (Pendiente, Urgente, Realizado).

### Características Técnicas Destacadas
*   **Autenticación Segura:** Registro e inicio de sesión gestionados por Supabase Auth, con validación de sesión mediante tokens JWT.
*   **Feedback Visual (UX):** Uso de *spinners* (ruedas de carga) en botones y pantallas para indicar al usuario que el sistema está procesando información.
*   **Modales Custom:** Interfaz limpia libre de ventanas emergentes del navegador; las confirmaciones de borrado y formularios se manejan con modales propios de la app.
*   **Diseño Responsive:** Interfaz adaptada principalmente para dispositivos móviles, pero funcional en escritorio.

## 🛠️ Stack Tecnológico

La aplicación fue construida bajo una arquitectura cliente-servidor separada, contenerizada para garantizar su portabilidad.

### Frontend
*   **HTML5 & CSS3:** Estructura y diseño visual.
*   **JavaScript (Vanilla):** Lógica de interactividad, manejo del DOM y consumo de la API mediante `fetch`.
*   *(Diseño:* Paleta de colores de alto contraste basada en crema, teal y naranja, pensada para baja visión).

### Backend
*   **Python 3.12:** Lenguaje base del servidor.
*   **FastAPI:** Framework web moderno para la creación de la API REST.
*   **Pydantic:** Validación estricta de datos de entrada (schemas) y manejo de errores.
*   **Uvicorn:** Servidor ASGI para correr la aplicación.

### Base de Datos y Autenticación
*   **PostgreSQL:** Base de datos relacional.
*   **Supabase:** Plataforma BaaS (Backend as a Service) utilizada para alojar la base de datos y gestionar la autenticación de usuarios (manejo de `auth.users` y `profiles`).

### DevOps e Infraestructura
*   **Docker & Docker Compose:** La aplicación completa (Backend + Frontend estático) se empaqueta y ejecuta dentro de un contenedor, facilitando el despliegue y evitando problemas de compatibilidad de entorno.

## 🏗️ Estructura del Repositorio

El proyecto sigue una estructura de responsabilidades separadas (3 capas):

```text
NotaApp/
│
├── backend/                  # Servidor FastAPI
│   ├── app/
│   │   ├── database/         # Conexión a Supabase
│   │   ├── routers/          # Endpoints de la API (auth, cuentas, etc.)
│   │   ├── schemas/          # Modelos de validación (Pydantic)
│   │   └── services/         # Lógica de negocio y seguridad (JWT)
│   ├── requirements.txt      # Dependencias de Python
│   └── .env                  # Variables de entorno (NO subido a Git)
│
├── frontend/                 # Interfaz de usuario
│   ├── css/                  # Estilos
│   ├── js/                   # Lógica de JavaScript (app.js)
│   └── index.html            # Estructura principal
│
├── Dockerfile                # Receta de construcción de la imagen Docker
├── docker-compose.yml        # Orquestación del contenedor
└── README.md
