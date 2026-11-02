from datetime import date, datetime, time

from pydantic import BaseModel, Field


class RecordatorioCreate(BaseModel):
    motivo: str = Field(..., min_length=1, max_length=200)
    fecha: date
    hora: time
    estado: str = Field(..., pattern="^(pendiente|realizado|urgente)$")
    telefono_id: str | None = None


class RecordatorioUpdate(BaseModel):
    motivo: str | None = Field(None, min_length=1, max_length=200)
    fecha: date | None = None
    hora: time | None = None
    estado: str | None = Field(None, pattern="^(pendiente|realizado|urgente)$")


class RecordatorioResponse(BaseModel):
    id: str
    motivo: str
    fecha: date
    hora: time
    estado: str
    telefono_id: str | None = None
    created_at: datetime | None = None
