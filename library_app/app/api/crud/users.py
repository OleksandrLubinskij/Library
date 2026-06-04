from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.security import get_password_hash
from app.core.config import USERNAME, PASSWORD, ROLE

router = APIRouter()

def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()

def create_user(user: UserCreate, db) -> None:
    user_dict = user.model_dump()
    raw_password = user_dict.pop(PASSWORD)
    hashed_password = get_password_hash(raw_password)

    new_user = User(
        username = user_dict[USERNAME],
        password = hashed_password,
        role = user_dict[ROLE]
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": "Can`t add user to database"})
    
