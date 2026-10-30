from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from agents.coordinator import ProjectCoordinator
from core.config import OUTPUT_DIR, STATIC_DIR, TEMPLATE_DIR

api_router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@api_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@api_router.get("/health")
async def health():
    return {"status": "ok", "service": "Agente 3D"}


@api_router.post("/api/process")
async def process_model(
    file: UploadFile = File(...),
    material: str = Form("PLA"),
    nozzle_mm: float = Form(0.4),
    profile_name: str = Form("Bambu X2D"),
):
    coordinator = ProjectCoordinator()
    try:
        result = await coordinator.process_upload(
            file=file,
            material=material,
            nozzle_mm=nozzle_mm,
            profile_name=profile_name,
        )
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive safety net
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o arquivo: {exc}") from exc


@api_router.get("/api/manifest/{name}")
async def get_manifest(name: str):
    manifest_path = OUTPUT_DIR / "uploads" / f"{name}.json"
    if not manifest_path.exists():
        manifest_path = OUTPUT_DIR / "uploads" / f"{name}_manifest.json"
    if not manifest_path.exists():
        raise HTTPException(status_code=404, detail="Manifest not found.")
    return JSONResponse(content=__import__("json").loads(manifest_path.read_text(encoding="utf-8")))


@api_router.get("/api/download/{name}")
async def download_file(name: str):
    path = OUTPUT_DIR / "uploads" / name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    return FileResponse(path)


__all__ = ["api_router"]
