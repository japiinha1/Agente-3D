from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import api_router
from core.config import BASE_DIR, STATIC_DIR, TEMPLATE_DIR

app = FastAPI(title="Agente 3D", version="1.0.0")

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
app.include_router(api_router)


__all__ = ["app", "templates"]
