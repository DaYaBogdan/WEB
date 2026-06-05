from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class LoginData(BaseModel):
    login: str
    password: str

class UserCreate(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    login: str
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True   # для работы с SQLAlchemy моделями