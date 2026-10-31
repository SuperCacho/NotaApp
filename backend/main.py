# backend/main.py
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import Client, create_client

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear cliente de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Faltan las variables de entorno SUPABASE_URL o SUPABASE_PUBLISHABLE_KEY"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="NotaApp API")


class Cuenta(BaseModel):
    nombre_servicio: str
    usuario_login: str


@app.get("/")
def read_root():
    return {"mensaje": "¡Hola desde FastAPI y Supabase!"}


@app.get("/api/test-db")
def test_db_connection():
    """Endpoint de prueba para verificar la conexión con Supabase."""
    try:
        # Hacemos una consulta simple a la tabla 'cuentas'.
        # Si RLS está bien configurado, esto podría devolver un array vacío o un error de permisos.
        # Ajustaremos esto según tu esquema real.
        response = supabase.table("cuentas").select("*").limit(1).execute()
        return {"conexion": "exitosa", "datos": response.data}
    except Exception as e:
        # Si hay un error (ej. tabla no existe, RLS bloquea), lo devolvemos para debug.
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e!s}")


# (Opcional) Ruta para crear una cuenta de prueba
@app.post("/api/cuentas-test")
def crear_cuenta_test(cuenta: Cuenta):
    try:
        response = supabase.table("cuentas").insert(cuenta.dict()).execute()
        return {"cuenta_creada": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear: {e!s}")


from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
