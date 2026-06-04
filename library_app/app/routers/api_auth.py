from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserLogin
from app.api.crud import users as crud_users
from sqlalchemy import select
from app.models import User
from app.services import get_current_user
from app.security import  verify_password, create_access_token
from app.core.config import ADMIN
router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> dict:
    existing_user = crud_users.get_user_by_username(username=user_data.username, db=db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this name already exists"
        )
    
    crud_users.create_user(db=db, user=user_data)
    
    return {"message": "User registered successfully"}

@router.get("/get")
async def get_users(db: Session = Depends(get_db),
                    current_user: str = Depends(get_current_user)):
    if current_user.role != ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="There are no rights for this action")
    stmt = select(User)
    user = db.execute(stmt).scalars().all()
    return user

@router.post("/login")
async def login(response: Response, user_info: UserLogin, db: Session = Depends(get_db)) -> dict:
    user = crud_users.get_user_by_username(username=user_info.username, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A user with this name already exists"
        )
    if not verify_password(user_info.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    token_data = {
        "sub": user.username,
        "role": user.role
    }
    access_token = create_access_token(data=token_data)
    
    response.set_cookie(
        key="access_token", 
        value=f"{access_token}", 
        httponly=True
    )
    
    return {"message": "Successful login"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "success", "message": "Logged out successfully"}