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

X2D_PROFILE = {
    "machine": "Bambu X2D",
    "build_volume_mm": {
        "x": 256.0,
        "y": 256.0,
        "z": 260.0,
    },
    "dual_nozzle_build_volume_mm": {
        "x": 235.5,
        "y": 256.0,
        "z": 256.0,
    },
    "included_nozzle_mm": 0.4,
    "supported_nozzles_mm": [0.2, 0.4, 0.6, 0.8],
    "max_nozzle_temp_c": 300,
    "materials": [
        "PLA",
        "PETG",
        "ABS",
        "ASA",
        "TPU",
        "PA",
        "PET",
        "PC",
        "PVA",
        "PLA-CF",
        "PETG-CF",
        "ABS-CF",
        "ASA-CF",
    ],
    "notes": "Official Bambu Lab X2D values from the public printer documentation and user manual data.",
}

__all__ = [
    "BASE_DIR",
    "OUTPUT_DIR",
    "STATIC_DIR",
    "TEMPLATE_DIR",
    "DEFAULT_PROFILE",
    "SUPPORTED_EXTENSIONS",
    "X2D_PROFILE",
]
