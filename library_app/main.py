import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # <-- Перевір цей імпорт!
from app.routers import endpoints, views

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(views.router)
app.include_router(endpoints.api_router)
