from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.schemas.recordatorios import RecordatorioCreate, RecordatorioUpdate
from app.services.security import get_current_profile

router = APIRouter(prefix="/recordatorios", tags=["recordatorios"])


@router.get("/")
def get_recordatorios(profile: dict = Depends(get_current_profile)):
    res = (
        supabase.table("recordatorios")
        .select("*")
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    return res.data


@router.post("/")
def create_recordatorio(
    rec: RecordatorioCreate, profile: dict = Depends(get_current_profile)
):
    data = rec.model_dump()
    data["user_id"] = str(profile["id"])
    res = supabase.table("recordatorios").insert(data).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="No se pudo crear el recordatorio")
    return res.data[0]


@router.put("/{rec_id}")
def update_recordatorio(
    rec_id: str, rec: RecordatorioUpdate, profile: dict = Depends(get_current_profile)
):
    existe = (
        supabase.table("recordatorios")
        .select("id")
        .eq("id", rec_id)
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    if not existe.data:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    data = rec.model_dump(exclude_unset=True)
    res = supabase.table("recordatorios").update(data).eq("id", rec_id).execute()
    return res.data[0]


@router.delete("/{rec_id}")
def delete_recordatorio(rec_id: str, profile: dict = Depends(get_current_profile)):
    existe = (
        supabase.table("recordatorios")
        .select("id")
        .eq("id", rec_id)
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    if not existe.data:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    supabase.table("recordatorios").delete().eq("id", rec_id).execute()
    return {"message": "Recordatorio eliminado"}
