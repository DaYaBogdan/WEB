# app/models/user.py
from app.db.Base import BaseModel
from sqlalchemy import String, Column, Integer

class Customer(BaseModel):
    __tablename__ = "customers"
    
    masterID = Column(Integer)
    FIO = Column(String)
    phone = Column(String)
    email = Column(String, nullable=True)
    
    