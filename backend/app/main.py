import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import auth, cuentas

app = FastAPI(title="NotaApp API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cuentas.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Configuración para servir el frontend desde Docker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Como este archivo está en backend/app/main.py, subimos dos niveles para llegar a la raíz y entrar a frontend
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "..", "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    print(f"ADVERTENCIA: No se encontró la carpeta frontend en {FRONTEND_DIR}")
