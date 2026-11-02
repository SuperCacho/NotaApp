from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.schemas.telefonos import TelefonoCreate, TelefonoResponse, TelefonoUpdate
from app.services.security import get_current_profile

router = APIRouter(prefix="/telefonos", tags=["telefonos"])


@router.get("/", response_model=list[TelefonoResponse])
def listar_telefonos(profile: dict = Depends(get_current_profile)):
    try:
        result = (
            supabase.table("telefonos")
            .select("*")
            .eq("owner_id", profile["id"])
            .execute()
        )
        return result.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=TelefonoResponse)
def crear_telefono(req: TelefonoCreate, profile: dict = Depends(get_current_profile)):
    try:
        data = {
            "owner_id": profile["id"],
            "nombre": req.nombre,
            "numero": req.numero,
            "tipo": req.tipo,
            "descripcion": req.descripcion,
        }
        result = supabase.table("telefonos").insert(data).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{telefono_id}", response_model=TelefonoResponse)
def actualizar_telefono(
    telefono_id: str, req: TelefonoUpdate, profile: dict = Depends(get_current_profile)
):
    try:
        cambios = req.dict(exclude_unset=True)
        if not cambios:
            raise HTTPException(status_code=400, detail="Sin cambios")
        result = (
            supabase.table("telefonos")
            .update(cambios)
            .eq("id", telefono_id)
            .eq("owner_id", profile["id"])
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="No encontrado")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{telefono_id}")
def eliminar_telefono(telefono_id: str, profile: dict = Depends(get_current_profile)):
    supabase.table("telefonos").delete().eq("id", telefono_id).eq(
        "owner_id", profile["id"]
    ).execute()
    return {"message": "Eliminado"}
