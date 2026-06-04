from pydantic import BaseModel
from typing import Optional
class BookCreate(BaseModel):
    title: str
    genre: str
    release_year: int
    author_id: int

class AuthorCreate(BaseModel):
    firstname: str
    lastname: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class BookUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    author_id: Optional[int] = None

class UserLogin(BaseModel):
    username: str
    password: str