from typing import Optional
from pydantic import BaseModel
from .User import UserResponse
from .Settings import SettingsResponse

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    settings: Optional[SettingsResponse] = None