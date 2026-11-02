from fastapi import HTTPException, Header, Depends
from app.database import supabase


async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Falta token de autenticacion")

    token = authorization.replace("Bearer ", "")

    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalido")
        return user_response.user
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")


async def get_current_profile(user=Depends(get_current_user)):
    try:
        result = supabase.table("profiles").select("*").eq("auth_id", user.id).single().execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Perfil no encontrado")
        return result.data
    except Exception:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")