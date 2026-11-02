# 📊 PROGRESO — NotaApp

## 🎯 Estado actual
- Fase en curso: Fase D — MVP Conectado
- Branch activa: `dev`

## ✅ Lo que se hizo (última sesión)
- `.venv` creado y funcional.
- Dependencias base instaladas: fastapi, uvicorn, pydantic, supabase.

## 🔜 Lo que sigue (próxima sesión)
- Crear `backend/main.py` con conexión a Supabase y una ruta de prueba.
- Crear `frontend/index.html` que consuma esa ruta.
- Servir el frontend desde FastAPI.
- Escribir el `README.md`.

## 🐳 Estado de Docker
- ¿Corriendo? NO
- Última imagen construida: (ninguna todavía)

## 🧠 Decisiones tomadas
- Dev diario con `.venv`; Docker solo para entrega final.
- Frontend servido por FastAPI (StaticFiles) como Plan A, nginx como Plan B.
- Supabase en la nube (sin Postgres local).