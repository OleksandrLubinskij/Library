from fastapi import Depends, HTTPException, APIRouter
from app.models import Book
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas import BookCreate, BookUpdate
from typing import Optional

router = APIRouter()

@router.get("/")
async def get_books(
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    stmt = select(Book)
    if title:
        stmt = stmt.where(Book.title.ilike(f"%{title}%"))

    if author_id:
        stmt = stmt.where(Book.author_id == author_id)
    books = db.execute(stmt).scalars().all()
    return books

@router.post("/create")
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book_dict = book.model_dump()
    new_book = Book(**new_book_dict)
    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail={"message": "Can`t add book to database"})
    
@router.patch("/edit/{book_id}")
async def edit_book(book: BookUpdate, book_id: int, db: Session = Depends(get_db)):
    book_db = db.get(Book, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    
    update_data = book.model_dump(exclude_unset=True)
    try:
        for key, value in update_data.items():
            setattr(book_db, key, value)
        
        db.commit()
        db.refresh(book_db)
        return book_db
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail={"message": "Can`t edit book to database"})
    
@router.delete("/delete/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail={"message": "Book not found"})
    
    try:
        db.delete(book)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail={"message": "Can`t delete book from database"})

