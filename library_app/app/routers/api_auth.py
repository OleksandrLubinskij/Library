from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate
from app.api.crud import users as crud_users

from sqlalchemy import select
from app.models import User
router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> dict:
    existing_user = crud_users.user_exists(user_data.username, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this name already exists"
        )
    
    crud_users.create_user(db=db, user=user_data)
    
    return {"message": "User registered successfully"}

@router.get("/get")
async def get_authors(db: Session = Depends(get_db)):
    stmt = select(User)
    author = db.execute(stmt).scalars().all()
    return author