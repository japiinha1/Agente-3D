from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.mesh_validator import MeshValidator


class MeshValidatorAgent:
    """Responsible for analyzing mesh integrity and printability risk."""

    @staticmethod
    def analyze(file_path: str | Path) -> Dict[str, Any]:
        return MeshValidator.analyze(file_path)


__all__ = ["MeshValidatorAgent"]
