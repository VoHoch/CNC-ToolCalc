"""Validation result model - v2.0 Multi-Level Validation."""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from .enums import ValidationStatus


class ValidationResult(BaseModel):
    """Result of parameter validation with Red/Yellow/Green status system.

    v1.0: Sorotec reference validation
    v2.0: Multi-level validation (ae, ap, MRR, Power, Geometry)
    """

    status: ValidationStatus = Field(default=ValidationStatus.PENDING)

    # v1.0 Fields (Sorotec reference validation)
    vc_delta_pct: float = 0.0
    fz_delta_pct: float = 0.0
    sorotec_ref_vc: Optional[float] = None
    sorotec_ref_fz: Optional[float] = None

    # v2.0 Fields (Multi-level validation)
    limits_applied: Dict = Field(default_factory=dict, description="Limits used for validation")
    mrr_calculated: Optional[float] = Field(None, description="Material Removal Rate [cm³/min]")
    power_calculated: Optional[float] = Field(None, description="Required power [kW]")
    ld_ratio: Optional[float] = Field(None, description="L/D ratio of tool")

    # Messages (compatible with both versions)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

    def is_safe(self) -> bool:
        """Returns True if status is GREEN or YELLOW (not RED).

        Returns:
            bool: True if parameters are acceptable
        """
        return self.status in [ValidationStatus.GREEN, ValidationStatus.YELLOW]

    def get_icon(self) -> str:
        """Get traffic light emoji.

        Returns:
            Emoji string representing validation status
        """
        return {
            ValidationStatus.GREEN: "🟢",
            ValidationStatus.YELLOW: "🟡",
            ValidationStatus.RED: "🔴",
            ValidationStatus.PENDING: "⚪",
        }[self.status]

    def get_display_icon(self) -> str:
        """Get icon for GUI display (v2.0 format with checkmarks).

        Returns:
            str: Emoji icon representing status
        """
        icons = {
            ValidationStatus.GREEN: "✅",
            ValidationStatus.YELLOW: "⚠️",
            ValidationStatus.RED: "❌",
            ValidationStatus.PENDING: "⚪"
        }
        return icons.get(self.status, "❓")

    def get_summary(self) -> str:
        """Get summary text.

        Returns:
            Human-readable summary of validation status
        """
        if self.status == ValidationStatus.GREEN:
            return "✅ All parameters within safe limits"
        elif self.status == ValidationStatus.YELLOW:
            count = len(self.warnings)
            return f"⚠️ {count} warning(s) - Review recommended"
        elif self.status == ValidationStatus.RED:
            count = len(self.errors)
            return f"❌ {count} error(s) - UNSAFE parameters!"
        else:
            return "⚪ Not validated yet"

    def get_details(self) -> str:
        """Get detailed report with all errors and warnings (v2.0).

        Returns:
            str: Multi-line detailed report
        """
        lines = [self.get_summary()]

        if self.errors:
            lines.append("\nErrors:")
            for error in self.errors:
                lines.append(f"  • {error}")

        if self.warnings:
            lines.append("\nWarnings:")
            for warning in self.warnings:
                lines.append(f"  • {warning}")

        if self.recommendations:
            lines.append("\nRecommendations:")
            for rec in self.recommendations:
                lines.append(f"  • {rec}")

        if self.mrr_calculated is not None:
            lines.append(f"\nMRR: {self.mrr_calculated:.0f} cm³/min")

        if self.power_calculated is not None:
            lines.append(f"Power: {self.power_calculated:.1f} kW")

        if self.ld_ratio is not None and self.ld_ratio > 3.0:
            lines.append(f"L/D Ratio: {self.ld_ratio:.1f} (limits reduced)")

        return "\n".join(lines)
