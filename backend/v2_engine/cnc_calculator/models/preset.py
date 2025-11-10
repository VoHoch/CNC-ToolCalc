"""Preset model for cutting data."""

from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from .validation_result import ValidationResult


class Preset(BaseModel):
    """Cutting data preset for one material + operation combination."""

    # Identity
    guid: UUID = Field(default_factory=uuid4)
    name: str  # "Alu - Schlicht(F)"
    material: str  # "Alu"
    operation: str  # "Schlicht(F)"
    comment: str = ""

    # Base Parameters (from calculation)
    vc_base: float = Field(..., gt=0, description="Base vc [m/min]")
    fz_base: float = Field(..., gt=0, description="Base fz [mm]")

    # Final Parameters (after all adjustments)
    vc_final: float = Field(..., gt=0)
    fz_final: float = Field(..., gt=0)
    n_rpm: float = Field(..., gt=0, le=24000)
    vf_mm_per_min: float = Field(..., gt=0)

    # Depths of Cut
    ae_mm: float = Field(..., gt=0, description="Radial depth [mm]")
    ap_mm: float = Field(..., gt=0, description="Axial depth [mm]")

    # Feed Factors
    feed_entry: float = Field(0.5, gt=0, le=2.0)
    feed_exit: float = Field(1.0, gt=0, le=2.0)
    feed_ramp: float = Field(0.5, gt=0, le=2.0)
    feed_plunge: float = Field(0.25, gt=0, le=2.0)
    feed_transition: float = Field(1.0, gt=0, le=2.0)
    ramp_angle_deg: float = Field(2.0, gt=0, le=90)

    # Coolant
    coolant: str = "disabled"

    # Fusion 360 Expressions (CRITICAL - must have all 12!)
    # Note: tool-coolant, use-stepdown, use-stepover are TOP-LEVEL fields, NOT expressions
    expressions: dict = Field(default_factory=dict)

    # Validation
    validation_result: Optional[ValidationResult] = None

    # State
    accepted: bool = False
    manually_edited: bool = False

    def validate_expressions(self) -> List[str]:
        """Ensure all required expressions are present.

        Returns:
            List of missing expression keys (empty if valid)
        """
        # Based on Fusion 360 feedback: ALL these values need to be parametric
        # User confirmed: Einfahrvorschub, Ausfahrvorschub, etc. müssen fx-Icon haben
        required_keys = [
            "tool_surfaceSpeed",
            "tool_feedPerTooth",
            "tool_feedCutting",
            "tool_feedEntry",
            "tool_feedExit",
            "tool_feedPlunge",
            "tool_feedRamp",
            "tool_feedTransition",
            "tool_rampSpindleSpeed",
            "tool_rampAngle",
            "tool_stepdown",
            "tool_stepover",
        ]  # 12 expressions as required by user
        missing = [k for k in required_keys if k not in self.expressions]
        if missing:
            return [f"Missing expressions: {', '.join(missing)}"]
        return []
