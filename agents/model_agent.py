from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.mesh_validator import BambuRules, MeshValidator, PrintPackageBuilder


class ModelAgent:
    """Responsible for prompt-driven or procedural model preparation."""

    @staticmethod
    def prepare_model(prompt: str, **_: Any) -> Dict[str, Any]:
        return {
            "status": "pending",
            "prompt": prompt,
            "message": "Model generation is intentionally routed through a dedicated agent layer.",
        }


class RepairAgent:
    """Responsible for safety repair and mesh cleanup before print validation."""

    @staticmethod
    def repair(file_path: str | Path, output_path: str | Path) -> Dict[str, Any]:
        return MeshValidator.repair(file_path, output_path)


__all__ = ["ModelAgent", "RepairAgent"]
