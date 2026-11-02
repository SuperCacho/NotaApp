
from fastapi import APIRouter, HTTPException, Depends
from app.database import supabase
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse
from app.services.security import get_current_profile

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(req: RegisterRequest):
    try:
        auth_response = supabase.auth.sign_up({
            "email": req.email,
            "password": req.password,
            "options": {"data": {"nombre": req.nombre, "rol": req.rol}}
        })

        if not auth_response.user:
            raise HTTPException(status_code=400, detail="No se pudo crear el usuario")

        auth_id = auth_response.user.id

        existing = supabase.table("profiles").select("*").eq("auth_id", auth_id).execute()
        if existing.data and len(existing.data) > 0:
            profile = existing.data[0]
        else:
            profile_data = {
                "auth_id": auth_id,
                "nombre": req.nombre,
                "email": req.email,
                "rol": req.rol,
                "activo": True
            }
            insert_result = supabase.table("profiles").insert(profile_data).execute()
            profile = insert_result.data[0] if insert_result.data else None

        return {
            "message": "Usuario registrado correctamente",
            "user": UserResponse(
                id=str(profile["id"]),
                nombre=profile["nombre"],
                email=profile["email"],
                rol=profile["rol"]
            )
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en el registro: {str(e)}")


@router.post("/login")
def login(req: LoginRequest):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })

        if not auth_response.session:
            raise HTTPException(status_code=401, detail="Credenciales invalidas")

        profile_result = supabase.table("profiles").select("*").eq("auth_id", auth_response.user.id).execute()
        profile = profile_result.data[0] if profile_result.data else None

        return {
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "user": UserResponse(
                id=str(profile["id"]) if profile else str(auth_response.user.id),
                nombre=profile["nombre"] if profile else auth_response.user.user_metadata.get("nombre", ""),
                email=auth_response.user.email,
                rol=profile["rol"] if profile else auth_response.user.user_metadata.get("rol", "titular")
            )
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error en login: {str(e)}")


@router.get("/me")
def me(profile: dict = Depends(get_current_profile)):
    return UserResponse(
        id=str(profile["id"]),
        nombre=profile["nombre"],
        email=profile["email"],
        rol=profile["rol"]
    )
