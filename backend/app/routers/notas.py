from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.schemas.notas import NotaCreate, NotaUpdate
from app.services.security import get_current_profile

router = APIRouter(prefix="/notas", tags=["notas"])


@router.get("/")
def get_notas(profile: dict = Depends(get_current_profile)):
    res = (
        supabase.table("notas").select("*").eq("user_id", str(profile["id"])).execute()
    )
    return res.data


@router.post("/")
def create_nota(nota: NotaCreate, profile: dict = Depends(get_current_profile)):
    data = nota.model_dump()
    data["user_id"] = str(profile["id"])
    res = supabase.table("notas").insert(data).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="No se pudo crear la nota")
    return res.data[0]


@router.put("/{nota_id}")
def update_nota(
    nota_id: str, nota: NotaUpdate, profile: dict = Depends(get_current_profile)
):
    existe = (
        supabase.table("notas")
        .select("id")
        .eq("id", nota_id)
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    if not existe.data:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    data = nota.model_dump(exclude_unset=True)
    res = supabase.table("notas").update(data).eq("id", nota_id).execute()
    return res.data[0]


@router.delete("/{nota_id}")
def delete_nota(nota_id: str, profile: dict = Depends(get_current_profile)):
    existe = (
        supabase.table("notas")
        .select("id")
        .eq("id", nota_id)
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    if not existe.data:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    supabase.table("notas").delete().eq("id", nota_id).execute()
    return {"message": "Nota eliminada"}
