from fastapi import APIRouter
from app.api.crud import books, authors
import app.routers.api_auth as api_auth

api_router = APIRouter()
api_router.include_router(books.router, 
                          prefix="/books",
                          tags=["Book"])

api_router.include_router(authors.router, 
                          prefix="/authors",
                          tags=["Author"])

api_router.include_router(api_auth.router, 
                          prefix="/user",
                          tags=["User"])