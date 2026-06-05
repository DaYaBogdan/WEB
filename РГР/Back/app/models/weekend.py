# app/models/user.py
from app.db.Base import BaseModel
from sqlalchemy import String, Column, Integer, ForeignKey, Date

class Weekend(BaseModel):
    __tablename__ = "weekends"
    
    master_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, unique=True, nullable=False)  # только дата