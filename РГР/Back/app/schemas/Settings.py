from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SettingsResponse(BaseModel):
    id: int
    user_id: int  # Изменено с master_id на user_id
    theme: str
    language: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SettingsUpdate(BaseModel):
    theme: Optional[str] = Field(None, min_length=2, max_length=50)
    language: Optional[str] = Field(None, min_length=2, max_length=10)

class SettingsCreate(BaseModel):
    user_id: int
    theme: str = "light"
    language: str = "ru"