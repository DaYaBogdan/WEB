from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SettingsResponse(BaseModel):
    id: int
    user_id: int
    theme: str
    language: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SettingsUpdate(BaseModel):
    theme: Optional[str] = Field(None, pattern="^(light|dark)$")
    language: Optional[str] = Field(None, pattern="^(ru|en)$")

class SettingsCreate(BaseModel):
    user_id: int
    theme: str = Field("light", pattern="^(light|dark)$")
    language: str = Field("ru", pattern="^(ru|en)$")