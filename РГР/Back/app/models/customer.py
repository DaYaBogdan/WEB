# app/models/user.py
from app.db.Base import BaseModel
from sqlalchemy import String, Column

class Customer(BaseModel):
    __tablename__ = "customers"
    
    FIO = Column(String)
    phone = Column(String)