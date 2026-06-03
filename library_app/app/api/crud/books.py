from fastapi import Depends, HTTPException, APIRouter
from app.models import Book, Author
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas import BookCreate, BookUpdate
from typing import Optional
import io
import pandas as pd
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/export")
async def export_books_to_excel(db: Session = Depends(get_db)):
    try:
        stmt = select(Book).join(Book.author)
        books = db.execute(stmt).scalars().all()
        if not books:
            raise HTTPException(status_code=404, detail={"message": "Books not found"})
        data = []
        for i, book in enumerate(books):
            data.append({
                "ID": book.id,
                "Title": book.title,
                "Genre": book.genre,
                "Release year": book.release_year,
                "Author": f"{book.author.lastname} {book.author.firstname}"
            })
        df = pd.DataFrame(data)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Books Catalog")
        buffer.seek(0)
        headers = {
            'Content-Disposition': 'attachment; filename="books_catalog.xlsx"'
        }
        
        return StreamingResponse(
            buffer, 
            headers=headers, 
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail={"message": f"Error during export: {e}"})

    
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

