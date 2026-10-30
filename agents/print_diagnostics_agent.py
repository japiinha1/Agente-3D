from __future__ import annotations

from typing import Any, Dict

from rules.print_failure_rules import diagnose_print_issues


class PrintDiagnosticsAgent:
    """Translates mesh validation risk into real printable-failure diagnosis and corrective guidance."""

    @staticmethod
    def diagnose(analysis: Dict[str, Any], material: str, nozzle_mm: float, profile_name: str = "Bambu X2D") -> Dict[str, Any]:
        return diagnose_print_issues(analysis, material, nozzle_mm, profile_name)


__all__ = ["PrintDiagnosticsAgent"]
