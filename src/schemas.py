from pydantic import BaseModel
from datetime import date

class Register(BaseModel):
    email:str
    role:str
    password:str

class Login(BaseModel):
    email:str
    password:str

class post_leave(BaseModel):
    leave_type:str
    start_date:date
    end_date:date

class leave_response(BaseModel):
    user_id:int
    email:str
    total_leaves:int
    status:str


    