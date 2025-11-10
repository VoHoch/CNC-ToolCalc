"""Material configuration model."""

from typing import Optional
from pydantic import BaseModel, Field


class DryMachiningFactors(BaseModel):
    """Adjustment factors for dry machining (no coolant)."""

    vc_factor: float = Field(..., gt=0, le=1.5, description="Cutting speed adjustment")
    fz_factor: float = Field(..., gt=0, le=2.0, description="Feed per tooth adjustment")
    ae_factor: float = Field(..., gt=0, le=1.5, description="Radial depth adjustment")
    ap_factor: float = Field(..., gt=0, le=1.5, description="Axial depth adjustment")
    reason: str = ""


class MaterialConfig(BaseModel):
    """Material-specific configuration."""

    id: str  # "Alu", "HolzW", etc.
    name: str  # "Aluminium (Knetlegierung)"
    color: str = "#FFFFFF"  # Hex color for GUI

    # Base cutting parameters
    vc_nominal: float = Field(..., gt=0, description="Nominal vc [m/min]")
    fz_base_at_d6: float = Field(..., gt=0, description="fz @ D=6mm [mm]")
    fz_exponent: float = Field(0.35, gt=0, description="Diameter scaling exponent")

    # RPM limits
    rpm_min: int = Field(2000, ge=0)
    rpm_max: int = Field(24000, ge=0)

    # Dry machining factors
    dry_factors: DryMachiningFactors

    # Validation reference (if available)
    sorotec_reference: Optional[dict] = None
