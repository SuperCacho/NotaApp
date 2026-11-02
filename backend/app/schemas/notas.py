from datetime import datetime

from pydantic import BaseModel, Field


class NotaCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150)
    contenido: str = Field(..., min_length=1)
    categoria: str = Field(..., pattern="^(servicios|salud|personal|otro)$")


class NotaUpdate(BaseModel):
    titulo: str | None = Field(None, min_length=1, max_length=150)
    contenido: str | None = Field(None, min_length=1)
    categoria: str | None = Field(None, pattern="^(servicios|salud|personal|otro)$")


class NotaResponse(BaseModel):
    id: str
    titulo: str
    contenido: str
    categoria: str
    created_at: datetime | None = None
