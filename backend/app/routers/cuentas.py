from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.schemas.cuentas import CuentaCreate, CuentaResponse, CuentaUpdate
from app.services.security import get_current_profile

router = APIRouter(prefix="/cuentas", tags=["cuentas"])


def _to_response(c: dict) -> CuentaResponse:
    return CuentaResponse(
        id=str(c["id"]),
        sitio=c["sitio"],
        login=c["login"],
        tipo=c["tipo"],
        estado=c["estado"],
        archivada=c["archivada"],
        created_at=c.get("created_at"),
    )


@router.get("/", response_model=list[CuentaResponse])
def listar_cuentas(profile: dict = Depends(get_current_profile)):
    try:
        result = (
            supabase.table("cuentas")
            .select("*")
            .eq("owner_id", profile["id"])
            .eq("archivada", False)
            .execute()
        )
        return [_to_response(c) for c in (result.data or [])]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar cuentas: {e!s}")


@router.post("/", response_model=CuentaResponse)
def crear_cuenta(req: CuentaCreate, profile: dict = Depends(get_current_profile)):
    try:
        cuenta_data = {
            "owner_id": profile["id"],
            "sitio": req.sitio,
            "login": req.login,
            "password_ciphertext": req.password,
            "tipo": req.tipo,
            "estado": req.estado,
            "archivada": False,
            # Agregamos estos campos para que Supabase no de error
            "password_iv": "pending_iv",
            "password_salt": "pending_salt",
            "password_key_version": 1,
        }

        result = supabase.table("cuentas").insert(cuenta_data).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="No se pudo crear la cuenta")

        return _to_response(result.data[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear cuenta: {e!s}")


@router.put("/{cuenta_id}", response_model=CuentaResponse)
def actualizar_cuenta(
    cuenta_id: str, req: CuentaUpdate, profile: dict = Depends(get_current_profile)
):
    try:
        existente = (
            supabase.table("cuentas")
            .select("*")
            .eq("id", cuenta_id)
            .eq("owner_id", profile["id"])
            .execute()
        )
        if not existente.data:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        cambios = {}
        if req.sitio is not None:
            cambios["sitio"] = req.sitio
        if req.login is not None:
            cambios["login"] = req.login
        if req.tipo is not None:
            cambios["tipo"] = req.tipo
        if req.estado is not None:
            cambios["estado"] = req.estado
        if req.password:
            cambios["password_ciphertext"] = req.password

        if not cambios:
            return _to_response(existente.data[0])

        result = supabase.table("cuentas").update(cambios).eq("id", cuenta_id).execute()
        if not result.data:
            raise HTTPException(status_code=500, detail="No se pudo actualizar")

        return _to_response(result.data[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar cuenta: {e!s}"
        )


@router.delete("/{cuenta_id}")
def eliminar_cuenta(cuenta_id: str, profile: dict = Depends(get_current_profile)):
    try:
        existente = (
            supabase.table("cuentas")
            .select("*")
            .eq("id", cuenta_id)
            .eq("owner_id", profile["id"])
            .execute()
        )
        if not existente.data:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        supabase.table("cuentas").delete().eq("id", cuenta_id).execute()
        return {"message": "Cuenta eliminada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar cuenta: {e!s}")
