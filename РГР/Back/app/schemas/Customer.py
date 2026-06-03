# app/schemas/customer.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class CustomerBase(BaseModel):
    """Базовые поля клиента"""
    FIO: str = Field(..., min_length=2, max_length=255, description="ФИО клиента")
    phone: str = Field(..., description="Номер телефона")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # Удаляем все нецифровые символы
        cleaned = re.sub(r'\D', '', v)
        
        # Проверяем длину (для России 11 цифр)
        if len(cleaned) not in [10, 11]:
            raise ValueError('Phone number must have 10 or 11 digits')
        
        # Приводим к единому формату (+7XXXXXXXXXX)
        if len(cleaned) == 10:
            cleaned = '7' + cleaned
        
        return f"+{cleaned}"
    
    @field_validator('FIO')
    @classmethod
    def validate_fio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('FIO cannot be empty')
        # Убираем лишние пробелы
        return ' '.join(v.strip().split())

class CustomerCreate(CustomerBase):
    """Для создания клиента (POST запрос)"""
    pass

class CustomerUpdate(BaseModel):
    """Для обновления клиента (PATCH/PUT запрос)"""
    FIO: Optional[str] = Field(None, min_length=2, max_length=255)
    phone: Optional[str] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        cleaned = re.sub(r'\D', '', v)
        if len(cleaned) not in [10, 11]:
            raise ValueError('Phone number must have 10 or 11 digits')
        if len(cleaned) == 10:
            cleaned = '7' + cleaned
        return f"+{cleaned}"
    
    @field_validator('FIO')
    @classmethod
    def validate_fio(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('FIO cannot be empty')
        return ' '.join(v.strip().split())

class CustomerResponse(BaseModel):
    """Для ответа с сервера (GET запрос)"""
    id: int
    FIO: str
    phone: str
    created_at: datetime
    updated_at: Optional[datetime] = None  # Может быть None если не обновлялось
    
    class Config:
        from_attributes = True  # Для работы с SQLAlchemy моделями

class CustomerShortResponse(BaseModel):
    """Краткая информация о клиенте (без временных меток)"""
    id: int
    FIO: str
    phone: str
    
    class Config:
        from_attributes = True