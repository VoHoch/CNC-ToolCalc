"""Operation configuration model."""

from typing import List
from pydantic import BaseModel, Field


class FeedFactors(BaseModel):
    """Relative feed factors for different cutting operations."""

    entry: float = 0.5
    exit: float = 1.0
    ramp: float = 0.5
    plunge: float = 0.25
    transition: float = 1.0
    ramp_angle_deg: float = 2.0


class OperationConfig(BaseModel):
    """Operation-specific configuration."""

    id: str  # "OP_PLANEN_GROB"
    name: str  # "Planen (Grob)"
    label: str  # Display name
    description: str

    # Tool type compatibility
    tool_types: List[str]  # ["face_mill", "flat_end_mill"]

    # Depth ratios
    ae_ratio: float = Field(..., gt=0, description="Radial ratio (× DC)")
    ap_ratio: float = Field(..., gt=0, description="Axial ratio (× DC or LCF)")

    # Adjustment factors
    vc_factor: float = Field(1.0, gt=0)
    fz_factor: float = Field(1.0, gt=0)

    # Feed factors
    feed_factors: FeedFactors

    # Notes
    notes: str = ""
