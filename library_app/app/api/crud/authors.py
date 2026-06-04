from fastapi import Depends, HTTPException, APIRouter, status
from app.models import Author, User
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas import AuthorCreate
from app.services import get_current_user
from app.core.config import ADMIN
router = APIRouter()

def get_all_authors(db):
    stmt = select(Author)
    author = db.execute(stmt).scalars().all()
    return author

@router.get("/")
async def get_authors(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    return get_all_authors(db)

@router.post("/create")
async def create_author(author: AuthorCreate, 
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(get_current_user)):
    if current_user.role != ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="There are no rights for this action")
    
    new_author_dict = author.model_dump()
    new_author = Author(**new_author_dict)
    try:
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        return new_author
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": "Can`t add author to database"})
    
@router.delete("/delete/{author_id}")
async def delete_author(author_id: int, 
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    if current_user.role != ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="There are no rights for this action")
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Author not found"})
    
    try:
        db.delete(author)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": "Can`t delete author from database"})