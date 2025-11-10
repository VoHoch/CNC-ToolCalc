"""Validation against Sorotec reference data."""

import logging
from typing import Optional
from ..models import Preset, ValidationResult, ValidationStatus, Tool

logger = logging.getLogger(__name__)


class Validator:
    """Validates calculated cutting data against Sorotec reference."""

    def __init__(self, sorotec_reference: dict):
        """Initialize validator.

        Args:
            sorotec_reference: Sorotec reference data dictionary
        """
        self.reference_data = sorotec_reference.get("reference_data", {})
        self.tolerances = sorotec_reference.get("validation_tolerances", {})

        self.green_threshold = self.tolerances.get("green_threshold_pct", 15)
        self.yellow_threshold = self.tolerances.get("yellow_threshold_pct", 30)
        self.red_threshold = self.tolerances.get("red_threshold_pct", 50)

    def validate_preset(self, preset: Preset, tool: Tool) -> ValidationResult:
        """Validate a preset against Sorotec reference.

        Args:
            preset: Preset to validate
            tool: Tool object for context

        Returns:
            ValidationResult with status and messages
        """
        # Try to find reference data
        ref_data = self._find_reference(
            preset.material, tool.geometry.DC, tool.geometry.NOF
        )

        if not ref_data:
            logger.debug(
                f"No reference data for {preset.material} "
                f"D{tool.geometry.DC} NOF{tool.geometry.NOF}"
            )
            return ValidationResult(
                status=ValidationStatus.PENDING,
                recommendations=[
                    "Keine Sorotec-Referenzdaten für diese Konfiguration"
                ],
            )

        # Calculate deviations
        vc_delta_pct = self._calculate_deviation_pct(
            preset.vc_final, ref_data.get("vc", 0)
        )
        fz_delta_pct = self._calculate_deviation_pct(
            preset.fz_final, ref_data.get("fz", 0)
        )

        # Determine status
        max_delta = max(abs(vc_delta_pct), abs(fz_delta_pct))
        status = self._determine_status(max_delta)

        # Generate messages
        warnings, errors, recommendations = self._generate_messages(
            status, vc_delta_pct, fz_delta_pct, ref_data
        )

        return ValidationResult(
            status=status,
            vc_delta_pct=vc_delta_pct,
            fz_delta_pct=fz_delta_pct,
            warnings=warnings,
            errors=errors,
            recommendations=recommendations,
            sorotec_ref_vc=ref_data.get("vc"),
            sorotec_ref_fz=ref_data.get("fz"),
        )

    def _find_reference(
        self, material: str, diameter: float, nof: int
    ) -> Optional[dict]:
        """Find matching reference data.

        Args:
            material: Material identifier
            diameter: Tool diameter
            nof: Number of flutes

        Returns:
            Reference data dict or None if not found
        """
        material_refs = self.reference_data.get(material, {})

        # Try exact match first
        key = f"D{int(diameter)}_NOF{nof}"
        if key in material_refs:
            return material_refs[key]

        # Try closest diameter match
        for ref_key, ref_data in material_refs.items():
            if ref_data.get("diameter") == diameter and ref_data.get("flutes") == nof:
                return ref_data

        return None

    def _calculate_deviation_pct(self, calculated: float, reference: float) -> float:
        """Calculate percentage deviation.

        Args:
            calculated: Calculated value
            reference: Reference value

        Returns:
            Percentage deviation (positive if calculated > reference)
        """
        if reference == 0:
            return 0.0

        return ((calculated - reference) / reference) * 100.0

    def _determine_status(self, max_delta_pct: float) -> ValidationStatus:
        """Determine validation status based on max deviation.

        Args:
            max_delta_pct: Maximum absolute deviation percentage

        Returns:
            ValidationStatus enum
        """
        if max_delta_pct <= self.green_threshold:
            return ValidationStatus.GREEN
        elif max_delta_pct <= self.yellow_threshold:
            return ValidationStatus.YELLOW
        else:
            return ValidationStatus.RED

    def _generate_messages(
        self,
        status: ValidationStatus,
        vc_delta_pct: float,
        fz_delta_pct: float,
        ref_data: dict,
    ) -> tuple:
        """Generate warning, error, and recommendation messages.

        Args:
            status: Validation status
            vc_delta_pct: vc deviation percentage
            fz_delta_pct: fz deviation percentage
            ref_data: Reference data

        Returns:
            Tuple of (warnings, errors, recommendations)
        """
        warnings = []
        errors = []
        recommendations = []

        if status == ValidationStatus.GREEN:
            recommendations.append(
                f"Werte liegen im grünen Bereich (±{self.green_threshold}%)"
            )

        elif status == ValidationStatus.YELLOW:
            if abs(vc_delta_pct) > self.green_threshold:
                warnings.append(
                    f"vc ist {vc_delta_pct:+.1f}% von Sorotec-Referenz "
                    f"({ref_data.get('vc')} m/min) abweichend"
                )
            if abs(fz_delta_pct) > self.green_threshold:
                warnings.append(
                    f"fz ist {fz_delta_pct:+.1f}% von Sorotec-Referenz "
                    f"({ref_data.get('fz')} mm) abweichend"
                )
            recommendations.append(
                "Werte leicht erhöht - testen oder konservativer anpassen"
            )

        else:  # RED
            if abs(vc_delta_pct) > self.yellow_threshold:
                errors.append(
                    f"vc ist {vc_delta_pct:+.1f}% von Sorotec-Referenz "
                    f"({ref_data.get('vc')} m/min) abweichend - KRITISCH!"
                )
            if abs(fz_delta_pct) > self.yellow_threshold:
                errors.append(
                    f"fz ist {fz_delta_pct:+.1f}% von Sorotec-Referenz "
                    f"({ref_data.get('fz')} mm) abweichend - KRITISCH!"
                )
            recommendations.append(
                "Werte stark abweichend - unbedingt überprüfen oder anpassen!"
            )

        return warnings, errors, recommendations
