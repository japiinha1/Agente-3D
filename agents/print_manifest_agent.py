from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.mesh_validator import PrintPackageBuilder


class PrintManifestAgent:
    """Responsible for generating artifacts for pre-print review."""

    @staticmethod
    def build_manifest(file_name: str, analysis: Dict[str, Any], print_report: Dict[str, Any]) -> Dict[str, Any]:
        return PrintPackageBuilder.build_manifest(file_name, analysis, print_report)

    @staticmethod
    def write_manifest(path: str | Path, payload: Dict[str, Any]) -> str:
        return PrintPackageBuilder.write_manifest(path, payload)


__all__ = ["PrintManifestAgent"]
