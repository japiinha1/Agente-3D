from __future__ import annotations

from typing import Any, Dict

from src.mesh_validator import BambuRules


class PrinterProfileAgent:
    """Responsible for printer-specific profile generation and preflight rules."""

    @staticmethod
    def choose_profile(material: str, nozzle_mm: float, profile_name: str = "Bambu X2D") -> Dict[str, Any]:
        return BambuRules.choose_profile(material, nozzle_mm, profile_name)

    @staticmethod
    def build_preflight_report(analysis: Dict[str, Any], material: str, nozzle_mm: float, profile_name: str = "Bambu X2D") -> Dict[str, Any]:
        return BambuRules.build_print_report(analysis, material, nozzle_mm, profile_name)


__all__ = ["PrinterProfileAgent"]
