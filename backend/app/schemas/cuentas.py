from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CuentaCreate(BaseModel):
    sitio: str = Field(..., min_length=1, max_length=200)
    login: str = Field(..., min_length=1, max_length=200)
    password: str = Field(..., min_length=1)
    tipo: str = Field(..., pattern="^(correo|red_social|streaming|otro)$")
    estado: str = Field(..., pattern="^(normal|importante|revisar|urgente)$")


class CuentaUpdate(BaseModel):
    sitio: Optional[str] = Field(None, min_length=1, max_length=200)
    login: Optional[str] = Field(None, min_length=1, max_length=200)
    password: Optional[str] = Field(None, min_length=1)
    tipo: Optional[str] = Field(None, pattern="^(correo|red_social|streaming|otro)$")
    estado: Optional[str] = Field(None, pattern="^(normal|importante|revisar|urgente)$")


class CuentaResponse(BaseModel):
    id: str
    sitio: str
    login: str
    tipo: str
    estado: str
    archivada: bool
    created_at: Optional[datetime] = None