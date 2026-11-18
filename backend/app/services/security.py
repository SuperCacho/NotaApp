import os
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from app.database import supabase

# Configuración de seguridad
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key-cambiame-en-produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8  # Token de 8 horas

# ACÁ EL CAMBIO: Usamos pbkdf2_sha256 en vez de bcrypt
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Herramienta para leer el token
security_scheme = HTTPBearer()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        profile_id = payload.get("sub")
        if profile_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="La sesión ha expirado")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Buscamos al usuario en la base de datos por su ID
    res = supabase.table("profiles").select("*").eq("id", profile_id).execute()
    if not res.data:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return res.data[0]
