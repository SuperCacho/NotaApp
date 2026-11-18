from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.schemas.telefonos import TelefonoCreate, TelefonoUpdate
from app.services.security import get_current_profile

router = APIRouter(prefix="/telefonos", tags=["telefonos"])


@router.get("/")
def get_telefonos(profile: dict = Depends(get_current_profile)):
    res = (
        supabase.table("telefonos")
        .select("*")
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    return res.data


@router.post("/")
def create_telefono(
    telefono: TelefonoCreate, profile: dict = Depends(get_current_profile)
):
    data = telefono.model_dump()
    data["user_id"] = str(profile["id"])
    res = supabase.table("telefonos").insert(data).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="No se pudo crear el teléfono")
    return res.data[0]


@router.put("/{telefono_id}")
def update_telefono(
    telefono_id: str,
    telefono: TelefonoUpdate,
    profile: dict = Depends(get_current_profile),
):
    existe = (
        supabase.table("telefonos")
        .select("id")
        .eq("id", telefono_id)
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    if not existe.data:
        raise HTTPException(status_code=404, detail="Teléfono no encontrado")
    data = telefono.model_dump(exclude_unset=True)
    res = supabase.table("telefonos").update(data).eq("id", telefono_id).execute()
    return res.data[0]


@router.delete("/{telefono_id}")
def delete_telefono(telefono_id: str, profile: dict = Depends(get_current_profile)):
    existe = (
        supabase.table("telefonos")
        .select("id")
        .eq("id", telefono_id)
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    if not existe.data:
        raise HTTPException(status_code=404, detail="Teléfono no encontrado")
    supabase.table("telefonos").delete().eq("id", telefono_id).execute()
    return {"message": "Teléfono eliminado"}
