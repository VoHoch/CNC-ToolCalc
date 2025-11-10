"""Enumerations for the CNC Calculator."""

from enum import Enum


class ToolType(str, Enum):
    """Tool type enumeration matching Fusion 360 specifications."""

    FLAT_END_MILL = "flat end mill"
    BALL_END_MILL = "ball end mill"
    BULL_NOSE_END_MILL = "bull nose end mill"
    FACE_MILL = "face mill"
    CHAMFER_MILL = "chamfer mill"
    THREAD_MILL = "thread mill"
    DRILL = "drill"
    RADIUS_MILL = "radius mill"
    SPOT_DRILL = "spot drill"


class OperationType(str, Enum):
    """Operation type enumeration for 12 milling operations."""

    # Slot Operations (4)
    PARTIAL_SLOT_OP = "PARTIAL_SLOT_OP"
    FULL_SLOT_OP = "FULL_SLOT_OP"
    TROCHOIDAL_SLOT_OP = "TROCHOIDAL_SLOT_OP"
    FINISH_SLOT_OP = "FINISH_SLOT_OP"

    # Face Operations (2)
    ROUGH_FACE_OP = "ROUGH_FACE_OP"
    FINISH_FACE_OP = "FINISH_FACE_OP"

    # Contour Operations (3)
    RADIUS_CONTOUR_OP = "RADIUS_CONTOUR_OP"
    CHAMFER_CONTOUR_OP = "CHAMFER_CONTOUR_OP"
    BALL_3D_OP = "BALL_3D_OP"

    # Special Operations (3)
    DRILLING_OP = "DRILLING_OP"
    VGROOVE_OP = "VGROOVE_OP"
    THREADING_OP = "THREADING_OP"


class ValidationStatus(str, Enum):
    """Validation status for traffic light system."""

    GREEN = "GREEN"      # Within acceptable range
    YELLOW = "YELLOW"    # Slightly elevated
    RED = "RED"          # Critical deviation
    PENDING = "PENDING"  # Not yet validated
