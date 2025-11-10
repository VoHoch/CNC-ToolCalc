"""Intelligent preset matching with 3-level fallback strategy."""

import logging
from typing import Optional, Tuple, List, Dict
from difflib import get_close_matches

logger = logging.getLogger(__name__)


# Level 1: Exact Matches
EXACT_OPERATION_MATCHES = {
    "FINISH_SLOT_OP": [
        "Finish Slot",
        "Slot: Finish",
        "Slot Finish",
        "FinishSlot",
        "Finish Contour",
        "Contour: Finish",
        "Schlicht(F)",
        "Kontur"
    ],
    "RADIUS_CONTOUR_OP": [
        "Radius Contour",
        "Contour: Radius",
        "Contour Radius",
        "RadiusContour",
        "Abrunden",
        "Schlicht(R)"
    ],
    "CHAMFER_CONTOUR_OP": [
        "Chamfer Contour",
        "Contour: Chamfer",
        "Chamfer",
        "Fase"
    ],
    "BALL_3D_OP": [
        "Ball-End 3D",
        "Contour: Ball-End 3D",
        "Ball End",
        "Ball 3D",
        "Kugelfräser",
        "Kugel"
    ],
    "ROUGH_FACE_OP": [
        "Face: Rough",
        "Rough Face",
        "Face Rough",
        "Planen (Grob)",
        "Planen Grob",
        "Schruppen"
    ],
    "FINISH_FACE_OP": [
        "Face: Finish",
        "Finish Face",
        "Face Finish",
        "Planen (Fein)",
        "Planen Fein"
    ],
    "PARTIAL_SLOT_OP": [
        "Slot: Partial",
        "Partial Slot",
        "Partial",
        "Teilschnitt",
        "Tasche"
    ],
    "FULL_SLOT_OP": [
        "Slot: Full",
        "Full Slot",
        "Full",
        "Vollschnitt",
        "Vollnut"
    ],
    "TROCHOIDAL_SLOT_OP": [
        "Slot: Trochoidal",
        "Trochoidal Slot",
        "Trochoidal",
        "Adaptiv",
        "Adaptive"
    ],
    "DRILLING_OP": [
        "Special: Drilling",
        "Drilling",
        "Drill",
        "Bohren"
    ],
    "VGROOVE_OP": [
        "Special: V-Groove",
        "V-Groove",
        "V Groove",
        "Gravur",
        "Engraving"
    ],
    "THREADING_OP": [
        "Special: Threading",
        "Threading",
        "Thread",
        "Gewinde"
    ]
}

EXACT_MATERIAL_MATCHES = {
    "Aluminium": [
        "Aluminium",
        "Aluminum",
        "Alu",
        "Al"
    ],
    "Steel": [
        "Steel",
        "Stahl",
        "ST37",
        "C45"
    ],
    "Stainless": [
        "Stainless Steel",
        "Stainless",
        "Edelstahl",
        "1.4301",
        "1.4404"
    ],
    "Hardwood": [
        "Hardwood",
        "Hartholz",
        "Holz Hart",
        "HolzH",
        "Oak",
        "Beech"
    ],
    "Softwood": [
        "Softwood",
        "Weichholz",
        "Holz Weich",
        "HolzW",
        "Pine",
        "Spruce"
    ],
    "Plastic": [
        "Plastic",
        "Plastics",
        "Kunststoff",
        "Acryl",
        "Acrylic",
        "POM"
    ],
    "Brass": [
        "Brass",
        "Messing",
        "CuZn39"
    ],
    "Copper": [
        "Copper",
        "Kupfer",
        "Cu"
    ]
}

# Level 2: German → English Mapping
GERMAN_TO_ENGLISH = {
    # Operationen
    "Kontur": "FINISH_SLOT_OP",
    "Schlichten": "FINISH_SLOT_OP",
    "Schlicht": "FINISH_SLOT_OP",
    "Schruppen": "ROUGH_FACE_OP",
    "Planen": "ROUGH_FACE_OP",
    "Planen Grob": "ROUGH_FACE_OP",
    "Planen Fein": "FINISH_FACE_OP",
    "Teilschnitt": "PARTIAL_SLOT_OP",
    "Vollschnitt": "FULL_SLOT_OP",
    "Trochoidal": "TROCHOIDAL_SLOT_OP",
    "Adaptiv": "TROCHOIDAL_SLOT_OP",
    "Bohren": "DRILLING_OP",
    "Gravur": "VGROOVE_OP",
    "Fase": "CHAMFER_CONTOUR_OP",
    "Gewinde": "THREADING_OP",
    "Abrunden": "RADIUS_CONTOUR_OP",
    "Radius": "RADIUS_CONTOUR_OP",
    "Kugel": "BALL_3D_OP",
    "Tasche": "PARTIAL_SLOT_OP",
    "Schlicht(F)": "FINISH_SLOT_OP",
    "Schlicht(R)": "RADIUS_CONTOUR_OP",

    # Materialien
    "Aluminium": "Aluminium",
    "Alu": "Aluminium",
    "Stahl": "Steel",
    "Edelstahl": "Stainless",
    "Holz Hart": "Hardwood",
    "Hartholz": "Hardwood",
    "HolzH": "Hardwood",
    "Holz Weich": "Softwood",
    "Weichholz": "Softwood",
    "HolzW": "Softwood",
    "Kunststoff": "Plastic",
    "Acryl": "Plastic",
    "Messing": "Brass",
    "Kupfer": "Copper",
}


class PresetMatcher:
    """
    Intelligent preset matching with 3-level fallback strategy.

    Level 1: Exact matches (high confidence)
    Level 2: German → English mapping (high confidence)
    Level 3: Fuzzy matching (medium confidence)
    """

    def __init__(self):
        """Initialize preset matcher."""
        self.exact_op_matches = EXACT_OPERATION_MATCHES
        self.exact_mat_matches = EXACT_MATERIAL_MATCHES
        self.german_to_english = GERMAN_TO_ENGLISH

    def match_preset(
        self,
        preset_name: str,
        material_name: str = ""
    ) -> Tuple[Optional[str], Optional[str], str]:
        """
        Try to match preset and material names to our IDs.

        Args:
            preset_name: Original preset name from .tools file
            material_name: Original material name (optional, may be embedded in preset_name)

        Returns:
            (operation_id, material_id, confidence)
            confidence: "high" | "medium" | "low" | "none"
        """

        # Normalize names
        preset_clean = preset_name.strip()
        material_clean = material_name.strip() if material_name else ""

        # ═══════════════════════════════════════════════════════
        # LEVEL 1: Exact Matches
        # ═══════════════════════════════════════════════════════

        op_id = self._exact_match_operation(preset_clean)
        mat_id = self._exact_match_material(material_clean) if material_clean else None

        # Also try to extract material from preset name
        if not mat_id:
            mat_id = self._extract_material_from_preset(preset_clean)

        if op_id and mat_id:
            logger.info(f"Exact match: '{preset_name}' → {op_id} + {mat_id}")
            return (op_id, mat_id, "high")

        # ═══════════════════════════════════════════════════════
        # LEVEL 2: German → English Mapping
        # ═══════════════════════════════════════════════════════

        if not op_id:
            op_id = self.german_to_english.get(preset_clean)
            if op_id:
                logger.info(f"German match: '{preset_clean}' → {op_id}")

        if not mat_id and material_clean:
            mat_id = self.german_to_english.get(material_clean)
            if mat_id:
                logger.info(f"German match: '{material_clean}' → {mat_id}")

        if op_id and mat_id:
            return (op_id, mat_id, "high")

        # ═══════════════════════════════════════════════════════
        # LEVEL 3: Fuzzy Matching
        # ═══════════════════════════════════════════════════════

        if not op_id:
            op_id = self._fuzzy_match_operation(preset_clean)
            if op_id:
                logger.info(f"Fuzzy match: '{preset_clean}' → {op_id}")
                confidence = "medium"
            else:
                confidence = "none"
        else:
            confidence = "high"

        if not mat_id and material_clean:
            mat_id = self._fuzzy_match_material(material_clean)
            if mat_id:
                logger.info(f"Fuzzy match: '{material_clean}' → {mat_id}")
            if confidence != "none":
                confidence = "medium"

        if not op_id and not mat_id:
            logger.warning(f"No match found for: '{preset_name}' / '{material_name}'")
            confidence = "none"

        return (op_id, mat_id, confidence)

    def _exact_match_operation(self, name: str) -> Optional[str]:
        """Exact match for operation."""
        for op_id, names in self.exact_op_matches.items():
            if name in names:
                return op_id
        return None

    def _exact_match_material(self, name: str) -> Optional[str]:
        """Exact match for material."""
        for mat_id, names in self.exact_mat_matches.items():
            if name in names:
                return mat_id
        return None

    def _extract_material_from_preset(self, preset_name: str) -> Optional[str]:
        """Try to extract material from preset name (e.g., 'Aluminum - Face Rough')."""
        lower = preset_name.lower()

        # Check each material's aliases
        for mat_id, names in self.exact_mat_matches.items():
            for name in names:
                if name.lower() in lower:
                    return mat_id

        return None

    def _fuzzy_match_operation(self, name: str) -> Optional[str]:
        """Fuzzy match for operation."""
        all_names = []
        for op_id, names in self.exact_op_matches.items():
            all_names.extend([(n, op_id) for n in names])

        name_list = [n[0] for n in all_names]
        matches = get_close_matches(name, name_list, n=1, cutoff=0.6)

        if matches:
            # Find corresponding ID
            for n, op_id in all_names:
                if n == matches[0]:
                    return op_id

        return None

    def _fuzzy_match_material(self, name: str) -> Optional[str]:
        """Fuzzy match for material."""
        all_names = []
        for mat_id, names in self.exact_mat_matches.items():
            all_names.extend([(n, mat_id) for n in names])

        name_list = [n[0] for n in all_names]
        matches = get_close_matches(name, name_list, n=1, cutoff=0.6)

        if matches:
            for n, mat_id in all_names:
                if n == matches[0]:
                    return mat_id

        return None

    def analyze_imported_presets(self, tools: List) -> List[Dict]:
        """
        Analyze imported .tools file and create matching report.

        Args:
            tools: List of Tool objects with presets

        Returns:
            List of matching results with confidence levels
        """
        results = []

        for tool in tools:
            for preset in tool.presets:
                # Extract preset name and material
                preset_name = preset.name if hasattr(preset, 'name') else preset.description

                # Try to extract material from preset description or name
                material_name = ""
                if hasattr(preset, 'material'):
                    material_name = preset.material

                op_id, mat_id, confidence = self.match_preset(
                    preset_name,
                    material_name
                )

                results.append({
                    "tool": tool.description,
                    "tool_id": tool.tool_id,
                    "original_preset": preset_name,
                    "original_material": material_name,
                    "matched_operation": op_id,
                    "matched_material": mat_id,
                    "confidence": confidence
                })

        return results

    def get_statistics(self, results: List[Dict]) -> Dict:
        """
        Get statistics about matching results.

        Args:
            results: List of matching results

        Returns:
            Dictionary with counts by confidence level
        """
        stats = {
            "total": len(results),
            "high": sum(1 for r in results if r["confidence"] == "high"),
            "medium": sum(1 for r in results if r["confidence"] == "medium"),
            "low": sum(1 for r in results if r["confidence"] == "low"),
            "none": sum(1 for r in results if r["confidence"] == "none"),
        }

        return stats
