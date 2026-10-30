from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

for _path in (STATIC_DIR, TEMPLATE_DIR):
    _path.mkdir(parents=True, exist_ok=True)

DEFAULT_PROFILE = "Bambu X2D"
SUPPORTED_EXTENSIONS = {".stl", ".obj", ".3mf"}

__all__ = [
    "BASE_DIR",
    "OUTPUT_DIR",
    "STATIC_DIR",
    "TEMPLATE_DIR",
    "DEFAULT_PROFILE",
    "SUPPORTED_EXTENSIONS",
]
