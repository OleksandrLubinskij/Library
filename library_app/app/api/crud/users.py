from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.services import get_password_hash
from app.database import get_db
from app.core.config import USERNAME, PASSWORD

router = APIRouter()

def user_exists(username: str, db: Session = Depends(get_db)) -> bool:
    user = db.get(User, username)
    return True if user else False

def create_user(user: UserCreate, db: Session = Depends(get_db)) -> None:
    user_dict = user.model_dump()
    raw_password = user_dict.pop(PASSWORD)
    hashed_password = get_password_hash(raw_password)

    new_user = User(
        username = user_dict[USERNAME],
        password = hashed_password
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
    
