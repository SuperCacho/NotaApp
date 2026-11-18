from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    rol: str = "titular"


class LoginRequest(BaseModel):
    identifier: str = Field(..., description="Puede ser un email o un username")
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: str
    nombre: str
    username: str
    email: str
    rol: str
