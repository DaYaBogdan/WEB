# app/db/base.py
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr, declarative_base

Base = declarative_base()

class BaseModel(Base):
    """Абстрактная базовая модель с общими полями"""
    __abstract__ = True  # Важно! Таблица не создаётся

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())