# app/models/user.py
from app.db.Base import BaseModel
from sqlalchemy import String, Column

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True)
    password = Column(String)