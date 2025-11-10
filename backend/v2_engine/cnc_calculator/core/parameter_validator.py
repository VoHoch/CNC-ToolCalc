"""Parameter Validator - v2.0 Multi-Level Validation System."""

import logging
from typing import Dict, Optional
from ..models.validation_result import ValidationResult
from ..models.enums import ValidationStatus
from ..models.tool import Tool
from .mrr_calculator import MRRCalculator
from .limit_manager import LimitManager

logger = logging.getLogger(__name__)


class ParameterValidator:
    """Multi-level parameter validation with Red/Yellow/Green status system.

    Based on MASTER_SPECIFICATION v2.0 Section 6.

    Validation Levels:
    1. ae (Radial Depth) - Check against min/max/recommended
    2. ap (Axial Depth) - Check against min/max and material-specific limits
    3. MRR (Material Removal Rate) - Check against spindle capacity
    4. Power - Check against 6kW spindle limit
    5. Geometry - Check tool-specific constraints (L/D, Ball-End radius, etc.)

    Status System:
    - 🟢 GREEN: All checks passed, optimal parameters
    - 🟡 YELLOW: Within limits but with warnings (near limits, not optimal)
    - 🔴 RED: Outside safe limits, UNSAFE to use
    """

    def __init__(
        self,
        materials: Dict,
        mrr_calculator: MRRCalculator,
        limit_manager: LimitManager,
        spindle_power_kw: float = 6.0
    ):
        """Initialize validator.

        Args:
            materials: Material configuration dict
            mrr_calculator: MRR and Power calculator instance
            limit_manager: Limit manager instance
            spindle_power_kw: Available spindle power [kW], default 6.0
        """
        self.materials = materials
        self.mrr_calculator = mrr_calculator
        self.limit_manager = limit_manager
        self.spindle_power_kw = spindle_power_kw
        logger.debug("ParameterValidator initialized")

    def validate(
        self,
        tool: Tool,
        material_id: str,
        operation_id: str,
        ae_mm: float,
        ap_mm: float,
        vf_mm_per_min: float,
        rpm: float,
        vc_m_per_min: float,
        fz_mm: float
    ) -> ValidationResult:
        """Perform complete multi-level validation.

        Args:
            tool: Tool object with geometry
            material_id: Material ID
            operation_id: Operation ID
            ae_mm: Radial depth of cut [mm]
            ap_mm: Axial depth of cut [mm]
            vf_mm_per_min: Feed rate [mm/min]
            rpm: Spindle speed [rpm]
            vc_m_per_min: Cutting speed [m/min]
            fz_mm: Feed per tooth [mm/tooth]

        Returns:
            ValidationResult with status, errors, warnings, recommendations
        """
        result = ValidationResult()

        # Calculate L/D ratio for limit adjustments
        DC = tool.geometry.DC
        LCF = tool.geometry.LCF
        ld_ratio = LCF / DC
        result.ld_ratio = ld_ratio

        # Get limits (with L/D adjustment if needed)
        tool_type = self._get_tool_type(tool)
        limits = self.limit_manager.get_limits_with_ld_adjustment(
            material_id, tool_type, operation_id, ld_ratio
        )

        if limits is None:
            # Use defaults
            limits = self.limit_manager.get_default_limits(operation_id)
            result.warnings.append(
                f"No specific limits for {material_id}/{tool_type}/{operation_id}, "
                f"using defaults"
            )

        result.limits_applied = limits

        # Perform 5-level validation
        self._validate_ae(ae_mm, DC, limits, result)
        self._validate_ap(ap_mm, DC, LCF, material_id, operation_id, limits, result)
        self._validate_geometry(tool, operation_id, ae_mm, ap_mm, result)

        # MRR & Power validation (calculates and checks)
        self._validate_mrr_and_power(
            ae_mm, ap_mm, vf_mm_per_min, material_id, limits, result
        )

        # Determine final status
        if result.errors:
            result.status = ValidationStatus.RED
            logger.warning(f"Validation FAILED: {len(result.errors)} error(s)")
        elif result.warnings:
            result.status = ValidationStatus.YELLOW
            logger.info(f"Validation OK with warnings: {len(result.warnings)}")
        else:
            result.status = ValidationStatus.GREEN
            logger.debug("Validation PASSED: All parameters optimal")

        return result

    def _get_tool_type(self, tool: Tool) -> str:
        """Determine tool type from tool object.

        Args:
            tool: Tool object

        Returns:
            Tool type string (e.g., "end_mill", "ball_end_mill")
        """
        # Simple heuristic based on tool description or geometry
        description = tool.description.lower() if tool.description else ""

        if "ball" in description:
            return "ball_end_mill"
        elif "drill" in description:
            return "drill"
        elif "thread" in description:
            return "thread_mill"
        else:
            return "end_mill"

    def _validate_ae(
        self,
        ae_mm: float,
        DC: float,
        limits: Dict,
        result: ValidationResult
    ):
        """Validate radial depth of cut (ae).

        Checks:
        - ae_min: Minimum engagement for effective cutting
        - ae_max: Maximum based on DC and operation
        - ae_recommended: Optimal value

        Args:
            ae_mm: Radial depth [mm]
            DC: Cutting diameter [mm]
            limits: Operation limits dict
            result: ValidationResult to update
        """
        # Get limits as absolute values
        ae_min = limits.get("ae_factor_min", 0.05) * DC
        ae_max = limits.get("ae_factor_max", 0.5) * DC
        ae_recommended = limits.get("ae_recommended", limits.get("ae_factor_max", 0.35)) * DC

        # Check minimum
        if ae_mm < ae_min:
            result.errors.append(
                f"❌ ae={ae_mm:.2f}mm too small! Minimum: {ae_min:.2f}mm "
                f"(rubbing risk)"
            )
            return

        # Check maximum
        if ae_mm > ae_max:
            result.errors.append(
                f"❌ ae={ae_mm:.2f}mm exceeds maximum {ae_max:.2f}mm! "
                f"Reduce to ≤{ae_max:.2f}mm"
            )
            return

        # Check if not optimal
        if ae_mm < ae_recommended * 0.7:
            result.warnings.append(
                f"⚠️ ae={ae_mm:.2f}mm below recommended {ae_recommended:.2f}mm "
                f"(not optimal)"
            )
        elif ae_mm > ae_max * 0.9:
            result.warnings.append(
                f"⚠️ ae={ae_mm:.2f}mm near maximum {ae_max:.2f}mm "
                f"(high load)"
            )

        logger.debug(
            f"ae validation: {ae_mm:.2f}mm in range [{ae_min:.2f}, {ae_max:.2f}]mm"
        )

    def _validate_ap(
        self,
        ap_mm: float,
        DC: float,
        LCF: float,
        material_id: str,
        operation_id: str,
        limits: Dict,
        result: ValidationResult
    ):
        """Validate axial depth of cut (ap).

        Checks:
        - ap_fixed: Fixed value for Face operations
        - ap_min_fixed: Material minimum (Steel 1.5mm, Stainless 2.0mm)
        - ap_max: Maximum based on LCF or formula
        - Material-specific constraints

        Args:
            ap_mm: Axial depth [mm]
            DC: Cutting diameter [mm]
            LCF: Length of cut [mm]
            material_id: Material ID
            operation_id: Operation ID
            limits: Operation limits dict
            result: ValidationResult to update
        """
        # Check fixed ap (Face operations)
        if "ap_fixed" in limits:
            ap_expected = limits["ap_fixed"]
            if abs(ap_mm - ap_expected) > 0.05:  # 0.05mm tolerance
                result.warnings.append(
                    f"⚠️ ap={ap_mm:.2f}mm differs from standard {ap_expected:.2f}mm "
                    f"for this operation"
                )
            logger.debug(f"ap validation: Fixed value {ap_expected}mm")
            return

        # Check material minimum (CRITICAL for Steel/Stainless!)
        material = self.materials.get(material_id, {})
        material_ap_min = material.get("ap_min", 0.0)

        # Also check operation-specific minimum
        operation_ap_min = limits.get("ap_min_fixed", 0.0)
        ap_min = max(material_ap_min, operation_ap_min)

        if ap_mm < ap_min:
            result.errors.append(
                f"❌ ap={ap_mm:.2f}mm below minimum {ap_min:.2f}mm! "
                f"({material_id} requires ap≥{ap_min}mm to prevent work-hardening)"
            )
            return

        # Check maximum
        if "ap_factor_max" in limits:
            ap_max = limits["ap_factor_max"] * LCF
            if ap_mm > ap_max:
                result.errors.append(
                    f"❌ ap={ap_mm:.2f}mm exceeds maximum {ap_max:.2f}mm! "
                    f"Reduce to ≤{ap_max:.2f}mm"
                )
                return

            # Warning if close to limit
            if ap_mm > ap_max * 0.9:
                result.warnings.append(
                    f"⚠️ ap={ap_mm:.2f}mm near maximum {ap_max:.2f}mm (high load)"
                )

        logger.debug(f"ap validation: {ap_mm:.2f}mm, min={ap_min:.2f}mm")

    def _validate_geometry(
        self,
        tool: Tool,
        operation_id: str,
        ae_mm: float,
        ap_mm: float,
        result: ValidationResult
    ):
        """Validate geometry-specific constraints.

        Checks:
        - Ball-End: ap ≤ radius
        - Radius Mill: ap ≤ 2 × corner_radius
        - V-Tools: depth within angle limits
        - L/D ratio warnings

        Args:
            tool: Tool object
            operation_id: Operation ID
            ae_mm: Radial depth [mm]
            ap_mm: Axial depth [mm]
            result: ValidationResult to update
        """
        DC = tool.geometry.DC
        LCF = tool.geometry.LCF
        ld_ratio = LCF / DC

        # L/D ratio warnings
        if ld_ratio > 5.0:
            result.warnings.append(
                f"⚠️ L/D={ld_ratio:.1f} > 5.0! High deflection risk, "
                f"limits reduced by 30%"
            )
        elif ld_ratio > 4.0:
            result.warnings.append(
                f"⚠️ L/D={ld_ratio:.1f} > 4.0! Deflection risk, limits reduced by 20%"
            )
        elif ld_ratio > 3.0:
            result.warnings.append(
                f"⚠️ L/D={ld_ratio:.1f} > 3.0! Limits reduced by 10%"
            )

        # Ball-End specific checks
        if operation_id == "BALL_3D_OP":
            radius = DC / 2
            if ap_mm > radius:
                result.errors.append(
                    f"❌ Ball-End: ap={ap_mm:.2f}mm exceeds radius {radius:.2f}mm! "
                    f"Reduce to ≤{radius:.2f}mm"
                )

        # Radius Mill checks
        if operation_id == "RADIUS_CONTOUR_OP":
            if hasattr(tool.geometry, 'corner_radius') and tool.geometry.corner_radius:
                corner_radius = tool.geometry.corner_radius
                max_ap = 2 * corner_radius
                if ap_mm > max_ap:
                    result.errors.append(
                        f"❌ Radius Mill: ap={ap_mm:.2f}mm exceeds 2×radius "
                        f"{max_ap:.2f}mm! Reduce to ≤{max_ap:.2f}mm"
                    )

        # V-Tool / Chamfer checks
        if operation_id in ["VGROOVE_OP", "CHAMFER_CONTOUR_OP"]:
            if hasattr(tool.geometry, 'angle') and tool.geometry.angle:
                angle = tool.geometry.angle
                # Simple depth check (full validation requires workpiece width)
                if ap_mm > DC * 0.4:
                    result.warnings.append(
                        f"⚠️ V-Tool: ap={ap_mm:.2f}mm may be too deep for angle "
                        f"{angle}° - verify against workpiece geometry"
                    )

        logger.debug(f"Geometry validation: L/D={ld_ratio:.1f}, operation={operation_id}")

    def _validate_mrr_and_power(
        self,
        ae_mm: float,
        ap_mm: float,
        vf_mm_per_min: float,
        material_id: str,
        limits: Dict,
        result: ValidationResult
    ):
        """Validate Material Removal Rate and spindle power.

        Checks:
        - MRR against operation-specific limit
        - Power against spindle capacity (6kW)
        - Provides safe vf if limits exceeded

        Args:
            ae_mm: Radial depth [mm]
            ap_mm: Axial depth [mm]
            vf_mm_per_min: Feed rate [mm/min]
            material_id: Material ID
            limits: Operation limits dict
            result: ValidationResult to update
        """
        # Calculate MRR and Power
        mrr = self.mrr_calculator.calculate_mrr(ae_mm, ap_mm, vf_mm_per_min)
        power = self.mrr_calculator.calculate_power(mrr, material_id)

        result.mrr_calculated = mrr
        result.power_calculated = power

        # Get MRR limit
        mrr_max = limits.get("mrr_max", 500)

        # Check MRR limit
        if mrr > mrr_max:
            vf_max_safe = (mrr_max * 1000) / (ae_mm * ap_mm)
            result.errors.append(
                f"❌ MRR {mrr:.0f} cm³/min exceeds limit {mrr_max} cm³/min! "
                f"Reduce vf to max {vf_max_safe:.0f} mm/min"
            )
            return

        # Check Power limit
        if power > self.spindle_power_kw:
            result.errors.append(
                f"❌ Power {power:.1f}kW exceeds spindle {self.spindle_power_kw}kW! "
                f"Reduce MRR (lower vf or ap)!"
            )
            return

        # Warnings if close to limits
        if mrr > mrr_max * 0.9:
            result.warnings.append(
                f"⚠️ MRR {mrr:.0f} cm³/min near limit {mrr_max} cm³/min"
            )

        if power > self.spindle_power_kw * 0.8:
            result.warnings.append(
                f"⚠️ Power {power:.1f}kW near spindle limit {self.spindle_power_kw}kW"
            )

        # Recommendation if MRR very low (inefficient)
        if mrr < mrr_max * 0.3:
            result.recommendations.append(
                f"💡 MRR {mrr:.0f} cm³/min is only {(mrr/mrr_max)*100:.0f}% of "
                f"maximum {mrr_max} cm³/min - consider increasing vf for efficiency"
            )

        logger.debug(
            f"MRR/Power validation: MRR={mrr:.0f}/{mrr_max} cm³/min, "
            f"Power={power:.1f}/{self.spindle_power_kw} kW"
        )
