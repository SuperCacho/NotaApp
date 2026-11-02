from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    rol: str = "titular"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    id: str
    nombre: str
    email: str
    rol: str