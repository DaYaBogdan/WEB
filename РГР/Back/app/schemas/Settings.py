from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SettingsData(BaseModel):
    id: int
    master_id: int
    theme: str
    language: str
    created_at: datetime
    updated_at: Optional[datetime] = None