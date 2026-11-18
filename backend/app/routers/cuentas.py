from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.schemas.cuentas import CuentaCreate, CuentaUpdate
from app.services.security import get_current_profile

router = APIRouter(prefix="/cuentas", tags=["cuentas"])


@router.get("/")
def get_cuentas(profile: dict = Depends(get_current_profile)):
    res = (
        supabase.table("cuentas")
        .select("*")
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    return res.data


@router.post("/")
def create_cuenta(cuenta: CuentaCreate, profile: dict = Depends(get_current_profile)):
    data = cuenta.model_dump()
    data["user_id"] = str(profile["id"])
    res = supabase.table("cuentas").insert(data).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="No se pudo crear la cuenta")
    return res.data[0]


@router.put("/{cuenta_id}")
def update_cuenta(
    cuenta_id: str, cuenta: CuentaUpdate, profile: dict = Depends(get_current_profile)
):
    existe = (
        supabase.table("cuentas")
        .select("id")
        .eq("id", cuenta_id)
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    if not existe.data:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    data = cuenta.model_dump(exclude_unset=True)
    res = supabase.table("cuentas").update(data).eq("id", cuenta_id).execute()
    return res.data[0]


@router.delete("/{cuenta_id}")
def delete_cuenta(cuenta_id: str, profile: dict = Depends(get_current_profile)):
    existe = (
        supabase.table("cuentas")
        .select("id")
        .eq("id", cuenta_id)
        .eq("user_id", str(profile["id"]))
        .execute()
    )
    if not existe.data:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    supabase.table("cuentas").delete().eq("id", cuenta_id).execute()
    return {"message": "Cuenta eliminada"}
