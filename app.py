from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.mesh_validator import BambuRules, MeshValidator, PrintPackageBuilder

app = FastAPI(title="Agente 3D", version="0.1.0")

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
if not TEMPLATE_DIR.exists():
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "service": "Agente 3D"}


@app.post("/api/process")
async def process_model(
    file: UploadFile = File(...),
    material: str = Form("PLA"),
    nozzle_mm: float = Form(0.4),
    profile_name: str = Form("Bambu X1C"),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Arquivo obrigatório.")

    ext = Path(file.filename).suffix.lower()
    if ext not in {".stl", ".obj", ".3mf"}:
        raise HTTPException(status_code=400, detail="Formato inválido. Use STL, OBJ ou 3MF.")

    upload_dir = OUTPUT_DIR / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    original_path = upload_dir / f"original_{file.filename}"
    original_bytes = await file.read()
    original_path.write_bytes(original_bytes)

    analysis = MeshValidator.analyze(original_path)
    repaired_path = None

    if not analysis.get("is_watertight", False) or not analysis.get("is_manifold", False):
        repaired_name = f"repaired_{Path(file.filename).stem}.stl"
        repaired_path = upload_dir / repaired_name
        repair_result = MeshValidator.repair(original_path, repaired_path)
        if repair_result.get("status") == "ok":
            analysis = repair_result["analysis"]
        else:
            repaired_path = None

    config = BambuRules.choose_profile(material, nozzle_mm, profile_name)
    checks = BambuRules.build_print_report(analysis, material, nozzle_mm, profile_name)
    manifest = PrintPackageBuilder.build_manifest(file.filename, analysis, checks)
    manifest_path = upload_dir / f"{Path(file.filename).stem}_manifest.json"
    PrintPackageBuilder.write_manifest(manifest_path, manifest)

    response = {
        "status": "processed",
        "file_name": file.filename,
        "material": material,
        "profile": config,
        "analysis": analysis,
        "checks": checks,
        "manifest_path": str(manifest_path),
        "repaired_file": str(repaired_path) if repaired_path else None,
        "recommendations": checks["recommendations"],
        "is_ready": checks["status"] == "READY_FOR_REVIEW",
    }

    return JSONResponse(content=response)


@app.get("/api/manifest/{name}")
async def get_manifest(name: str):
    manifest_path = OUTPUT_DIR / "uploads" / f"{Path(name).stem}_manifest.json"
    if not manifest_path.exists():
        raise HTTPException(status_code=404, detail="Manifest not found.")
    return JSONResponse(content=json.loads(manifest_path.read_text(encoding="utf-8")))


@app.get("/api/download/{name}")
async def download_file(name: str):
    path = OUTPUT_DIR / "uploads" / name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    return FileResponse(path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=10000, reload=True)
