from fastapi import APIRouter
from app.api.crud import books, authors

api_router = APIRouter()
api_router.include_router(books.router, 
                          prefix="/books",
                          tags=["Book"])

api_router.include_router(authors.router, 
                          prefix="/authors",
                          tags=["Author"])