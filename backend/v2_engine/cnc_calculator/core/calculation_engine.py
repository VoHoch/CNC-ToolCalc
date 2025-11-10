"""Main calculation engine for CNC cutting data - REDESIGNED."""

import logging
import math
import json
from typing import Dict, Optional
from pathlib import Path
from ..models import Tool, Preset, ValidationResult, ValidationStatus
from .mrr_calculator import MRRCalculator
from .limit_manager import LimitManager
from .parameter_validator import ParameterValidator

logger = logging.getLogger(__name__)

# Load configurations
CONFIG_DIR = Path(__file__).parent.parent / "config"

with open(CONFIG_DIR / "materials.json", 'r', encoding='utf-8') as f:
    MATERIALS = json.load(f)

with open(CONFIG_DIR / "operations.json", 'r', encoding='utf-8') as f:
    OPERATIONS = json.load(f)


class CalculationEngine:
    """
    Main calculation engine implementing the MASTER ALGORITHM.

    Based on CNC_CALCULATION_SPECIFICATION_FINAL.md
    Implements all 12 operations with material-specific rules.
    """

    def __init__(self):
        """Initialize calculation engine."""
        self.materials = MATERIALS
        self.operations = OPERATIONS

        # Spindle limits
        self.rpm_min = 2000
        self.rpm_max = 24000

        # v2.0: Initialize validators
        self.mrr_calculator = MRRCalculator(materials=MATERIALS)
        self.limit_manager = LimitManager(config_dir=CONFIG_DIR)
        self.parameter_validator = ParameterValidator(
            materials=MATERIALS,
            mrr_calculator=self.mrr_calculator,
            limit_manager=self.limit_manager,
            spindle_power_kw=6.0
        )

        logger.info("Calculation engine initialized with 12 operations, 8 materials, and v2.0 validators")

    def calculate_preset(
        self,
        tool: Tool,
        material_id: str,
        operation_id: str,
        pitch: Optional[float] = None  # For threading
    ) -> Preset:
        """
        MASTER CALCULATION ALGORITHM

        All corrections are applied systematically as per specification.

        Args:
            tool: Tool object
            material_id: Material ID (e.g., "Aluminium")
            operation_id: Operation ID (e.g., "FINISH_SLOT_OP")
            pitch: Thread pitch in mm (only for THREADING_OP)

        Returns:
            Preset with all calculated parameters
        """

        material = self.materials[material_id]
        operation = self.operations[operation_id]

        # Tool geometry
        DC = tool.geometry.DC
        NOF = tool.geometry.NOF
        LCF = tool.geometry.LCF
        L_D_ratio = LCF / DC

        logger.debug(f"Calculating: {tool.tool_id} - {material_id} - {operation_id}")

        # ═══════════════════════════════════════════════════════
        # STEP 1: Calculate cutting speed (vc)
        # ═══════════════════════════════════════════════════════

        vc = material["vc_base"]

        # Operation factor
        vc *= operation.get("vc_factor", 1.0)

        # Dry machining (always active)
        vc *= material["dry_machining_factor"]

        # L/D correction
        if L_D_ratio > 3.0:
            lcd_vc_factor = 1.0 - ((L_D_ratio - 3.0) * 0.05)  # -5% per unit
            vc *= max(lcd_vc_factor, 0.7)  # Minimum 70%

        # Threading: Material-specific vc adjustment
        if operation_id == "THREADING_OP":
            vc *= operation["material_vc_factors"].get(material_id, 1.0)

        # CR-001: Finish operations - apply material-specific vc_finish_factor
        if operation_id in ["FINISH_SLOT_OP", "FINISH_FACE_OP"]:
            vc_finish_factor = material.get("vc_finish_factor", 1.0)
            vc *= vc_finish_factor
            logger.debug(f"Finish operation: Applied vc_finish_factor={vc_finish_factor:.2f}")

        # ═══════════════════════════════════════════════════════
        # STEP 2: Calculate RPM
        # ═══════════════════════════════════════════════════════

        n = (vc * 1000) / (math.pi * DC)

        # Ball-end boost
        if operation_id == "BALL_3D_OP":
            n *= operation.get("n_boost", 1.15)

        # Clamp to spindle limits
        n = self._clamp(n, self.rpm_min, self.rpm_max)

        # ═══════════════════════════════════════════════════════
        # STEP 3: Calculate feed per tooth (fz)
        # ═══════════════════════════════════════════════════════

        # Special operations have own fz logic
        if operation_id == "DRILLING_OP":
            fz = operation["material_fz"].get(material_id, 0.08)

        else:
            # Standard: Diameter scaling
            fz = material["fz_base"] * (DC / 6.0) ** material["diameter_exponent"]

            # Operation factor
            fz *= operation.get("fz_factor", 1.0)

            # Dry machining
            fz *= material["dry_machining_factor"]

            # L/D correction
            if L_D_ratio > 3.0:
                lcd_fz_factor = self._get_lcd_fz_correction(L_D_ratio)
                fz *= lcd_fz_factor

            # CR-001: Finish operations - apply material-specific fz_finish_factor
            if operation_id in ["FINISH_SLOT_OP", "FINISH_FACE_OP"]:
                fz_finish_factor = material.get("fz_finish_factor", 1.0)
                fz *= fz_finish_factor
                logger.debug(f"Finish operation: Applied fz_finish_factor={fz_finish_factor:.2f}")

        # ═══════════════════════════════════════════════════════
        # STEP 4: Calculate engagement (ae)
        # ═══════════════════════════════════════════════════════

        if "ae_d_ratio" in operation:
            ae = DC * operation["ae_d_ratio"]
        else:
            ae = DC * 0.5  # Default

        # ═══════════════════════════════════════════════════════
        # STEP 5: Calculate depth of cut (ap) - v2.0 CRITICAL FIX!
        # ═══════════════════════════════════════════════════════
        # REGEL: FACE = FEST, SLOT = LCF, GEOMETRY = GEOMETRISCH LIMITIERT
        #
        # GRUPPE 1: FACE OPERATIONS (ap FEST!)
        # GRUPPE 2: PERIPHERAL OPERATIONS (ap von LCF abhängig!)
        # GRUPPE 3: GEOMETRY-DEPENDENT (ap geometrisch limitiert!)
        # GRUPPE 4: SPECIAL OPERATIONS (eigene Formeln)
        # ═══════════════════════════════════════════════════════

        # GRUPPE 1: FACE OPERATIONS (ap FEST!)
        if operation_id == "ROUGH_FACE_OP":
            # Feste Werte pro Material (unabhängig von LCF!)
            AP_FACE_ROUGH = {
                "Aluminium": 1.0,
                "Steel": 0.8,
                "Stainless": 0.8,
                "Hardwood": 1.5,
                "Softwood": 1.5,
                "Plastic": 1.0,
                "Brass": 1.0,
                "Copper": 1.0
            }
            ap = AP_FACE_ROUGH.get(material_id, 1.0)

        elif operation_id == "FINISH_FACE_OP":
            ap = 0.2  # IMMER 0.2mm (unabhängig von Material!)

        # GRUPPE 2: PERIPHERAL OPERATIONS (ap von LCF abhängig!)
        elif operation_id == "FINISH_SLOT_OP":
            ap = 0.2  # Fixed for finishing

        elif operation_id in ["PARTIAL_SLOT_OP", "FULL_SLOT_OP", "TROCHOIDAL_SLOT_OP"]:
            if material_id in ["Hardwood", "Softwood"]:
                # Holz: Basierend auf DC (nicht LCF!)
                base_ap = DC * 1.5
            else:
                # Metall: Basierend auf LCF
                base_ap = LCF * material["ap_max_factor"]

            # Operation-spezifisch
            if operation_id == "FULL_SLOT_OP":
                ap = base_ap * 0.6
            elif operation_id == "TROCHOIDAL_SLOT_OP":
                ap = base_ap * 1.2
            else:
                ap = base_ap

            # Material-Minimum (nur für Metall! - KRITISCH für Steel/Stainless!)
            if material_id in ["Steel", "Stainless"] and "ap_min" in material:
                ap = max(ap, material["ap_min"])

        # GRUPPE 3: GEOMETRY-DEPENDENT (geometrisch limitiert!)
        elif operation_id == "BALL_3D_OP":
            # KRITISCH: Nie mehr als Radius! Sonst schneidet der Schaft!
            radius = DC / 2
            ap = min(0.5, radius)

        elif operation_id == "RADIUS_CONTOUR_OP":
            # KRITISCH: Max 2× Radius!
            if hasattr(tool.geometry, 'corner_radius') and tool.geometry.corner_radius:
                radius = tool.geometry.corner_radius
                ap = min(0.2, 2 * radius)
            else:
                ap = 0.2

        elif operation_id in ["VGROOVE_OP", "CHAMFER_CONTOUR_OP"]:
            # KRITISCH: Geometrisch limitiert durch Winkel!
            if hasattr(tool.geometry, 'angle') and tool.geometry.angle:
                angle = tool.geometry.angle
                max_depth = DC / (2 * math.tan(math.radians(angle / 2)))
                ap = min(0.3, max_depth)
            else:
                ap = 0.3

        # GRUPPE 4: SPECIAL OPERATIONS (eigene Formeln)
        elif operation_id == "DRILLING_OP":
            ap = LCF  # Kann volle Länge nutzen

        elif operation_id == "THREADING_OP":
            # Wird aus pitch berechnet
            ap = 1.0  # Placeholder

        else:
            # Fallback für unbekannte Operationen
            ap = 0.5
            logger.warning(f"Unknown operation {operation_id} - using fallback ap=0.5mm")

        # FINALE LIMITS: Niemals mehr als LCF!
        ap = min(ap, LCF)

        # Absolute minimum (safety)
        ap = max(ap, 0.1)

        # ═══════════════════════════════════════════════════════
        # STEP 6: Calculate feed rate (vf)
        # ═══════════════════════════════════════════════════════

        if operation_id == "DRILLING_OP":
            vf = fz * n  # WITHOUT NOF!

        elif operation_id == "THREADING_OP":
            if pitch is None:
                # Use default for M6 if not specified
                pitch = operation["pitch_by_thread"].get("M6", 1.0)
            vf = pitch * n  # Exact pitch!

        else:
            vf = fz * NOF * n  # Standard

        # ═══════════════════════════════════════════════════════
        # STEP 7: Calculate chip thickness (for validation)
        # ═══════════════════════════════════════════════════════

        if operation_id not in ["DRILLING_OP", "THREADING_OP"]:
            hm = fz * math.sqrt(ae / DC)
        else:
            hm = fz  # Simplified

        # ═══════════════════════════════════════════════════════
        # STEP 8: Get ramp angle
        # ═══════════════════════════════════════════════════════

        ramp_angle = material["ramp_angle"]

        # Diameter adjustment
        if DC > 8:
            ramp_angle *= 0.8
        elif DC > 12:
            ramp_angle *= 0.6

        # Full slot adjustment
        if operation_id == "FULL_SLOT_OP":
            ramp_angle *= 0.5  # CRITICAL!

        # ═══════════════════════════════════════════════════════
        # STEP 9: Calculate feed factors with ALL corrections
        # ═══════════════════════════════════════════════════════

        base_factors = operation["feed_factors"].copy()

        # Material correction
        if material_id == "Steel":
            base_factors['plunge'] *= 0.6
            base_factors['ramp'] *= 0.5
            base_factors['entry'] *= 0.7
        elif material_id == "Stainless":
            base_factors['plunge'] *= 0.5
            base_factors['ramp'] *= 0.4
            base_factors['entry'] *= 0.6

        # L/D correction
        if L_D_ratio > 3.0:
            lcd_factor = 1.0 - ((L_D_ratio - 3.0) * 0.1)
            base_factors['plunge'] *= max(lcd_factor, 0.7)
            base_factors['ramp'] *= max(lcd_factor, 0.7)

        # Dry machining correction
        base_factors['plunge'] *= 0.85
        base_factors['ramp'] *= 0.85

        # ═══════════════════════════════════════════════════════
        # STEP 10: Build expressions for Fusion 360
        # ═══════════════════════════════════════════════════════

        # CRITICAL FIX: Proper expressions for Fusion 360
        # - NO circular references
        # - Numeric values with units, not references
        # - Factors shown as "0.800 * tool_feedCutting" (factor first!)

        # CRITICAL FIX: Expressions must be FORMULAS not direct values!
        # Based on Fusion 360 screenshot feedback:
        # - Schnittgeschwindigkeit, Rampen-Drehzahl, Vorschub pro Zahn → parametrisch ✓
        # - Einfahrvorschub, Ausfahrvorschub, Übergangsvorschub, Helixvorschub → parametrisch (fehlte!)
        # - Tiefenzustellung, Querzustellung → parametrisch ✓

        # Calculate percentages based on current values
        ap_percent = (ap / tool.geometry.LCF) if tool.geometry.LCF > 0 else 0.06
        ae_percent = (ae / tool.geometry.DC) if tool.geometry.DC > 0 else 0.5

        expressions = {
            # Base cutting parameters
            "tool_surfaceSpeed": f"{vc:.1f} m/min",
            "tool_feedPerTooth": f"{fz:.4f} mm",
            "tool_rampSpindleSpeed": f"{n:.0f} rpm",
            "tool_rampAngle": f"{ramp_angle:.1f} deg",

            # Feed cutting - base value
            "tool_feedCutting": f"{vf:.0f} mm/min",

            # Feed factors as formulas (multiplication with tool_feedCutting)
            "tool_feedEntry": f"{base_factors['entry']:.3f} * tool_feedCutting",
            "tool_feedExit": f"{base_factors['exit']:.3f} * tool_feedCutting",
            "tool_feedPlunge": f"{base_factors['plunge']:.3f} * tool_feedCutting",
            "tool_feedRamp": f"{base_factors['ramp']:.3f} * tool_feedCutting",
            "tool_feedTransition": f"{base_factors['transition']:.3f} * tool_feedCutting",

            # Tool geometry based formulas
            "tool_stepdown": f"{ap_percent:.3f} * tool_fluteLength",
            "tool_stepover": f"{ae_percent:.3f} * tool_diameter",
        }

        # FULL VERSION (commented out for testing):
        # expressions = {
        #     # Base values (direct numbers with units)
        #     "tool_surfaceSpeed": f"{vc:.1f} m/min",
        #     "tool_feedPerTooth": f"{fz:.4f} mm",
        #     "tool_rampSpindleSpeed": f"{n:.0f} rpm",  # Rampen-Drehzahl als Parameter
        #     "tool_rampAngle": f"{ramp_angle:.1f} deg",
        #
        #     # Feed rate - direct value, no formula
        #     "tool_feedCutting": f"{vf:.0f} mm/min",
        #
        #     # Feed factors - show factor first, then multiply by feedCutting
        #     "tool_feedEntry": f"{base_factors['entry']:.3f} * tool_feedCutting",
        #     "tool_feedExit": f"{base_factors['exit']:.3f} * tool_feedCutting",
        #     "tool_feedPlunge": f"{base_factors['plunge']:.3f} * tool_feedCutting",
        #     "tool_feedRamp": f"{base_factors['ramp']:.3f} * tool_feedCutting",
        #     "tool_feedTransition": f"{base_factors['transition']:.3f} * tool_feedCutting",
        #
        #     # Depths - ONLY expressions, NOT flags (flags are top-level in preset dict)
        #     "tool_stepdown": f"{ap:.2f} mm",
        #     "tool_stepover": f"{ae:.2f} mm",
        # }

        # ═══════════════════════════════════════════════════════
        # STEP 11: Build preset object
        # ═══════════════════════════════════════════════════════

        # CRITICAL: Intelligente Namenskonvention (siehe ARCHITECTURE.md Abschnitt 3)
        # Format: "{Material-Kurzform} - {Bearbeitungsart}{Suffix}"
        preset_name = self._generate_preset_name(material_id, operation_id, operation)

        preset = Preset(
            name=preset_name,
            material=material_id,  # FIXED: Add material
            operation=operation_id,  # FIXED: Add operation
            comment=f"{material['display_name']} - {operation['display_name']}",  # FIXED: Use comment not description
            vc_base=material["vc_base"],
            vc_final=vc,
            fz_base=material["fz_base"],
            fz_final=fz,
            n_rpm=n,
            vf_mm_per_min=vf,
            ae_mm=ae,
            ap_mm=ap,
            feed_entry=base_factors['entry'],
            feed_exit=base_factors['exit'],
            feed_plunge=base_factors['plunge'],
            feed_ramp=base_factors['ramp'],
            coolant="disabled",
            expressions=expressions
        )

        # v2.0: Perform multi-level validation
        validation = self.parameter_validator.validate(
            tool=tool,
            material_id=material_id,
            operation_id=operation_id,
            ae_mm=ae,
            ap_mm=ap,
            vf_mm_per_min=vf,
            rpm=n,
            vc_m_per_min=vc,
            fz_mm=fz
        )
        preset.validation_result = validation

        logger.debug(
            f"Result: vc={vc:.1f}, n={n:.0f}, fz={fz:.4f}, vf={vf:.0f}, "
            f"ae={ae:.2f}, ap={ap:.2f}, hm={hm:.4f} | "
            f"Validation: {validation.get_icon()} {validation.status.value}"
        )

        if not validation.is_safe():
            logger.warning(f"Preset validation failed: {validation.get_summary()}")
            for error in validation.errors:
                logger.warning(f"  ERROR: {error}")

        return preset

    def _generate_preset_name(self, material_id: str, operation_id: str, operation: dict) -> str:
        """
        Generate Fusion 360 compatible preset name - v2.0 Format.

        Format: "{MaterialAbbr}_{Category}_{Variant}"
        Example: "Alu_Face_Rough"

        See ARCHITECTURE.md Section 3 for details.

        Args:
            material_id: Material ID (e.g., "Aluminium")
            operation_id: Operation ID (e.g., "ROUGH_FACE_OP")
            operation: Operation config dict

        Returns:
            Formatted preset name (e.g., "Alu_Face_Rough")
        """
        # Get material abbreviation from config (max 5 chars)
        material_abbr = self.materials[material_id].get("abbreviation", material_id[:5])

        # Map operation ID to name
        OPERATION_NAMES = {
            "ROUGH_FACE_OP": "Face_Rough",
            "FINISH_FACE_OP": "Face_Finish",
            "PARTIAL_SLOT_OP": "Slot_Partial",
            "FULL_SLOT_OP": "Slot_Full",
            "TROCHOIDAL_SLOT_OP": "Slot_Trochoidal",
            "FINISH_SLOT_OP": "Slot_Finish",
            "RADIUS_CONTOUR_OP": "Contour_Radius",
            "CHAMFER_CONTOUR_OP": "Contour_Chamfer",
            "BALL_3D_OP": "3D_Ball",
            "DRILLING_OP": "Drill",
            "VGROOVE_OP": "Engrave",
            "THREADING_OP": "Thread"
        }

        operation_name = OPERATION_NAMES.get(operation_id, operation.get("display_name_short", "Unknown"))

        # Build name: Material_Operation
        preset_name = f"{material_abbr}_{operation_name}"

        return preset_name

    def _clamp(self, value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max."""
        return max(min_val, min(value, max_val))

    def _get_lcd_fz_correction(self, lcd_ratio: float) -> float:
        """L/D ratio correction for feed per tooth."""
        if lcd_ratio <= 3.0:
            return 1.0
        elif lcd_ratio <= 4.0:
            return 0.9
        elif lcd_ratio <= 5.0:
            return 0.8
        else:  # > 5.0
            return 0.7

    def validate_preset(
        self,
        preset: Preset,
        tool: Tool,
        material_id: str,
        operation_id: str
    ) -> ValidationResult:
        """
        Validate calculated preset with multi-level checks.

        Args:
            preset: Calculated preset
            tool: Tool object
            material_id: Material ID
            operation_id: Operation ID

        Returns:
            ValidationResult with status and messages
        """

        material = self.materials[material_id]
        operation = self.operations[operation_id]

        errors = []
        warnings = []
        recommendations = []

        # ═══════════════════════════════════════════════════════
        # CHECK 1: RPM Limits
        # ═══════════════════════════════════════════════════════

        if preset.n_rpm < self.rpm_min:
            warnings.append(f"RPM {preset.n_rpm:.0f} below minimum {self.rpm_min}")

        if preset.n_rpm > self.rpm_max:
            errors.append(f"RPM {preset.n_rpm:.0f} exceeds spindle maximum {self.rpm_max}!")

        # ═══════════════════════════════════════════════════════
        # CHECK 2: Chip Thickness (CRITICAL for Steel/Stainless)
        # ═══════════════════════════════════════════════════════

        if material_id in ["Steel", "Stainless"]:
            hm_min = material["hm_min"]

            # Calculate actual hm
            if operation_id not in ["DRILLING_OP", "THREADING_OP"]:
                ae_d_ratio = preset.ae_mm / tool.geometry.DC
                hm = preset.fz_final * math.sqrt(ae_d_ratio)
            else:
                hm = preset.fz_final

            if hm < hm_min:
                errors.append(
                    f"⚠️ CRITICAL: Chip thickness {hm:.3f}mm below minimum {hm_min}mm!\n"
                    f"Risk: {'Work-hardening (Stainless)' if material_id == 'Stainless' else 'Silver chips (Steel)'}\n"
                    f"→ MUST increase feed per tooth!"
                )

                # Calculate required fz
                fz_required = hm_min / math.sqrt(ae_d_ratio) if operation_id not in ["DRILLING_OP", "THREADING_OP"] else hm_min
                recommendations.append(f"Increase fz to at least {fz_required:.3f}mm")

        # ═══════════════════════════════════════════════════════
        # CHECK 3: Depth of Cut
        # ═══════════════════════════════════════════════════════

        if preset.ap_mm > tool.geometry.LCF:
            errors.append(f"ap {preset.ap_mm:.1f}mm exceeds cutting length {tool.geometry.LCF}mm!")

        # Material-specific ap checks
        if material_id == "Steel" and preset.ap_mm < 1.5:
            warnings.append(
                "ap < 1.5mm for steel - risk of insufficient chip thickness!"
            )

        if material_id == "Stainless" and preset.ap_mm < 2.0:
            errors.append(
                "⚠️ CRITICAL: ap < 2.0mm for stainless steel!\n"
                "Risk of catastrophic work-hardening!\n"
                "Material will become impossible to cut!"
            )

        # ═══════════════════════════════════════════════════════
        # CHECK 4: L/D Ratio
        # ═══════════════════════════════════════════════════════

        lcd = tool.calculate_ld_ratio()

        if lcd > 4.0:
            warnings.append(f"L/D ratio {lcd:.1f} > 4.0 - risk of vibration/deflection")

        if lcd > 6.0:
            errors.append(f"L/D ratio {lcd:.1f} > 6.0 - CRITICAL deflection risk!")

        # ═══════════════════════════════════════════════════════
        # CHECK 5: Feed Rate Sanity
        # ═══════════════════════════════════════════════════════

        if preset.vf_mm_per_min < 100:
            warnings.append("Feed rate very low - inefficient")

        if preset.vf_mm_per_min > 5000:
            warnings.append("Feed rate very high - check calculation")

        # ═══════════════════════════════════════════════════════
        # CHECK 6: Full Slot Warnings
        # ═══════════════════════════════════════════════════════

        if operation_id == "FULL_SLOT_OP":
            warnings.append(
                "⚠️ Full slotting operation - maximum chip load!\n"
                "- Tool breakage risk if parameters too aggressive\n"
                "- Consider trochoidal milling instead"
            )

        # ═══════════════════════════════════════════════════════
        # CHECK 7: Threading Pitch Validation
        # ═══════════════════════════════════════════════════════

        if operation_id == "THREADING_OP":
            # vf MUST be exactly pitch × n
            expected_vf = (preset.vf_mm_per_min / preset.n_rpm)  # back-calculate pitch
            # We can't validate without knowing original pitch, so just note it
            recommendations.append(
                f"Threading: Verify pitch is correct (vf/n = {expected_vf:.3f}mm)"
            )

        # ═══════════════════════════════════════════════════════
        # BUILD RESULT
        # ═══════════════════════════════════════════════════════

        if errors:
            status = ValidationStatus.RED
        elif warnings:
            status = ValidationStatus.YELLOW
        else:
            status = ValidationStatus.GREEN

        return ValidationResult(
            status=status,
            errors=errors,
            warnings=warnings,
            recommendations=recommendations,
            sorotec_ref_vc=None,  # TODO: Add Sorotec validation
            sorotec_ref_fz=None,
            vc_delta_pct=0.0,
            fz_delta_pct=0.0
        )
