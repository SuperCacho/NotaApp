from datetime import datetime

from pydantic import BaseModel, Field


class CuentaCreate(BaseModel):
    sitio: str = Field(..., min_length=1, max_length=200)
    login: str = Field(..., min_length=1, max_length=200, description="Usuario o email")
    password: str = Field(..., min_length=1)
    tipo: str = Field(..., pattern="^(correo|red_social|streaming|otro)$")
    estado: str = Field(..., pattern="^(normal|importante|revisar)$")


class CuentaUpdate(BaseModel):
    sitio: str | None = Field(None, min_length=1, max_length=200)
    login: str | None = Field(None, min_length=1, max_length=200)
    password: str | None = Field(None, min_length=1)
    tipo: str | None = Field(None, pattern="^(correo|red_social|streaming|otro)$")
    estado: str | None = Field(None, pattern="^(normal|importante|revisar)$")


class CuentaResponse(BaseModel):
    id: str
    sitio: str
    login: str
    tipo: str
    estado: str
    archivada: bool
    created_at: datetime | None = None
