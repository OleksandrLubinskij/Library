from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request, error: str = None):
    return templates.TemplateResponse(
        name="login.html", 
        context={"request": request, "error": error},
        request=request
    )