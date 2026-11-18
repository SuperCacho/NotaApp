from datetime import datetime

from pydantic import BaseModel, Field


class NotaCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    contenido: str = Field(..., min_length=1)
    categoria: str = Field(..., pattern="^(personal|salud|servicios|estudio|otro)$")


class NotaUpdate(BaseModel):
    titulo: str | None = Field(None, min_length=1, max_length=200)
    contenido: str | None = Field(None, min_length=1)
    categoria: str | None = Field(
        None, pattern="^(personal|salud|servicios|estudio|otro)$"
    )


class NotaResponse(BaseModel):
    id: str
    titulo: str
    contenido: str
    categoria: str
    user_id: str
    created_at: datetime | None = None
