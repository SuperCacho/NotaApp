from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class CuentaCreate(BaseModel):
    sitio: str
    login: str
    tipo: str
    estado: str = "Normal"
    password_ciphertext: str = "pending_web_crypto"


class TelefonoCreate(BaseModel):
    nombre: str
    numero: str
    tipo: str
    descripcion: str | None = ""


class NotaCreate(BaseModel):
    titulo: str
    contenido: str
    categoria: str


class RecodatorioCreate(BaseModel):
    motivo: str
    fecha: str
    hora: str
    estado: str = "Pendiente"
    telefono_id: str | None = None
