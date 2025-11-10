"""Base calculations for CNC machining."""

import math


class BaseCalculator:
    """Base calculator for fundamental CNC calculations."""

    @staticmethod
    def calculate_rpm(vc: float, diameter: float) -> float:
        """Calculate spindle speed (RPM) from cutting speed and diameter.

        Formula: n = (vc × 1000) / (π × D)

        Args:
            vc: Cutting speed [m/min]
            diameter: Tool diameter [mm]

        Returns:
            Spindle speed [RPM]
        """
        if diameter <= 0:
            raise ValueError("Diameter must be positive")
        if vc <= 0:
            raise ValueError("Cutting speed must be positive")

        return (vc * 1000.0) / (math.pi * diameter)

    @staticmethod
    def calculate_vc(rpm: float, diameter: float) -> float:
        """Calculate cutting speed from RPM and diameter.

        Formula: vc = (π × D × n) / 1000

        Args:
            rpm: Spindle speed [RPM]
            diameter: Tool diameter [mm]

        Returns:
            Cutting speed [m/min]
        """
        if diameter <= 0:
            raise ValueError("Diameter must be positive")
        if rpm <= 0:
            raise ValueError("RPM must be positive")

        return (math.pi * diameter * rpm) / 1000.0

    @staticmethod
    def calculate_vf(fz: float, nof: int, rpm: float) -> float:
        """Calculate feed rate from feed per tooth, number of flutes, and RPM.

        Formula: vf = fz × NOF × n

        Args:
            fz: Feed per tooth [mm]
            nof: Number of flutes
            rpm: Spindle speed [RPM]

        Returns:
            Feed rate [mm/min]
        """
        if fz <= 0:
            raise ValueError("Feed per tooth must be positive")
        if nof < 1:
            raise ValueError("Number of flutes must be >= 1")
        if rpm <= 0:
            raise ValueError("RPM must be positive")

        return fz * nof * rpm

    @staticmethod
    def scale_fz_by_diameter(
        fz_base: float, exponent: float, diameter: float, base_diameter: float = 6.0
    ) -> float:
        """Scale feed per tooth by diameter using power law.

        Formula: fz = fz_base × (D / D_base) ^ exponent

        Args:
            fz_base: Base feed per tooth at base diameter [mm]
            exponent: Scaling exponent (typically 0.3-0.35)
            diameter: Actual tool diameter [mm]
            base_diameter: Reference diameter (default 6mm)

        Returns:
            Scaled feed per tooth [mm]
        """
        if fz_base <= 0:
            raise ValueError("Base feed per tooth must be positive")
        if diameter <= 0:
            raise ValueError("Diameter must be positive")
        if base_diameter <= 0:
            raise ValueError("Base diameter must be positive")

        return fz_base * ((diameter / base_diameter) ** exponent)
