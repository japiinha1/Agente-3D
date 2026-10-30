from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.mesh_validator import BambuRules, MeshValidator


class RepairAgent:
    """Responsible for mesh repair and post-repair validation."""

    @staticmethod
    def repair(file_path: str | Path, output_path: str | Path) -> Dict[str, Any]:
        return MeshValidator.repair(file_path, output_path)


__all__ = ["RepairAgent"]
