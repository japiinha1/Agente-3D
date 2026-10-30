from __future__ import annotations

from typing import Any, Dict, List


PRINT_FAILURE_RULES: List[Dict[str, Any]] = [
    {
        "name": "warping",
        "summary": "Edges curl up and the model lifts from the bed.",
        "symptoms": [
            "corner lifting",
            "edge curl",
            "first layer detachment",
            "part twists during print",
        ],
        "probable_causes": [
            "bed too cold for material",
            "poor first layer calibration",
            "drafts or thermal shock",
            "high print area or large flat surfaces",
        ],
        "fixes": [
            "increase bed temperature within material limits",
            "use brim or raft for large footprints",
            "improve first layer squish and bed leveling",
            "keep a clean, draft-free environment",
        ],
        "material_notes": {
            "PLA": "Use 50-60C bed and good first layer adhesion.",
            "PETG": "Keep bed stable and avoid excessive cooling.",
            "ABS": "Use enclosure and controlled chamber temperature.",
            "ASA": "Use enclosure and keep thermal variation low.",
        },
        "severity": "high",
    },
    {
        "name": "poor_bed_adhesion",
        "summary": "The part does not stick reliably to the print surface.",
        "symptoms": [
            "part shifts mid-print",
            "first layer peeling",
            "edges detach after several layers",
        ],
        "probable_causes": [
            "dirty or uneven bed",
            "bad first-layer height",
            "insufficient bed temperature",
            "small contact area",
        ],
        "fixes": [
            "clean the bed with isopropyl alcohol",
            "level the bed and validate first layer calibration",
            "use brim or textured PEI surface when needed",
            "increase bed temperature within the material window",
        ],
        "material_notes": {
            "PLA": "Use moderate bed heat and a clean surface.",
            "PETG": "Careful with excessive nozzle cooling.",
            "ABS": "Use a hotter bed and enclosed chamber.",
            "ASA": "Use stable bed temperature and enclosure.",
        },
        "severity": "high",
    },
    {
        "name": "under_extrusion",
        "summary": "The filament does not fully fill the bead path.",
        "symptoms": [
            "thin walls",
            "gaps between lines",
            "weak layers",
            "missing infill",
        ],
        "probable_causes": [
            "low nozzle temperature",
            "partially clogged nozzle",
            "flow set too low",
            "incorrect filament diameter or profile",
        ],
        "fixes": [
            "increase nozzle temperature within material limits",
            "check filament diameter and flow calibration",
            "clean or replace nozzle if clogged",
            "review extrusion multiplier and volumetric flow",
        ],
        "material_notes": {
            "PLA": "Increase heat gradually if underextruding.",
            "PETG": "Keep nozzle temperature stable and avoid moisture.",
            "ABS": "Higher temperature can reduce underextrusion but should stay within limits.",
            "ASA": "Use proper material-specific temperature profile.",
        },
        "severity": "high",
    },
    {
        "name": "over_extrusion",
        "summary": "Too much material is deposited, causing rough or blocked details.",
        "symptoms": [
            "blobs on walls",
            "oversized top layers",
            "poor corners",
            "zits and ridges",
        ],
        "probable_causes": [
            "flow too high",
            "nozzle too hot",
            "overly aggressive extrusion calibration",
        ],
        "fixes": [
            "reduce flow ratio",
            "lower nozzle temp within the safe range",
            "calibrate extrusion multiplier",
            "check line width and layer height consistency",
        ],
        "material_notes": {
            "PLA": "Lower flow only if over-deposition is obvious.",
            "PETG": "Consider a slight reduction in flow to avoid blobs.",
            "ABS": "Keep flow stable and avoid excessive heat.",
            "ASA": "Flow tuning matters because of thermal shrink.",
        },
        "severity": "medium",
    },
    {
        "name": "stringing",
        "summary": "Thin plastic hairs appear between parts of the model.",
        "symptoms": [
            "hairy surfaces",
            "strings between features",
            "stringing across gaps",
        ],
        "probable_causes": [
            "nozzle too hot",
            "retraction settings too weak",
            "high travel speed or poor wipe settings",
        ],
        "fixes": [
            "lower nozzle temperature slightly",
            "increase retraction and tune wipe settings",
            "reduce traveling time between features",
        ],
        "material_notes": {
            "PLA": "Stringing is common with higher temps.",
            "PETG": "Keep retraction and speeds tuned to avoid stretch.",
            "ABS": "Material can be more challenging with stringing if hot.",
            "ASA": "Need stable temperature and retraction tuning.",
        },
        "severity": "medium",
    },
    {
        "name": "support_failure",
        "summary": "Supports break or do not sustain overhangs correctly.",
        "symptoms": [
            "supports snap away",
            "overhangs droop",
            "loose supports under bridges",
        ],
        "probable_causes": [
            "support density too low",
            "bad orientation",
            "weak support interface",
            "material not suited to support structure",
        ],
        "fixes": [
            "reorient the model to reduce unsupported spans",
            "increase support density and contact area",
            "use tree supports or line support where appropriate",
            "test support interface settings for the chosen material",
        ],
        "material_notes": {
            "PLA": "Good for simple support geometry and tree supports.",
            "PETG": "Use tuned support interface to avoid difficult removal.",
            "ABS": "Support strategy matters more because of shrinkage.",
            "ASA": "Need stable support settings under thermal stress.",
        },
        "severity": "high",
    },
    {
        "name": "overhang_issues",
        "summary": "Steep overhangs are not printed correctly without support.",
        "symptoms": [
            "hanging surfaces sag",
            "filament droops at steep angles",
            "layers undercut or fail",
        ],
        "probable_causes": [
            "orientation not optimized",
            "cooling insufficient",
            "support not placed correctly",
        ],
        "fixes": [
            "rotate the model to reduce steep overhangs",
            "add support with denser support interface",
            "improve cooling and reduce excessive heat",
        ],
        "material_notes": {
            "PLA": "Lower overhang risk than many materials.",
            "PETG": "Requires stable cooling and support planning.",
            "ABS": "Cooling must be balanced because of shrink and warping.",
            "ASA": "Keep support and thermal control tuned.",
        },
        "severity": "high",
    },
    {
        "name": "layer_shift",
        "summary": "Printed layers are offset sideways and the print is misaligned.",
        "symptoms": [
            "misaligned round features",
            "z-axis pattern offset",
            "layers not aligned",
        ],
        "probable_causes": [
            "belt tension issues",
            "loose mechanical parts",
            "motor skipping",
            "accelerations too aggressive",
        ],
        "fixes": [
            "check belt tension and axis motion",
            "tighten mechanical fasteners",
            "reduce print acceleration or jerk",
            "verify V-slot and carriage movement",
        ],
        "material_notes": {
            "PLA": "Layer shift is often mechanical not material-related.",
            "PETG": "Keep acceleration stable as material can be heavier to deposit.",
            "ABS": "Mechanical stability matters more with thermal drift.",
            "ASA": "Machine stability and motion tuning are critical.",
        },
        "severity": "critical",
    },
    {
        "name": "mesh_non_manifold",
        "summary": "The mesh is not a valid watertight solid for printing.",
        "symptoms": [
            "open edges",
            "holes",
            "inverted normals",
            "multiple disconnected shells",
        ],
        "probable_causes": [
            "bad STL export",
            "duplicate faces",
            "non-manifold geometry",
            "mesh reconstruction issues",
        ],
        "fixes": [
            "repair mesh and weld vertices",
            "close holes and remove duplicate faces",
            "merge disconnected shells",
            "re-export from a solid modeling source",
        ],
        "material_notes": {
            "PLA": "Any bad mesh creates print failures regardless of material.",
            "PETG": "Mesh integrity is still the first condition.",
            "ABS": "Repair before printing even if material is otherwise suitable.",
            "ASA": "Mesh quality must be clean before thermal stress is considered.",
        },
        "severity": "critical",
    },
]


def diagnose_print_issues(analysis: Dict[str, Any], material: str, nozzle_mm: float, profile_name: str = "Bambu X2D") -> Dict[str, Any]:
    material_key = str(material).upper()
    findings: List[Dict[str, Any]] = []

    if not analysis.get("is_watertight", False) or not analysis.get("is_manifold", False):
        findings.append({
            "name": "mesh_non_manifold",
            "severity": "critical",
            "confidence": 0.95,
            "summary": "The mesh is not currently a valid printable solid.",
            "recommendation": "Run mesh repair before printing.",
        })

    support_risk = float(analysis.get("support_risk", 0.0))
    warping_risk = float(analysis.get("warping_risk", 0.0))
    adhesion_risk = float(analysis.get("adhesion_risk", 0.0))

    if support_risk > 0.5:
        findings.append({
            "name": "support_failure",
            "severity": "high",
            "confidence": 0.8,
            "summary": "The model has significant overhang support risk.",
            "recommendation": "Rotate the model or add stronger support structures.",
        })

    if warping_risk > 0.6:
        findings.append({
            "name": "warping",
            "severity": "high",
            "confidence": 0.82,
            "summary": "The object has a high tendency to lift from the bed during printing.",
            "recommendation": "Increase bed adhesion and use brim/raft as needed.",
        })

    if adhesion_risk > 0.7:
        findings.append({
            "name": "poor_bed_adhesion",
            "severity": "high",
            "confidence": 0.85,
            "summary": "The first layer may not be stable enough for a reliable print.",
            "recommendation": "Improve bed calibration and first-layer contact.",
        })

    if support_risk < 0.2 and warping_risk < 0.3 and adhesion_risk < 0.3:
        findings.append({
            "name": "printability_ok",
            "severity": "low",
            "confidence": 0.7,
            "summary": "No strong risk flags in the current mesh analysis.",
            "recommendation": "Proceed with standard material-specific preflight review.",
        })

    actions: List[str] = []
    for issue in findings:
        rule = next((r for r in PRINT_FAILURE_RULES if r["name"] == issue["name"]), None)
        if rule is None:
            continue
        actions.extend(rule.get("fixes", []))

    if material_key:
        material_rule = next((r for r in PRINT_FAILURE_RULES if r["name"] == "warping"), None)
        if material_rule and material_key in material_rule.get("material_notes", {}):
            actions.append(material_rule["material_notes"][material_key])

    return {
        "profile_name": profile_name,
        "material": material_key,
        "nozzle_mm": float(nozzle_mm),
        "issues": findings,
        "recommendations": list(dict.fromkeys(actions)),
        "summary": {
            "support_risk": round(float(support_risk), 3),
            "warping_risk": round(float(warping_risk), 3),
            "adhesion_risk": round(float(adhesion_risk), 3),
        },
    }


__all__ = ["PRINT_FAILURE_RULES", "diagnose_print_issues"]
