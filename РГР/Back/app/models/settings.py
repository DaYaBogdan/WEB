# app/models/user.py
from app.db.Base import BaseModel
from sqlalchemy import String, Column, Integer, ForeignKey

class Settings(BaseModel):
    __tablename__ = "settings"
    
    master_id = Column(Integer, ForeignKey('users.id'))
    theme = Column(String)
    language = Column(String)