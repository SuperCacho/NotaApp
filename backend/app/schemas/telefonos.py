from datetime import datetime

from pydantic import BaseModel, Field


class TelefonoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    numero: str = Field(..., min_length=6, max_length=20)
    tipo: str = Field(..., pattern="^(familiar|medico|emergencia|servicios|otro)$")
    descripcion: str | None = Field(None, max_length=200)


class TelefonoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    numero: str | None = Field(None, min_length=6, max_length=20)
    tipo: str | None = Field(
        None, pattern="^(familiar|medico|emergencia|servicios|otro)$"
    )
    descripcion: str | None = Field(None, max_length=200)


class TelefonoResponse(BaseModel):
    id: str
    nombre: str
    numero: str
    tipo: str
    descripcion: str | None = None
    created_at: datetime | None = None
