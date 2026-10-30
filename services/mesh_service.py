from __future__ import annotations

from typing import Any, Dict

from agents.mesh_validator import MeshValidatorAgent
from agents.printer_profile_agent import PrinterProfileAgent
from agents.repair_agent import RepairAgent
from core.config import OUTPUT_DIR


class MeshService:
    """Service layer for mesh validation and preparation."""

    def __init__(self) -> None:
        self.validator = MeshValidatorAgent()
        self.repair = RepairAgent()
        self.profile = PrinterProfileAgent()

    def analyze(self, path: str):
        return self.validator.analyze(path)

    def repair(self, source: str, target: str):
        return self.repair.repair(source, target)

    def profile_for(self, material: str, nozzle_mm: float, profile_name: str):
        return self.profile.choose_profile(material, nozzle_mm, profile_name)


__all__ = ["MeshService"]
