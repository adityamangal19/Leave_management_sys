### Employee dashboard and Manager  dashboard

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models import User, Leave
from src.schemas import post_leave,leave_response
from src.auth import get_current_user
from src.database import get_db
from datetime import date

router=APIRouter()

@router.post("/post_leave")  ## employee can post his leave
def post_leaves(leave:post_leave,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    current_user=db.query(User).filter(User.id==user.id).first()
    print(current_user.id)
    
    if not current_user or current_user.role!="employee":
        raise HTTPException(status_code=401,detail="Unauthorized to apply for leaves")
    
    if current_user.total_leaves>current_user.leave_balance or (leave.end_date-leave.start_date).days>current_user.leave_balance:
        return "You have Consumed Your Total leave Balanced , talk with your manager"
    
    new_leave=Leave(user_id=current_user.id,leave_type=leave.leave_type,start_date=leave.start_date,end_date=leave.end_date)
    current_user.total_leaves=(leave.end_date-leave.start_date).days
    print(current_user.total_leaves)
    db.commit()
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return "You successfully apllied for a leave"

@router.get("/see")  ## Manger Can see all the leaves of all employess
def see_leaves(new_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    current_user=db.query(User).filter(User.id==new_user.id).first()

    if  current_user.role!="manager":
        raise HTTPException(status_code=401,detail="Unauthorized access")
    
    Total_leaves=[]
    users=db.query(User).all()
    
    
    if len(users)==0:
        return "No employees"
    for user in users:
        if user.role=="employee":
            l=db.query(Leave).filter(Leave.user_id==user.id).first()
            leave={
                 "user_id":user.id,
                 "email":user.email,
                 "total_leaves":user.total_leaves,
                 "status":l.status
            }
            print(leave)
            Total_leaves.append(leave)
    
    return Total_leaves
    

@router.put("/manager/{emp_id}/{status}")  # Approv and reject leaves   
def manager(emp_id:int,status:str,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    current_user=db.query(User).filter(User.id==user.id).first()
    print(current_user.email)

    emp=db.query(User).filter(User.id==emp_id)
    if not emp or emp.role=="manager":
        raise HTTPException(status_code=401,detail="OPeration not allowed")
    
    if not current_user or current_user.role!="manager":
        raise HTTPException(status_code=401,detail="Unauthorized Access")
    
    emp_leave=db.query(Leave).filter(Leave.user_id==emp_id).first()
    print(emp_leave.id)

    emp_leave.status=status
    db.commit()

    return "Leave status set to {status}"
