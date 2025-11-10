"""
CNC-ToolCalc Backend - Pydantic Schemas
Version: 0.0.1-alpha
Implementation: 100% Cleanroom (NO V2.0 dependencies)
Architecture: V4 Final Consolidated
"""

from enum import Enum
from typing import Optional, Dict, List
from pydantic import BaseModel, Field


# ============================================================================
# ENUMS
# ============================================================================

class MaterialType(str, Enum):
    """7 Materials (hardness-sorted)"""
    SOFTWOOD = "softwood"
    HARDWOOD = "hardwood"
    ALUMINIUM = "aluminium"
    BRASS = "brass"
    COPPER = "copper"
    ACRYLIC = "acrylic"
    STEEL_MILD = "steel_mild"
    STEEL_STAINLESS = "steel_stainless"


class OperationType(str, Enum):
    """13 Operations (including SLOT_TROCHOIDAL)"""
    # FACE (2)
    FACE_ROUGH = "face_rough"
    FACE_FINISH = "face_finish"

    # SLOT (4)
    SLOT_ROUGH = "slot_rough"
    SLOT_FINISH = "slot_finish"
    SLOT_FULL = "slot_full"
    SLOT_TROCHOIDAL = "slot_trochoidal"

    # GEOMETRY (3)
    GEO_CHAMFER = "geo_chamfer"
    GEO_RADIUS = "geo_radius"
    GEO_POCKET = "geo_pocket"

    # SPECIAL (3)
    CONTOUR_2D = "contour_2d"
    CONTOUR_3D = "contour_3d"
    SPECIAL_ADAPTIVE = "special_adaptive"


class CoatingType(str, Enum):
    """6 Coating Types"""
    NONE = "none"
    TIN = "tin"          # +40%
    TIALN = "tialn"      # +60%
    ALTIN = "altin"      # +80%
    DIAMOND = "diamond"  # +120% (non-ferrous only)
    CARBIDE = "carbide"  # +50%


class SurfaceQuality(str, Enum):
    """4 Surface Quality Levels"""
    ROUGHING = "roughing"
    STANDARD = "standard"
    FINISHING = "finishing"
    HIGH_FINISH = "high_finish"


class CoolantType(str, Enum):
    """3 Coolant Types"""
    WET = "wet"
    DRY = "dry"
    MQL = "mql"


# ============================================================================
# TOOL MODELS
# ============================================================================

class ToolGeometry(BaseModel):
    """Tool Geometry Parameters"""
    DC: float = Field(..., description="Cutting Diameter [mm]", gt=0)
    LCF: float = Field(..., description="Length of Cut (Flute Length) [mm]", gt=0)
    NOF: int = Field(..., description="Number of Flutes", ge=1, le=12)
    DCON: float = Field(..., description="Connection Diameter [mm]", gt=0)
    OAL: float = Field(..., description="Overall Length [mm]", gt=0)
    SFDM: float = Field(..., description="Shank Diameter [mm]", gt=0)


class Tool(BaseModel):
    """Tool Model"""
    id: str = Field(..., description="Tool ID (e.g., T1, T2)")
    name: str = Field(..., description="Tool Name")
    type: str = Field(..., description="Tool Type (e.g., flat end mill)")
    geometry: ToolGeometry

    @property
    def ld_ratio(self) -> float:
        """Calculate L/D ratio"""
        return self.geometry.LCF / self.geometry.DC

    @property
    def ld_classification(self) -> str:
        """Classify tool by L/D ratio"""
        ratio = self.ld_ratio
        if ratio < 1.0:
            return "SHORT"
        elif ratio < 4.0:
            return "NORMAL"
        elif ratio < 6.0:
            return "LONG"
        else:
            return "VERY_LONG"


# ============================================================================
# MATERIAL MODELS
# ============================================================================

class Material(BaseModel):
    """Material Model"""
    id: MaterialType
    name: str
    hardness_order: int = Field(..., description="Hardness order (1=softest, 7=hardest)")
    color: str = Field(..., description="UI color hex code")
    category: str = Field(..., description="Category: wood, metal, plastic")

    # Material properties for calculation
    kc: float = Field(..., description="Specific cutting force [N/mm²]")
    vc_base: float = Field(..., description="Base cutting speed [m/min]")
    dry_factor: float = Field(..., description="Dry machining correction factor")
    max_temp: float = Field(..., description="Max chip temperature [°C]")
    k_thermal: float = Field(..., description="Thermal conductivity factor")


# ============================================================================
# OPERATION MODELS
# ============================================================================

class Operation(BaseModel):
    """Operation Model"""
    id: OperationType
    name: str
    description: str
    category: str = Field(..., description="FACE, SLOT, GEOMETRY, SPECIAL")
    icon: str
    color: str

    # Operation parameters
    ae_factor: float = Field(..., description="Radial engagement factor (% of DC)")
    ap_factor: float = Field(..., description="Axial depth factor")
    ap_reference: str = Field(..., description="AP reference: DC, LCF, or dynamic")


# ============================================================================
# CALCULATION REQUEST/RESPONSE
# ============================================================================

class CalculationRequest(BaseModel):
    """Calculation Request"""
    tool_id: str
    material: MaterialType
    operation: OperationType
    coating: Optional[CoatingType] = CoatingType.NONE
    surface_quality: Optional[SurfaceQuality] = SurfaceQuality.STANDARD
    coolant: Optional[CoolantType] = CoolantType.WET


class CalculationResults(BaseModel):
    """10-Phase Calculation Results"""
    # Phase 1: Input
    tool: Tool
    material: MaterialType
    operation: OperationType

    # Phase 2: vc + Coating
    vc_base: float = Field(..., description="Base cutting speed [m/min]")
    coating_factor: float = Field(..., description="Coating multiplication factor")
    vc_final: float = Field(..., description="Final cutting speed [m/min]")

    # Phase 3: Spindle Speed
    n_rpm: int = Field(..., description="Spindle speed [RPM]")

    # Phase 4: Chip Load
    fz_base: float = Field(..., description="Base chip load [mm]")
    dry_factor: float = Field(..., description="Dry machining correction")
    fz_final: float = Field(..., description="Final chip load [mm]")

    # Phase 5: Feed Rate
    vf_mm_min: float = Field(..., description="Feed rate [mm/min]")
    vf_entry: float = Field(..., description="Entry feed rate [mm/min]")
    vf_ramp: float = Field(..., description="Ramp feed rate [mm/min]")
    vf_plunge: float = Field(..., description="Plunge feed rate [mm/min]")
    ramp_angle: float = Field(default=2.0, description="Ramp angle [degrees]")

    # Phase 6: Engagement
    ae_mm: float = Field(..., description="Radial engagement [mm]")
    ap_mm: float = Field(..., description="Axial depth [mm]")
    ap_reference: str = Field(..., description="AP reference used: DC or LCF")

    # Phase 7: Power & Torque
    mrr: float = Field(..., description="Material Removal Rate [cm³/min]")
    power_kw: float = Field(..., description="Cutting power [kW]")
    torque_nm: float = Field(..., description="Torque [Nm]")

    # Phase 8: Thermal
    chip_temperature_c: float = Field(..., description="Chip temperature [°C]")

    # Phase 9: Chip Formation
    chip_formation: str = Field(..., description="Chip type prediction")

    # Phase 10: L/D Stability
    ld_ratio: float = Field(..., description="L/D ratio")
    ld_classification: str = Field(..., description="Tool length classification")
    stability_warnings: List[str] = Field(default_factory=list)


class ValidationCheck(BaseModel):
    """Single validation check"""
    name: str
    passed: bool
    message: str
    severity: str = Field(..., description="info, warning, error")
    value: Optional[float] = None
    limit: Optional[float] = None


class ValidationChecks(BaseModel):
    """8 Validation Checks"""
    all_passed: bool
    checks: List[ValidationCheck]


class CalculationResponse(BaseModel):
    """Complete Calculation Response"""
    calculation_id: str
    timestamp: str
    results: CalculationResults
    validation: ValidationChecks
    warnings: List[str] = Field(default_factory=list)
