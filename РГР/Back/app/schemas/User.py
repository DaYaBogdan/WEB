from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class LoginData(BaseModel):
    login: str
    password: str

class UserCreate(BaseModel):
    fio: str = Field(..., min_length=3, max_length=50)
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    fio: str 
    login: str
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True   # для работы с SQLAlchemy моделями
        
class UserUpdate(BaseModel):
    fio: Optional[str] = Field(None, min_length=2, max_length=255)
    login: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[str] = Field(None, pattern="^(master|admin)$")
    
    @field_validator('login')
    @classmethod
    def validate_login(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError('Login cannot be empty')
        return v
    
    @field_validator('fio')
    @classmethod
    def validate_fio(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError('FIO cannot be empty')
        return v