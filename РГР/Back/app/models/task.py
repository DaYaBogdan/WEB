# app/models/user.py
from app.db.Base import BaseModel
from sqlalchemy import String, Column, Integer, ForeignKey, TIMESTAMP

class Task(BaseModel):
    __tablename__ = "tasks"
    
    customer_id = Column(Integer, ForeignKey('customers.id'))
    master_id = Column(Integer, ForeignKey('users.id'))
    service = Column(String)
    dateTime = Column(TIMESTAMP(timezone=True))
    cost = Column(Integer)