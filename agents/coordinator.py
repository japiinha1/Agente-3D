from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from agents.print_diagnostics_agent import PrintDiagnosticsAgent
from agents.printer_profile_agent import PrinterProfileAgent
from agents.repair_agent import RepairAgent
from agents.mesh_validator import MeshValidatorAgent
from agents.print_manifest_agent import PrintManifestAgent
from core.config import OUTPUT_DIR


class ProjectCoordinator:
    """Simple orchestration layer for the 3D model pipeline."""

    def __init__(self) -> None:
        self.validator = MeshValidatorAgent()
        self.repair = RepairAgent()
        self.profile = PrinterProfileAgent()
        self.manifest = PrintManifestAgent()
        self.diagnostics = PrintDiagnosticsAgent()

    async def process_upload(
        self,
        file,
        material: str,
        nozzle_mm: float,
        profile_name: str,
    ) -> Dict[str, Any]:
        if not file.filename:
            raise ValueError("Arquivo obrigatório.")

        upload_dir = OUTPUT_DIR / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)

        original_path = upload_dir / f"original_{file.filename}"
        contents = await file.read()
        original_path.write_bytes(contents)

        analysis = self.validator.analyze(original_path)

        repaired_path = None
        if not analysis.get("is_watertight", False) or not analysis.get("is_manifold", False):
            repaired_path = upload_dir / f"repaired_{Path(file.filename).stem}.stl"
            repair_result = self.repair.repair(original_path, repaired_path)
            if repair_result.get("status") == "ok":
                analysis = repair_result["analysis"]
            else:
                repaired_path = None

        profile = self.profile.choose_profile(material=material, nozzle_mm=nozzle_mm, profile_name=profile_name)
        checks = self.profile.build_preflight_report(analysis, material, nozzle_mm, profile_name)
        diagnostics = self.diagnostics.diagnose(analysis, material, nozzle_mm, profile_name)
        manifest = self.manifest.build_manifest(file.filename, analysis, checks)
        manifest["diagnostics"] = diagnostics
        manifest["print_failure_rules"] = diagnostics["issues"]
        manifest["recommended_actions"] = diagnostics["recommendations"]

        manifest_path = upload_dir / f"{Path(file.filename).stem}_manifest.json"
        self.manifest.write_manifest(manifest_path, manifest)

        return {
            "status": "processed",
            "file_name": file.filename,
            "material": material,
            "profile": profile,
            "analysis": analysis,
            "checks": checks,
            "diagnostics": diagnostics,
            "manifest_path": str(manifest_path),
            "repaired_file": str(repaired_path) if repaired_path else None,
            "recommendations": diagnostics["recommendations"] + checks.get("recommendations", []),
            "is_ready": checks.get("status") == "READY_FOR_REVIEW",
        }


__all__ = ["ProjectCoordinator"]
