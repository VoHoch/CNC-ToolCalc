"""Length-to-Diameter (L/D) ratio adjustment rules."""

from dataclasses import dataclass


@dataclass
class LCDAdjustment:
    """Adjustment factors based on L/D ratio."""

    ld_ratio: float
    fz_factor: float
    ae_factor: float
    warning: str = ""


class LCDRules:
    """Rules for adjusting parameters based on Length-to-Diameter ratio.

    High L/D ratios indicate slender tools that are more prone to:
    - Deflection
    - Vibration (chatter)
    - Tool breakage

    Adjustments reduce cutting forces to compensate.
    """

    def __init__(self):
        """Initialize LCD thresholds and adjustment factors."""
        self.thresholds = {
            "normal": 3.0,  # L/D <= 3: No adjustment
            "moderate": 5.0,  # L/D <= 5: Small reduction
            "high": 7.0,  # L/D <= 7: Medium reduction
            "critical": 10.0,  # L/D <= 10: Large reduction
        }

    def get_adjustment(self, ld_ratio: float) -> LCDAdjustment:
        """Get adjustment factors for given L/D ratio.

        Args:
            ld_ratio: Length-to-Diameter ratio (LCF / DC)

        Returns:
            LCDAdjustment with appropriate factors
        """
        if ld_ratio <= self.thresholds["normal"]:
            return LCDAdjustment(
                ld_ratio=ld_ratio,
                fz_factor=1.00,
                ae_factor=1.00,
                warning="",
            )
        elif ld_ratio <= self.thresholds["moderate"]:
            return LCDAdjustment(
                ld_ratio=ld_ratio,
                fz_factor=0.90,
                ae_factor=0.95,
                warning="Moderate L/D ratio - slight reduction",
            )
        elif ld_ratio <= self.thresholds["high"]:
            return LCDAdjustment(
                ld_ratio=ld_ratio,
                fz_factor=0.80,
                ae_factor=0.90,
                warning="High L/D ratio - medium reduction for stability",
            )
        elif ld_ratio <= self.thresholds["critical"]:
            return LCDAdjustment(
                ld_ratio=ld_ratio,
                fz_factor=0.70,
                ae_factor=0.85,
                warning="Critical L/D ratio - large reduction, risk of chatter",
            )
        else:
            return LCDAdjustment(
                ld_ratio=ld_ratio,
                fz_factor=0.60,
                ae_factor=0.80,
                warning="Extreme L/D ratio (>10) - very conservative parameters!",
            )
