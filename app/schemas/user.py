from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    # El rol se asigna automáticamente como "client" en el endpoint

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    role: str

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"