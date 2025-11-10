"""Expression builder for Fusion 360 cutting data."""

from ..models.operation import FeedFactors


class ExpressionBuilder:
    """Generates the 13 critical Fusion 360 expressions.

    CRITICAL: ALL 13 must be present or Fusion shows warnings!
    """

    def build_expressions(
        self,
        vc: float,
        fz: float,
        ae: float,
        ap: float,
        DC: float,
        LCF: float,
        feed_factors: FeedFactors,
    ) -> dict:
        """Build all 13 required expressions for Fusion 360.

        Args:
            vc: Cutting speed [m/min]
            fz: Feed per tooth [mm]
            ae: Radial depth of cut [mm]
            ap: Axial depth of cut [mm]
            DC: Tool diameter [mm]
            LCF: Length of cut (flute length) [mm]
            feed_factors: Feed factor configuration

        Returns:
            Dictionary with all 13 expression keys
        """
        # Calculate ratios for parametric expressions
        ae_ratio = ae / DC
        ap_ratio = ap / LCF

        expressions = {
            # 1-2: Base cutting parameters
            "tool_surfaceSpeed": f"{vc:.1f} mpm",
            "tool_feedPerTooth": f"{fz:.3f} mm",
            # 3-7: Feed expressions (relative to tool_feedCutting)
            "tool_feedEntry": f"tool_feedCutting*{feed_factors.entry}",
            "tool_feedExit": f"tool_feedCutting*{feed_factors.exit}",
            "tool_feedPlunge": f"tool_feedCutting*{feed_factors.plunge}",
            "tool_feedRamp": f"tool_feedCutting*{feed_factors.ramp}",
            "tool_feedTransition": f"tool_feedCutting*{feed_factors.transition}",
            # 8: Ramp RPM (usually 1:1 with main RPM)
            "tool_rampSpindleSpeed": "tool_spindleSpeed*1.0",
            # 9-10: Parametric depths (CRITICAL for Fusion adaptability)
            "tool_stepdown": f"tool_fluteLength*{ap_ratio:.6f}",
            "tool_stepover": f"tool_diameter*{ae_ratio:.6f}",
            # 11: Coolant mode
            "tool_coolant": "'disabled'",
            # 12-13: Enable flags
            "use_tool_stepdown": "true",
            "use_tool_stepover": "true",
        }

        return expressions
