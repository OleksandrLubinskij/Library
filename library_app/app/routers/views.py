from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import get_current_user
from fastapi import Depends, APIRouter
from app.api.crud.books import get_all_books
from app.api.crud.authors import get_all_authors
router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request, error: str = None):
    return templates.TemplateResponse(
        name="login.html", 
        context={"request": request, "error": error},
        request=request
    )

@router.get("/books")
async def books_page(
    request: Request,
    title: str = None,
    author_name: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    books = get_all_books(db, title=title, author_name=author_name)
    return templates.TemplateResponse(
        request=request, 
        name="books.html", 
        context={"request": request, "books": books, "user": current_user}
)

@router.get("/authors")
async def author_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    authors = get_all_authors(db)
    return templates.TemplateResponse(
        request=request, 
        name="authors.html", 
        context={"request": request, "authors": authors, "user": current_user}
)

@router.get("/admin", response_class=HTMLResponse)
async def get_admin_panel(request: Request, current_user: dict = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    if getattr(current_user, "role", None) != "admin":
        return RedirectResponse(url="/books", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(
        request=request,
        name="admin.html", 
        context={"user": current_user}
    )