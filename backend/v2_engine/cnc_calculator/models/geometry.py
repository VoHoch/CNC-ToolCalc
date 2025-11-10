"""Geometry model for CNC tools."""

from typing import List, Optional
from pydantic import BaseModel, Field


class Geometry(BaseModel):
    """Tool geometry according to Fusion 360 specification."""

    # REQUIRED (Fusion 360)
    DC: float = Field(..., gt=0, description="Cutting Diameter [mm]")
    DCX: float = Field(..., gt=0, description="Max Cutting Diameter [mm]")
    NOF: int = Field(..., ge=1, description="Number of Flutes")
    LCF: float = Field(..., gt=0, description="Length of Cut [mm]")
    shoulder_diameter: float = Field(..., gt=0)
    shoulder_length: float = Field(..., gt=0)

    # OPTIONAL
    OAL: Optional[float] = Field(None, gt=0, description="Overall Length")
    LB: Optional[float] = Field(None, gt=0, description="Body Length")
    SFDM: Optional[float] = Field(None, gt=0, description="Shank Diameter")
    RE: float = Field(0.0, ge=0, description="Corner Radius")
    TA: float = Field(0.0, ge=0, description="Taper Angle [°]")

    # Geometry-Dependent Operations (v2.0)
    corner_radius: Optional[float] = Field(None, gt=0, description="Corner Radius for Radius Mills [mm]")
    angle: Optional[float] = Field(None, gt=0, le=180, description="Angle for V-Tools/Chamfer Mills [°]")
    tip_angle: Optional[float] = Field(None, ge=0, le=180, description="Tip Angle for V-Bit [°] (alias for angle)")

    def validate_consistency(self) -> List[str]:
        """Validate geometric consistency.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        if self.DCX < self.DC:
            errors.append("DCX must be >= DC")
        if self.shoulder_diameter < self.DC:
            errors.append("shoulder_diameter should be >= DC")
        return errors
