"""
CNC-ToolCalc Backend - Validation Service
Version: 0.0.1-alpha
Implementation: 8-Checks Validation System from V4 Architecture
"""

from backend.models.schemas import CalculationResults, ValidationCheck, ValidationChecks
from backend.models.constants import SPINDLE_MAX_RPM, SPINDLE_MAX_POWER_KW


class ValidationService:
    """
    8-Checks Validation System

    1. rpm_within_limit: n <= spindle_max (30000)
    2. power_available: power_kw <= machine_power (0.7 kW)
    3. feed_rate_reasonable: vf between 10 and 5000 mm/min
    4. coating_valid: Already checked in calculation
    5. ld_ratio_stability: Check if ld_ratio requires reduction
    6. surface_quality_achievable: ae >= 0.5mm (too small = impossible)
    7. tool_engagement_safe: ap reasonable for tool
    8. temperature_safe: temp_c <= max material temp
    """

    def validate(self, results: CalculationResults) -> ValidationChecks:
        """Run all 8 validation checks"""

        checks = [
            self._check_rpm_within_limit(results.n_rpm),
            self._check_power_available(results.power_kw),
            self._check_feed_rate_reasonable(results.vf_mm_min),
            self._check_coating_valid(),  # Always passes (checked earlier)
            self._check_ld_ratio_stability(results.ld_ratio),
            self._check_surface_quality_achievable(results.ae_mm),
            self._check_tool_engagement_safe(results.ap_mm, results.tool.geometry.DC),
            self._check_temperature_safe(results.chip_temperature_c),
        ]

        all_passed = all(check.passed for check in checks)

        return ValidationChecks(all_passed=all_passed, checks=checks)

    def _check_rpm_within_limit(self, n_rpm: int) -> ValidationCheck:
        """Check 1: RPM within spindle limit"""
        passed = n_rpm <= SPINDLE_MAX_RPM

        return ValidationCheck(
            name="rpm_within_limit",
            passed=passed,
            message=(
                f"RPM {n_rpm} within spindle limit {SPINDLE_MAX_RPM}"
                if passed
                else f"RPM {n_rpm} exceeds spindle limit {SPINDLE_MAX_RPM}"
            ),
            severity="info" if passed else "error",
            value=float(n_rpm),
            limit=float(SPINDLE_MAX_RPM),
        )

    def _check_power_available(self, power_kw: float) -> ValidationCheck:
        """Check 2: Power available"""
        passed = power_kw <= SPINDLE_MAX_POWER_KW

        return ValidationCheck(
            name="power_available",
            passed=passed,
            message=(
                f"Power {power_kw:.2f}kW within machine limit {SPINDLE_MAX_POWER_KW}kW"
                if passed
                else f"Power {power_kw:.2f}kW exceeds machine limit {SPINDLE_MAX_POWER_KW}kW"
            ),
            severity="info" if passed else "warning",
            value=power_kw,
            limit=SPINDLE_MAX_POWER_KW,
        )

    def _check_feed_rate_reasonable(self, vf: float) -> ValidationCheck:
        """Check 3: Feed rate reasonable (10-5000 mm/min)"""
        passed = 10 <= vf <= 5000

        return ValidationCheck(
            name="feed_rate_reasonable",
            passed=passed,
            message=(
                f"Feed rate {vf:.1f} mm/min is reasonable (10-5000 mm/min)"
                if passed
                else f"Feed rate {vf:.1f} mm/min outside reasonable range (10-5000 mm/min)"
            ),
            severity="info" if passed else "warning",
            value=vf,
            limit=5000.0,
        )

    def _check_coating_valid(self) -> ValidationCheck:
        """Check 4: Coating valid (already validated in calculation)"""
        return ValidationCheck(
            name="coating_valid",
            passed=True,
            message="Coating validated for material",
            severity="info",
        )

    def _check_ld_ratio_stability(self, ld_ratio: float) -> ValidationCheck:
        """Check 5: L/D ratio stability"""
        # Warning if L/D > 4, error if L/D > 6
        if ld_ratio > 6.0:
            passed = False
            severity = "error"
            message = f"L/D ratio {ld_ratio:.2f} > 6.0: Very high risk of chatter"
        elif ld_ratio > 4.0:
            passed = False
            severity = "warning"
            message = f"L/D ratio {ld_ratio:.2f} > 4.0: Increased risk of vibration"
        else:
            passed = True
            severity = "info"
            message = f"L/D ratio {ld_ratio:.2f} is stable"

        return ValidationCheck(
            name="ld_ratio_stability",
            passed=passed,
            message=message,
            severity=severity,
            value=ld_ratio,
            limit=4.0,
        )

    def _check_surface_quality_achievable(self, ae: float) -> ValidationCheck:
        """Check 6: Surface quality achievable (ae >= 0.5mm minimum)"""
        passed = ae >= 0.5

        return ValidationCheck(
            name="surface_quality_achievable",
            passed=passed,
            message=(
                f"Radial engagement {ae:.2f}mm is sufficient"
                if passed
                else f"Radial engagement {ae:.2f}mm too small (min 0.5mm)"
            ),
            severity="info" if passed else "warning",
            value=ae,
            limit=0.5,
        )

    def _check_tool_engagement_safe(self, ap: float, dc: float) -> ValidationCheck:
        """Check 7: Tool engagement safe"""
        # ap should not exceed DC (100%)
        passed = ap <= dc

        return ValidationCheck(
            name="tool_engagement_safe",
            passed=passed,
            message=(
                f"Axial depth {ap:.2f}mm is safe for tool diameter {dc:.2f}mm"
                if passed
                else f"Axial depth {ap:.2f}mm exceeds tool diameter {dc:.2f}mm"
            ),
            severity="info" if passed else "error",
            value=ap,
            limit=dc,
        )

    def _check_temperature_safe(self, temp_c: float) -> ValidationCheck:
        """Check 8: Temperature safe (< 700°C)"""
        passed = temp_c <= 700

        return ValidationCheck(
            name="temperature_safe",
            passed=passed,
            message=(
                f"Chip temperature {temp_c:.1f}°C is safe"
                if passed
                else f"Chip temperature {temp_c:.1f}°C exceeds safe limit (700°C)"
            ),
            severity="info" if passed else "warning",
            value=temp_c,
            limit=700.0,
        )
