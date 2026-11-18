from fastapi import APIRouter, HTTPException

from app.database import supabase
from app.schemas.auth import LoginRequest, RegisterRequest, UserResponse
from app.services.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(req: RegisterRequest):
    # Verificamos si existe
    existe = (
        supabase.table("profiles")
        .select("id")
        .or_(f"email.eq.{req.email},username.eq.{req.username}")
        .execute()
    )
    if existe.data:
        raise HTTPException(
            status_code=400, detail="El email o nombre de usuario ya está en uso"
        )

    # Hasheamos
    hashed_pw = get_password_hash(req.password)

    # Preparamos los datos
    profile_data = {
        "nombre": req.nombre,
        "username": req.username,
        "email": req.email,
        "password_hash": hashed_pw,
        "rol": req.rol,
        "activo": True,
    }

    # Insertamos en Supabase
    try:
        res = supabase.table("profiles").insert(profile_data).execute()
        if not res.data:
            raise Exception("No se pudo guardar")
    except Exception as e:
        print("ERROR REAL EN SUPABASE:", e)
        raise HTTPException(
            status_code=500, detail="Error interno al registrar usuario"
        )

    profile = res.data[0]
    return {
        "message": "Usuario registrado correctamente",
        "user": UserResponse(
            id=str(profile["id"]),
            nombre=profile["nombre"],
            username=profile["username"],
            email=profile["email"],
            rol=profile["rol"],
        ),
    }


@router.post("/login")
def login(req: LoginRequest):
    # Buscamos por email O por username
    res = (
        supabase.table("profiles")
        .select("*")
        .or_(f"email.eq.{req.identifier},username.eq.{req.identifier}")
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    profile = res.data[0]

    # Validamos contraseña
    if not profile.get("password_hash") or not verify_password(
        req.password, profile["password_hash"]
    ):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Generamos el token
    token = create_access_token(data={"sub": str(profile["id"])})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(
            id=str(profile["id"]),
            nombre=profile["nombre"],
            username=profile["username"],
            email=profile["email"],
            rol=profile["rol"],
        ),
    }
