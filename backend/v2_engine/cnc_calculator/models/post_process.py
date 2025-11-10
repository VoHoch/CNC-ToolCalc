"""Post-processor configuration model."""

from pydantic import BaseModel


class PostProcess(BaseModel):
    """Post-processor configuration for CNC tool."""

    comment: str = ""
    number: int = 1
    diameter_offset: int = 1
    length_offset: int = 1

    # Tool change
    manual_tool_change: bool = False
    break_control: bool = False

    # Spindle direction
    clockwise: bool = True
