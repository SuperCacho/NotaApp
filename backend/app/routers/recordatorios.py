from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.schemas.recordatorios import (
    RecordatorioCreate,
    RecordatorioResponse,
    RecordatorioUpdate,
)
from app.services.security import get_current_profile

router = APIRouter(prefix="/recordatorios", tags=["recordatorios"])


@router.get("/", response_model=list[RecordatorioResponse])
def listar_recordatorios(profile: dict = Depends(get_current_profile)):
    try:
        result = (
            supabase.table("recordatorios")
            .select("*")
            .eq("owner_id", profile["id"])
            .execute()
        )
        return result.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=RecordatorioResponse)
def crear_recordatorio(
    req: RecordatorioCreate, profile: dict = Depends(get_current_profile)
):
    try:
        data = {
            "owner_id": profile["id"],
            "motivo": req.motivo,
            "fecha": str(req.fecha),
            "hora": str(req.hora),
            "estado": req.estado,
            "telefono_id": req.telefono_id,
        }
        result = supabase.table("recordatorios").insert(data).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{recordatorio_id}", response_model=RecordatorioResponse)
def actualizar_recordatorio(
    recordatorio_id: str,
    req: RecordatorioUpdate,
    profile: dict = Depends(get_current_profile),
):
    try:
        cambios = req.dict(exclude_unset=True)
        if "fecha" in cambios:
            cambios["fecha"] = str(cambios["fecha"])
        if "hora" in cambios:
            cambios["hora"] = str(cambios["hora"])
        if not cambios:
            raise HTTPException(status_code=400, detail="Sin cambios")
        result = (
            supabase.table("recordatorios")
            .update(cambios)
            .eq("id", recordatorio_id)
            .eq("owner_id", profile["id"])
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="No encontrado")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{recordatorio_id}")
def eliminar_recordatorio(
    recordatorio_id: str, profile: dict = Depends(get_current_profile)
):
    supabase.table("recordatorios").delete().eq("id", recordatorio_id).eq(
        "owner_id", profile["id"]
    ).execute()
    return {"message": "Eliminado"}
