from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.schemas.notas import NotaCreate, NotaResponse, NotaUpdate
from app.services.security import get_current_profile

router = APIRouter(prefix="/notas", tags=["notas"])


@router.get("/", response_model=list[NotaResponse])
def listar_notas(profile: dict = Depends(get_current_profile)):
    try:
        result = (
            supabase.table("notas").select("*").eq("owner_id", profile["id"]).execute()
        )
        return result.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=NotaResponse)
def crear_nota(req: NotaCreate, profile: dict = Depends(get_current_profile)):
    try:
        data = {
            "owner_id": profile["id"],
            "titulo": req.titulo,
            "contenido": req.contenido,
            "categoria": req.categoria,
        }
        result = supabase.table("notas").insert(data).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{nota_id}", response_model=NotaResponse)
def actualizar_nota(
    nota_id: str, req: NotaUpdate, profile: dict = Depends(get_current_profile)
):
    try:
        cambios = req.dict(exclude_unset=True)
        if not cambios:
            raise HTTPException(status_code=400, detail="Sin cambios")
        result = (
            supabase.table("notas")
            .update(cambios)
            .eq("id", nota_id)
            .eq("owner_id", profile["id"])
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="No encontrado")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{nota_id}")
def eliminar_nota(nota_id: str, profile: dict = Depends(get_current_profile)):
    supabase.table("notas").delete().eq("id", nota_id).eq(
        "owner_id", profile["id"]
    ).execute()
    return {"message": "Eliminado"}
