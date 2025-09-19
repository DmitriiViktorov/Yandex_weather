from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


ui_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@ui_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        }
    )

@ui_router.get("/choose", response_class=HTMLResponse)
async def choose(request: Request, city: str):
    return templates.TemplateResponse(
        "choose.html",
        {
            "request": request,
            "search_query": city,
        },
    )
