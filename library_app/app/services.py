from fastapi import Cookie, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud.users import get_user_by_username
from app.core.config import settings

def get_current_user(access_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY ,algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Damaged or expired token")
    
    user = get_user_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_UNAUTHORIZED, detail="User not found")
    
    return user

def get_current_user_or_redirect(access_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                            headers={"Location": "/login"})
    
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:

            raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                            headers={"Location": "/login"})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                            headers={"Location": "/login"})
    
    user = get_user_by_username(username=username, db=db)
    if user is None:
        print(F"user: {user}")
        raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                            headers={"Location": "/login"})
    
    return user