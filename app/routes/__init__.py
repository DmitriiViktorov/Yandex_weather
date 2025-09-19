from fastapi import APIRouter
from .ui_routes import ui_router
from .api_routes import api_router

all_routes = APIRouter()
all_routes.include_router(ui_router)
all_routes.include_router(api_router)
