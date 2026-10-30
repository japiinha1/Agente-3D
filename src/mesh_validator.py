from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import trimesh
    import numpy as np
except Exception as exc:  # pragma: no cover
    raise RuntimeError(f"Missing runtime dependencies: {exc}") from exc


class MeshValidator:
    """Core 3D mesh validation and repair helper."""

    @staticmethod
    def load_mesh(file_path: str | Path):
        return trimesh.load(file_path, force="mesh", allow_empty=True)

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
            }

        issues: List[str] = []

        if not isinstance(mesh, trimesh.Trimesh):
            return {
                "status": "invalid",
                "is_watertight": False,
                "is_manifold": False,
                "issues": ["Loaded object is not a single triangle mesh."],
                "volume": 0.0,
                "bounds": [0.0, 0.0, 0.0],
            }

        is_watertight = mesh.is_watertight
        is_manifold = mesh.is_volume
        if not is_watertight:
            issues.append("Mesh is not watertight / has open edges.")
        if not is_manifold:
            issues.append("Mesh is not manifold / not a closed printable volume.")

        if mesh.body_count > 1:
            issues.append("Mesh contains multiple bodies; print preparation may require boolean merge.")

        if len(mesh.vertices) == 0:
            issues.append("Mesh has no vertices.")

        volume = float(mesh.volume) if np.isfinite(mesh.volume) else 0.0
        bounds = mesh.bounds.tolist() if hasattr(mesh.bounds, "tolist") else [0.0, 0.0, 0.0]

        scale = np.abs(np.diff(bounds, axis=0)).max() if bounds else 0.0
        if scale <= 0:
            issues.append("Mesh dimensions are degenerate.")

        return {
            "status": "ok" if not issues else "warnings",
            "is_watertight": bool(is_watertight),
            "is_manifold": bool(is_manifold),
            "issues": issues,
            "volume": volume,
            "bounds": bounds,
            "face_count": int(len(mesh.faces)),
            "vertex_count": int(len(mesh.vertices)),
        }

    @staticmethod
    def repair(file_path: str | Path, output_path: str | Path) -> Dict[str, Any]:
        mesh = MeshValidator.load_mesh(file_path)
        if mesh is None:
            return {"status": "failed", "message": "Could not load mesh to repair."}

        repaired = mesh.copy()
        try:
            repaired.update_faces(repaired.faces)
        except Exception:
            pass

        # Basic cleanup heuristics
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
                repaired.fill_holes()
        except Exception:
            pass

        try:
            repaired.export(output_path)
        except Exception:
            # fallback: export to STL if generic export fails
            repaired.export(output_path.with_suffix(".stl"))

        analysis = MeshValidator.analyze(output_path)
        return {
            "status": "ok" if analysis["status"] != "invalid" else "warning",
            "analysis": analysis,
            "output": str(output_path),
        }


class BambuRules:
    """Static material and print settings for Bambu-compatible workflows."""

    MATERIALS = {
        "PLA": {
            "nozzle_temp_c": 215,
            "bed_temp_c": 60,
            "flow_ratio": 1.00,
            "speed_mult": 1.0,
            "supports": "tree",
            "layer_height": 0.20,
            "min_wall_thickness": 0.45,
            "min_feature_size": 0.8,
            "notes": "Good for everyday prototyping and detailed parts."
        },
        "PETG": {
            "nozzle_temp_c": 240,
            "bed_temp_c": 80,
            "flow_ratio": 1.06,
            "speed_mult": 0.9,
            "supports": "tree",
            "layer_height": 0.20,
            "min_wall_thickness": 0.55,
            "min_feature_size": 1.0,
            "notes": "Better for durability; increase cooling and reduce retraction stress."
        },
        "ABS": {
            "nozzle_temp_c": 250,
            "bed_temp_c": 100,
            "flow_ratio": 1.08,
            "speed_mult": 0.8,
            "supports": "tree",
            "layer_height": 0.20,
            "min_wall_thickness": 0.6,
            "min_feature_size": 1.1,
            "notes": "Need enclosure or strong chamber control; watch for warping." 
        },
        "ASA": {
            "nozzle_temp_c": 255,
            "bed_temp_c": 100,
            "flow_ratio": 1.09,
            "speed_mult": 0.8,
            "supports": "tree",
            "layer_height": 0.20,
            "min_wall_thickness": 0.6,
            "min_feature_size": 1.1,
            "notes": "Very good for outdoor use; chamber and bed adhesion matter." 
        },
    }

    @staticmethod
    def choose_profile(material: str, nozzle_mm: float, profile_name: str = "Bambu X1C") -> Dict[str, Any]:
        material_key = str(material).upper()
        base = BambuRules.MATERIALS.get(material_key, BambuRules.MATERIALS["PLA"])

        layer = 0.20
        if nozzle_mm in (0.2, 0.25, 0.3, 0.4, 0.6, 0.8):
            layer = 0.20 if nozzle_mm <= 0.4 else 0.28

        return {
            "machine": profile_name,
            "material": material_key,
            "nozzle_mm": float(nozzle_mm),
            "layer_height_mm": float(layer),
            "nozzle_temp_c": int(base["nozzle_temp_c"]),
            "bed_temp_c": int(base["bed_temp_c"]),
            "flow_ratio": float(base["flow_ratio"]),
            "speed_multiplier": float(base["speed_mult"]),
            "supports": base["supports"],
            "wall_thickness_min_mm": float(base["min_wall_thickness"]),
            "min_feature_size_mm": float(base["min_feature_size"]),
            "notes": base["notes"],
        }

    @staticmethod
    def build_print_checks(analysis: Dict[str, Any], material: str, nozzle_mm: float) -> Dict[str, Any]:
        profile = BambuRules.choose_profile(material, nozzle_mm)
        issues: List[str] = []
        recommendations: List[str] = []

        if not analysis.get("is_watertight", False):
            issues.append("Model is not watertight. Repair the mesh before printing.")
            recommendations.append("Fix holes and non-manifold edges in the mesh.")

        if not analysis.get("is_manifold", False):
            issues.append("Model likely fails manifold validation.")
            recommendations.append("Run a boolean union or mesh repair and re-check the mesh.")

        volume = float(analysis.get("volume", 0.0))
        if volume <= 0.0:
            issues.append("Calculated volume is invalid or zero.")
            recommendations.append("Validate the model origin and geometry before printing.")

        bounds = analysis.get("bounds", [0, 0, 0])
        if len(bounds) >= 3:
            extents = [float(bounds[1][0] - bounds[0][0]), float(bounds[1][1] - bounds[0][1]), float(bounds[1][2] - bounds[0][2])]
            if max(extents) > 250:
                recommendations.append("Large part: consider splitting for better print stability and support control.")

        return {
            "profile": profile,
            "issues": issues,
            "recommendations": recommendations,
            "status": "ready" if not issues else "needs_attention",
        }


class PrintPackageBuilder:
    """Builds a Bambu-compatible print package manifest."""

    @staticmethod
    def build_manifest(file_name: str, analysis: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "package_name": file_name,
            "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
            "model_summary": {
                "volume_mm3": round(float(analysis.get("volume", 0.0)), 3),
                "vertex_count": int(analysis.get("vertex_count", 0)),
                "face_count": int(analysis.get("face_count", 0)),
                "bounds": analysis.get("bounds", [0.0, 0.0, 0.0]),
                "is_watertight": bool(analysis.get("is_watertight", False)),
                "is_manifold": bool(analysis.get("is_manifold", False)),
            },
            "bambu_profile": config,
            "notes": [
                "This package is intended for validation and print preparation. For a final .3mf/.gcode, open it in Bambu Studio and use the generated settings.",
                "The mesh must be corrected before sending to the printer.",
            ],
        }

    @staticmethod
    def write_manifest(path: str | Path, payload: Dict[str, Any]) -> str:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return str(out)


__all__ = ["MeshValidator", "BambuRules", "PrintPackageBuilder"]

