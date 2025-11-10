"""Holder model for CNC tools."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class Holder(BaseModel):
    """Tool holder model."""

    description: str = "Generic Holder"
    vendor: str = "Generic"
    product_id: str = ""
    product_link: str = ""

    # Holder geometry (basic)
    diameter: float = Field(default=6.0, gt=0, description="Holder diameter [mm]")
    length: float = Field(default=50.0, gt=0, description="Holder length [mm]")

    # CRITICAL: Store complete raw holder data from Fusion 360 for 1:1 export
    # This preserves all fields: type, unit, gaugeLength, segments, guid, etc.
    raw_data: Optional[Dict[str, Any]] = Field(default=None, description="Complete holder data from import")
