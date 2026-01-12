### Login Register
from fastapi import APIRouter, Depends, HTTPException
from src.models import User, Leave
from src.schemas import Register, Login
from src.database import get_db
from src.auth import generate_jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import bcrypt


router=APIRouter()

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

@router.post("/register")
def user_register(user:Register,db: Session=Depends(get_db)):
    existing=db.query(User).filter(User.email==user.email).first()
    # select user from User where id ==user.id

    if existing:
        raise HTTPException(status_code=404, detail="User Already exist")
    
    hashed_pass=bcrypt_context.hash(user.password)
    truncated_pass=hashed_pass[:72]

    new_user=User(email=user.email,password=truncated_pass,role=user.role)

    db.add(new_user)
    db.commit()

    return {"msg":"New User Registered Successfully"}


@router.post("/login")
def user_login(user:Login,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    
    

    if not db_user or not bcrypt_context.verify(user.password,db_user.password):
        raise HTTPException(status_code=404,detail="Invalid Credentials")
    
    token=generate_jwt({"sub":db_user.email})

    print("User logged in successfully")
    

    return {"access_token": token, "token_type": "bearer"}