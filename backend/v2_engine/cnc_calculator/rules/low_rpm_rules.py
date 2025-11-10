"""Low RPM compensation rules."""


class LowRPMRules:
    """Rules for compensating when operating at low RPM.

    At low RPM (<4500), tools are more prone to rubbing rather than cutting.
    This can lead to poor surface finish and increased tool wear.

    Compensation: Reduce fz slightly to maintain chip load effectiveness.
    """

    def __init__(self, threshold_rpm: float = 4500, fz_factor: float = 0.90):
        """Initialize low RPM rules.

        Args:
            threshold_rpm: RPM below which compensation applies (default 4500)
            fz_factor: Feed per tooth reduction factor (default 0.90 = -10%)
        """
        self.threshold_rpm = threshold_rpm
        self.fz_factor = fz_factor

    def needs_compensation(self, rpm: float) -> bool:
        """Check if RPM requires compensation.

        Args:
            rpm: Spindle speed [RPM]

        Returns:
            True if rpm is below threshold
        """
        return rpm < self.threshold_rpm

    def get_fz_adjustment(self, rpm: float) -> float:
        """Get feed per tooth adjustment factor.

        Args:
            rpm: Spindle speed [RPM]

        Returns:
            Adjustment factor (1.0 if no adjustment needed)
        """
        if self.needs_compensation(rpm):
            return self.fz_factor
        return 1.0

    def get_warning(self, rpm: float) -> str:
        """Get warning message if compensation is applied.

        Args:
            rpm: Spindle speed [RPM]

        Returns:
            Warning message (empty if no warning)
        """
        if self.needs_compensation(rpm):
            return (
                f"Low RPM ({rpm:.0f}) - feed per tooth reduced by "
                f"{(1-self.fz_factor)*100:.0f}% to prevent rubbing"
            )
        return ""
