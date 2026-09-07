from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    """Для создания задачи"""
    customer_id: int
    master_id: int
    service: str
    datetime: datetime 
    cost: int

class TaskResponse(BaseModel):
    id: int
    customer_id: int
    master_id: int
    service: str
    dateTime: datetime  
    cost: float = Field(..., ge=500, le=5000)
    
    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    """Для обновления задачи (все поля опциональны)"""
    customer_id: Optional[int] = None
    master_id: Optional[int] = None
    service: Optional[str] = None
    dateTime: Optional[datetime] = None
    cost: Optional[float] = Field(..., ge=500, le=5000)
    completed: Optional[bool] = None