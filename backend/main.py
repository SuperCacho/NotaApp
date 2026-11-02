import os
from datetime import UTC, datetime, timedelta

import jwt as pyjwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from models import (
    CuentaCreate,
    LoginRequest,
    NotaCreate,
    RecordatorioCreate,
    TelefonoCreate,
)
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_demo_key")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️ ERROR: Faltan las variables de entorno en el .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI(title="NotaApp API")


# --- AUTH ---
@app.post("/auth/login")
def login(data: LoginRequest):
    try:
        res = supabase.table("profiles").select("*").eq("email", data.email).execute()
        if not res.data:
            nuevo_perfil = {
                "nombre": "Lucio Titular",
                "email": data.email,
                "rol": "titular",
                "activo": True,
            }
            res = supabase.table("profiles").insert(nuevo_perfil).execute()
        user = res.data[0]
        payload = {
            "sub": user["id"],
            "email": user["email"],
            "exp": datetime.now(UTC) + timedelta(hours=12),
        }
        token = pyjwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return {"access_token": token, "usuario": user}
    except Exception as e:
        raise HTTPException(500, detail=f"Error DB: {e!s}")


def get_current_user(authorization: str | None = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Token faltante")
    try:
        token = authorization.split(" ")[1]
        payload = pyjwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return {"id": payload["sub"], "email": payload["email"]}
    except:
        raise HTTPException(401, "Token inválido")


# --- CUENTAS ---
@app.get("/cuentas")
def listar_cuentas(user=Depends(get_current_user)):
    return (
        supabase.table("cuentas").select("*").eq("owner_id", user["id"]).execute().data
    )


@app.post("/cuentas")
def crear_cuenta(data: CuentaCreate, user=Depends(get_current_user)):
    nueva = data.dict()
    nueva["owner_id"] = user["id"]
    nueva["password_iv"] = "pending"
    nueva["password_salt"] = "pending"
    nueva["password_key_version"] = 1
    try:
        return supabase.table("cuentas").insert(nueva).execute().data[0]
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@app.delete("/cuentas/{id}")
def borrar_cuenta(id: str, user=Depends(get_current_user)):
    supabase.table("cuentas").delete().eq("id", id).eq("owner_id", user["id"]).execute()
    return {"ok": True}


# --- TELEFONOS ---
@app.get("/telefonos")
def listar_telefonos(user=Depends(get_current_user)):
    return (
        supabase.table("telefonos")
        .select("*")
        .eq("owner_id", user["id"])
        .execute()
        .data
    )


@app.post("/telefonos")
def crear_telefono(data: TelefonoCreate, user=Depends(get_current_user)):
    nuevo = data.dict()
    nuevo["owner_id"] = user["id"]
    return supabase.table("telefonos").insert(nuevo).execute().data[0]


@app.delete("/telefonos/{id}")
def borrar_telefono(id: str, user=Depends(get_current_user)):
    supabase.table("telefonos").delete().eq("id", id).eq(
        "owner_id", user["id"]
    ).execute()
    return {"ok": True}


# --- NOTAS ---
@app.get("/notas")
def listar_notas(user=Depends(get_current_user)):
    return supabase.table("notas").select("*").eq("owner_id", user["id"]).execute().data


@app.post("/notas")
def crear_nota(data: NotaCreate, user=Depends(get_current_user)):
    nueva = data.dict()
    nueva["owner_id"] = user["id"]
    return supabase.table("notas").insert(nueva).execute().data[0]


@app.delete("/notas/{id}")
def borrar_nota(id: str, user=Depends(get_current_user)):
    supabase.table("notas").delete().eq("id", id).eq("owner_id", user["id"]).execute()
    return {"ok": True}


# --- RECORDATORIOS ---
@app.get("/recordatorios")
def listar_recordatorios(user=Depends(get_current_user)):
    return (
        supabase.table("recordatorios")
        .select("*")
        .eq("owner_id", user["id"])
        .execute()
        .data
    )


@app.post("/recordatorios")
def crear_recordatorio(data: RecordatorioCreate, user=Depends(get_current_user)):
    nuevo = data.dict()
    nuevo["owner_id"] = user["id"]
    return supabase.table("recordatorios").insert(nuevo).execute().data[0]


@app.delete("/recordatorios/{id}")
def borrar_recordatorio(id: str, user=Depends(get_current_user)):
    supabase.table("recordatorios").delete().eq("id", id).eq(
        "owner_id", user["id"]
    ).execute()
    return {"ok": True}


# --- STATIC ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
