from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import trimesh


class MeshValidator:
    """Robust mesh validation and print-preflight diagnostics."""

    @staticmethod
    def load_mesh(file_path: str | Path):
        mesh = trimesh.load(str(file_path), force="mesh", allow_empty=True)
        if mesh is None:
            return None

        if isinstance(mesh, trimesh.Scene):
            try:
                mesh = mesh.dump(concatenate=True)
            except Exception:
                return None

        if isinstance(mesh, trimesh.Trimesh):
            return mesh

        return None

    @staticmethod
    def analyze(file_path: str | Path) -> Dict[str, Any]:
        mesh = MeshValidator.load_mesh(file_path)

        if mesh is None:
            return {
                "status": "invalid",
                "is_watertight": False,
                "is_manifold": False,
                "issues": ["Could not load mesh."],
                "volume": 0.0,
                "bounds": [0.0, 0.0, 0.0],
                "face_count": 0,
                "vertex_count": 0,
                "extents_mm": [0.0, 0.0, 0.0],
            }

        issues: List[str] = []
        volume = float(mesh.volume) if np.isfinite(mesh.volume) else 0.0
        bounds = mesh.bounds.tolist() if hasattr(mesh.bounds, "tolist") else [0.0, 0.0, 0.0]
        extents = np.abs(np.diff(bounds, axis=0)[0]).tolist() if isinstance(bounds, list) else [0.0, 0.0, 0.0]

        if mesh.is_watertight is False:
            issues.append("Mesh is not watertight: open edges or holes detected.")
        if mesh.is_volume is False:
            issues.append("Mesh is not manifold / not a solid printable volume.")
        if mesh.body_count > 1:
            issues.append("Object contains multiple disconnected bodies. Consider merging or splitting.")
        if len(mesh.vertices) == 0:
            issues.append("Mesh has no vertices.")
        if volume <= 0:
            issues.append("Volume is zero or invalid.")

        if max(extents or [0.0, 0.0, 0.0]) < 1e-6:
            issues.append("Mesh dimensions are degenerate.")

        return {
            "status": "ok" if not issues else "warnings",
            "is_watertight": bool(mesh.is_watertight),
            "is_manifold": bool(mesh.is_volume),
            "issues": issues,
            "volume": float(volume),
            "bounds": bounds,
            "face_count": int(len(mesh.faces)),
            "vertex_count": int(len(mesh.vertices)),
            "extents_mm": [float(v) for v in extents],
            "body_count": int(getattr(mesh, "body_count", 1)),
        }

    @staticmethod
    def repair(file_path: str | Path, output_path: str | Path) -> Dict[str, Any]:
        mesh = MeshValidator.load_mesh(file_path)
        if mesh is None:
            return {"status": "failed", "message": "Could not load mesh to repair."}

        repaired = mesh.copy()

        try:
            repaired.remove_unreferenced_vertices()
        except Exception:
            pass

        try:
            repaired.fix_normals()
        except Exception:
            pass

        try:
            if not repaired.is_watertight:
                repaired = repaired.fill_holes()
        except Exception:
            pass

        try:
            repaired.export(str(output_path))
        except Exception:
            alt = Path(str(output_path)).with_suffix(".stl")
            repaired.export(str(alt))
            return {"status": "ok", "analysis": MeshValidator.analyze(alt), "output": str(alt)}

        analysis = MeshValidator.analyze(output_path)
        return {
            "status": "ok" if analysis["status"] != "invalid" else "warning",
            "analysis": analysis,
            "output": str(output_path),
        }


class BambuRules:
    """Material presets and printability heuristics for Bambu-compatible workflows."""

    MATERIALS = {
        "PLA": {
            "nozzle_temp_c": 215,
            "bed_temp_c": 60,
            "flow_ratio": 1.0,
            "speed_mult": 1.0,
            "supports": "tree",
            "layer_height": 0.2,
            "min_wall_thickness": 0.45,
            "min_feature_size": 0.8,
            "notes": "Balanced material for prototypes and detailed prints."
        },
        "PETG": {
            "nozzle_temp_c": 240,
            "bed_temp_c": 80,
            "flow_ratio": 1.06,
            "speed_mult": 0.9,
            "supports": "tree",
            "layer_height": 0.2,
            "min_wall_thickness": 0.55,
            "min_feature_size": 1.0,
            "notes": "Use lower speed and stronger cooling path."
        },
        "ABS": {
            "nozzle_temp_c": 250,
            "bed_temp_c": 100,
            "flow_ratio": 1.08,
            "speed_mult": 0.8,
            "supports": "tree",
            "layer_height": 0.2,
            "min_wall_thickness": 0.6,
            "min_feature_size": 1.1,
            "notes": "Needs chamber and good bed adhesion."
        },
        "ASA": {
            "nozzle_temp_c": 255,
            "bed_temp_c": 100,
            "flow_ratio": 1.09,
            "speed_mult": 0.8,
            "supports": "tree",
            "layer_height": 0.2,
            "min_wall_thickness": 0.6,
            "min_feature_size": 1.1,
            "notes": "Good for outdoor use; control thermal shrink."
        },
    }

    @staticmethod
    def choose_profile(material: str, nozzle_mm: float, profile_name: str = "Bambu X1C") -> Dict[str, Any]:
        material_key = str(material).upper()
        base = BambuRules.MATERIALS.get(material_key, BambuRules.MATERIALS["PLA"])

        if nozzle_mm <= 0.4:
            layer_height = 0.2
        elif nozzle_mm <= 0.6:
            layer_height = 0.28
        else:
            layer_height = 0.32

        return {
            "machine": profile_name,
            "material": material_key,
            "nozzle_mm": float(nozzle_mm),
            "layer_height_mm": float(layer_height),
            "nozzle_temp_c": int(base["nozzle_temp_c"]),
            "bed_temp_c": int(base["bed_temp_c"]),
            "flow_ratio": float(base["flow_ratio"]),
            "speed_multiplier": float(base["speed_mult"]),
            "supports": base["supports"],
            "min_wall_thickness_mm": float(base["min_wall_thickness"]),
            "min_feature_size_mm": float(base["min_feature_size"]),
            "notes": base["notes"],
        }

    @staticmethod
    def build_print_report(analysis: Dict[str, Any], material: str, nozzle_mm: float, profile_name: str = "Bambu X1C") -> Dict[str, Any]:
        profile = BambuRules.choose_profile(material, nozzle_mm, profile_name)
        issues: List[str] = []
        recommendations: List[str] = []

        score = 100

        if not analysis.get("is_watertight", False):
            score -= 35
            issues.append("Model is not watertight.")
            recommendations.append("Repair holes and open edges before printing.")

        if not analysis.get("is_manifold", False):
            score -= 25
            issues.append("Model is not manifold.")
            recommendations.append("Run mesh repair or boolean union to make it a solid volume.")

        if float(analysis.get("volume", 0.0)) <= 0:
            score -= 20
            issues.append("Volume is invalid.")
            recommendations.append("Check if the mesh is loaded with correct dimensions and orientation.")

        extents = analysis.get("extents_mm", [0.0, 0.0, 0.0])
        if max(extents or [0.0, 0.0, 0.0]) > 250:
            recommendations.append("Large part: consider splitting into sections to improve dimensional stability and support behavior.")

        if analysis.get("body_count", 1) > 1:
            score -= 10
            recommendations.append("Multiple bodies detected; merge or isolate them before final slicing.")

        # heuristics for thin-wall and fragile geometry
        if max(extents or [0.0, 0.0, 0.0]) > 0 and profile["min_wall_thickness_mm"] > 0:
            if max(extents) < 6:
                recommendations.append("Small part: verify nozzle and wall thickness are compatible with the chosen nozzle size.")

        if score < 70:
            status = "NEEDS_REPAIR"
        elif score < 90:
            status = "REVIEW_REQUIRED"
        else:
            status = "READY_FOR_REVIEW"

        return {
            "status": status,
            "printability_score": max(0, min(100, int(score))),
            "profile": profile,
            "issues": issues,
            "recommendations": recommendations,
            "summary": {
                "volume_mm3": round(float(analysis.get("volume", 0.0)), 3),
                "face_count": int(analysis.get("face_count", 0)),
                "vertex_count": int(analysis.get("vertex_count", 0)),
                "bounds_mm": analysis.get("bounds", [0.0, 0.0, 0.0]),
                "extents_mm": analysis.get("extents_mm", [0.0, 0.0, 0.0]),
            },
        }


class PrintPackageBuilder:
    """Generate a print-prep manifest that can be reviewed before slicing."""

    @staticmethod
    def build_manifest(file_name: str, analysis: Dict[str, Any], print_report: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "package_name": file_name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "model_summary": {
                "volume_mm3": round(float(analysis.get("volume", 0.0)), 3),
                "vertex_count": int(analysis.get("vertex_count", 0)),
                "face_count": int(analysis.get("face_count", 0)),
                "bounds_mm": analysis.get("bounds", [0.0, 0.0, 0.0]),
                "extents_mm": analysis.get("extents_mm", [0.0, 0.0, 0.0]),
                "is_watertight": bool(analysis.get("is_watertight", False)),
                "is_manifold": bool(analysis.get("is_manifold", False)),
            },
            "bambu_profile": print_report["profile"],
            "printability": {
                "score": print_report["printability_score"],
                "status": print_report["status"],
                "issues": print_report["issues"],
                "recommendations": print_report["recommendations"],
            },
            "notes": [
                "This manifest is a pre-flight validation package for Bambu Studio.",
                "The final slicing and G-code generation still happens in the official Bambu Studio slicer.",
                "Use the profile and recommendations only as a preparation layer before sending to the printer."
            ],
        }

    @staticmethod
    def write_manifest(path: str | Path, payload: Dict[str, Any]) -> str:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return str(out)


__all__ = ["MeshValidator", "BambuRules", "PrintPackageBuilder"]

