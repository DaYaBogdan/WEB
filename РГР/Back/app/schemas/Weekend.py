from pydantic import BaseModel, Field
from datetime import date as d

class WeekendSchema(BaseModel):
    master_id: int = Field(..., description="ID мастера")
    date: d = Field(..., description="Дата выходного дня")
    
class WeekendResponse(BaseModel):
    id: int
    master_id: int
    date: d
    
    class Config:
        from_attributes = True  # для совместимости с SQLAlchemy