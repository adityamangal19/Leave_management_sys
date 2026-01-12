from sqlalchemy import Column, String, Integer, ForeignKey,Date
from src.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,nullable=False)
    role=Column(String,nullable=False)
    password=Column(String,nullable=False)
    leave_balance=Column(Integer,default=20)
    total_leaves=Column(Integer,default=0)

    leaves=relationship("Leave",back_populates="user")

class Leave(Base):
    __tablename__="leaves"
    id=Column(Integer,primary_key=True,index=True)
    leave_type=Column(String,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"))
    start_date=Column(Date)
    end_date=Column(Date)
    status=Column(String,default="Pending")
    

    user=relationship("User",back_populates="leaves")
    
