"""Tool model for CNC tools."""

from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from .enums import ToolType
from .geometry import Geometry
from .holder import Holder
from .post_process import PostProcess
from .preset import Preset


class Tool(BaseModel):
    """Represents a CNC cutting tool."""

    # Identity
    guid: UUID = Field(default_factory=uuid4)
    tool_id: str = Field(..., pattern=r"^T\d+$")  # T1, T2, etc.
    number: int = Field(..., ge=1)
    description: str

    # Vendor Info
    vendor: str = "Generic"
    product_id: str = ""
    product_link: str = ""

    # Classification
    type: ToolType
    unit: str = "millimeters"
    body_material_code: str = "carbide"
    grade: str = "Mill Generic"

    # Geometry & Holder
    geometry: Geometry
    holder: Holder
    post_process: PostProcess

    # Cutting Data (calculated)
    presets: List[Preset] = Field(default_factory=list)

    # State
    selected: bool = False  # For GUI

    # CRITICAL: Store complete raw tool data from Fusion 360 for 1:1 export
    # This preserves ALL original fields (geometry, holder, post-process, etc.)
    # Only "start-values" (presets) will be replaced with calculated data
    raw_data: Optional[Dict[str, Any]] = Field(default=None, description="Complete tool data from import")

    def calculate_ld_ratio(self) -> float:
        """Calculate Length-to-Diameter ratio.

        Returns:
            L/D ratio (LCF / DC)
        """
        return self.geometry.LCF / self.geometry.DC

    def get_max_ap(self) -> float:
        """Get maximum axial depth of cut.

        Returns:
            Maximum axial depth = LCF
        """
        return self.geometry.LCF

    def to_fusion_dict(self) -> dict:
        """Convert to Fusion 360 format.

        Returns:
            Dictionary ready for Fusion 360 export
        """
        # Implementation will be in io/tools_writer.py
        raise NotImplementedError("Implemented in tools_writer module")
