from fastapi import Depends, HTTPException, APIRouter, Query
from app.models import Author
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas import AuthorCreate

router = APIRouter()

@router.get("/")
async def get_authors(db: Session = Depends(get_db)):
    stmt = select(Author)
    author = db.execute(stmt).scalars().all()
    return author

@router.post("/create")
async def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=500, detail={"message": "Can`t add author to database"})
    
@router.delete("/delete/{author_id}")
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail={"message": "Author not found"})
    
    try:
        db.delete(author)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail={"message": "Can`t delete author from database"})