import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importamos todos los routers
from app.routers import auth, cuentas, notas, recordatorios, telefonos

app = FastAPI(title="NotaApp API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Abierto para evitar problemas en la expo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectamos los routers
app.include_router(auth.router)
app.include_router(cuentas.router)
app.include_router(telefonos.router)
app.include_router(notas.router)
app.include_router(recordatorios.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Montaje del frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Subimos dos niveles (de app/ a backend/ y luego a la raíz)
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "..", "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    print(f"ADVERTENCIA: No se encontró la carpeta frontend en {FRONTEND_DIR}")
