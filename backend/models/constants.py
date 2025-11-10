"""
CNC-ToolCalc Backend - Material & Operation Constants
Version: 0.0.1-alpha
Source: V4 Final Architecture Document, Part 2 (Domänenmodell)
"""

from backend.models.schemas import Material, Operation, MaterialType, OperationType


# ============================================================================
# MATERIALS (7 Materials, Hardness-Sorted)
# ============================================================================

MATERIALS = [
    Material(
        id=MaterialType.SOFTWOOD,
        name="Softwood (Weichholz)",
        hardness_order=1,
        color="#f4e4c1",
        category="wood",
        kc=40,
        vc_base=1000,
        dry_factor=1.0,
        max_temp=200,
        k_thermal=0.5
    ),
    Material(
        id=MaterialType.HARDWOOD,
        name="Hardwood (Hartholz)",
        hardness_order=2,
        color="#8b6f47",
        category="wood",
        kc=80,
        vc_base=800,
        dry_factor=1.0,
        max_temp=250,
        k_thermal=0.7
    ),
    Material(
        id=MaterialType.ACRYLIC,
        name="Acrylic (PMMA)",
        hardness_order=3,
        color="#60a5fa",
        category="plastic",
        kc=90,
        vc_base=600,
        dry_factor=0.9,
        max_temp=150,
        k_thermal=1.2
    ),
    Material(
        id=MaterialType.ALUMINIUM,
        name="Aluminium 6061/7075",
        hardness_order=4,
        color="#94a3b8",
        category="metal",
        kc=600,
        vc_base=377,
        dry_factor=0.85,
        max_temp=400,
        k_thermal=2.0
    ),
    Material(
        id=MaterialType.BRASS,
        name="Brass (Messing)",
        hardness_order=5,
        color="#fbbf24",
        category="metal",
        kc=800,
        vc_base=200,
        dry_factor=0.9,
        max_temp=450,
        k_thermal=2.2
    ),
    Material(
        id=MaterialType.COPPER,
        name="Copper (Kupfer)",
        hardness_order=6,
        color="#f97316",
        category="metal",
        kc=1000,
        vc_base=150,
        dry_factor=0.85,
        max_temp=450,
        k_thermal=3.0
    ),
    Material(
        id=MaterialType.STEEL_MILD,
        name="Steel (Mild Steel)",
        hardness_order=7,
        color="#475569",
        category="metal",
        kc=1800,
        vc_base=150,
        dry_factor=0.7,
        max_temp=600,
        k_thermal=4.0
    ),
    Material(
        id=MaterialType.STEEL_STAINLESS,
        name="Steel (Stainless)",
        hardness_order=8,
        color="#1e293b",
        category="metal",
        kc=2200,
        vc_base=80,
        dry_factor=0.65,
        max_temp=700,
        k_thermal=5.0
    ),
]

MATERIALS_MAP = {m.id: m for m in MATERIALS}


# ============================================================================
# OPERATIONS (13 Operations)
# ============================================================================

OPERATIONS = [
    # FACE Category (2 operations)
    Operation(
        id=OperationType.FACE_ROUGH,
        name="Face Milling (Roughing)",
        description="Schruppen von großen Flächen",
        category="FACE",
        icon="⬜",
        color="#fb923c",
        ae_factor=0.25,
        ap_factor=0.25,
        ap_reference="DC"
    ),
    Operation(
        id=OperationType.FACE_FINISH,
        name="Face Milling (Finishing)",
        description="Schlichten von Flächen für gute Oberfläche",
        category="FACE",
        icon="⬜",
        color="#fb923c",
        ae_factor=0.25,
        ap_factor=0.15,
        ap_reference="DC"
    ),

    # SLOT Category (4 operations)
    Operation(
        id=OperationType.SLOT_ROUGH,
        name="Slot Milling (Roughing)",
        description="Schruppen von Nuten",
        category="SLOT",
        icon="▭",
        color="#3b82f6",
        ae_factor=1.0,
        ap_factor=0.30,
        ap_reference="dynamic"
    ),
    Operation(
        id=OperationType.SLOT_FINISH,
        name="Slot Milling (Finishing)",
        description="Schlichten von Nuten",
        category="SLOT",
        icon="▭",
        color="#3b82f6",
        ae_factor=1.0,
        ap_factor=0.15,
        ap_reference="dynamic"
    ),
    Operation(
        id=OperationType.SLOT_FULL,
        name="Full Slotting",
        description="Volle Nutbreite + maximale Tiefe",
        category="SLOT",
        icon="▭",
        color="#3b82f6",
        ae_factor=1.0,
        ap_factor=0.50,
        ap_reference="DC"
    ),
    Operation(
        id=OperationType.SLOT_TROCHOIDAL,
        name="Trochoidal Slotting",
        description="Zirkular-interpolierte Nuten mit geringer Radiallast",
        category="SLOT",
        icon="⟳",
        color="#3b82f6",
        ae_factor=0.10,
        ap_factor=0.50,
        ap_reference="LCF"
    ),

    # GEOMETRY Category (3 operations)
    Operation(
        id=OperationType.GEO_CHAMFER,
        name="Chamfering",
        description="Fasen/Anfasen von Kanten",
        category="GEOMETRY",
        icon="◢",
        color="#06b6d4",
        ae_factor=0.05,
        ap_factor=0.10,
        ap_reference="DC"
    ),
    Operation(
        id=OperationType.GEO_RADIUS,
        name="Radius Milling",
        description="Radiusfräsen (innen/außen)",
        category="GEOMETRY",
        icon="◡",
        color="#06b6d4",
        ae_factor=0.05,
        ap_factor=0.15,
        ap_reference="DC"
    ),
    Operation(
        id=OperationType.GEO_POCKET,
        name="Pocket Milling",
        description="Taschen fräsen",
        category="GEOMETRY",
        icon="▢",
        color="#06b6d4",
        ae_factor=0.40,
        ap_factor=0.20,
        ap_reference="dynamic"
    ),

    # SPECIAL Category (3 operations)
    Operation(
        id=OperationType.CONTOUR_2D,
        name="2D Contouring",
        description="2D Konturfräsen",
        category="SPECIAL",
        icon="〰",
        color="#8b5cf6",
        ae_factor=0.10,
        ap_factor=0.15,
        ap_reference="dynamic"
    ),
    Operation(
        id=OperationType.CONTOUR_3D,
        name="3D Contouring",
        description="3D Konturfräsen (Finishing)",
        category="SPECIAL",
        icon="⛰",
        color="#8b5cf6",
        ae_factor=0.10,
        ap_factor=0.10,
        ap_reference="dynamic"
    ),
    Operation(
        id=OperationType.SPECIAL_ADAPTIVE,
        name="Adaptive Clearing",
        description="Adaptive Schruppen mit variablen Parametern",
        category="SPECIAL",
        icon="↻",
        color="#8b5cf6",
        ae_factor=0.40,
        ap_factor=0.30,
        ap_reference="LCF"
    ),
]

OPERATIONS_MAP = {op.id: op for op in OPERATIONS}


# ============================================================================
# COATING FACTORS
# ============================================================================

COATING_FACTORS = {
    "none": 1.0,
    "tin": 1.4,      # +40%
    "tialn": 1.6,    # +60%
    "altin": 1.8,    # +80%
    "diamond": 2.2,  # +120%
    "carbide": 1.5,  # +50%
}


# ============================================================================
# SURFACE QUALITY ADJUSTMENTS
# ============================================================================

SURFACE_QUALITY_FACTORS = {
    "roughing": {
        "ae": 1.0,
        "ap": 1.0,
        "vf": 1.2,  # +20% faster
    },
    "standard": {
        "ae": 1.0,
        "ap": 1.0,
        "vf": 1.0,
    },
    "finishing": {
        "ae": 0.7,   # -30%
        "ap": 0.8,   # -20%
        "vf": 0.8,   # -20%
    },
    "high_finish": {
        "ae": 0.5,   # -50%
        "ap": 0.6,   # -40%
        "vf": 0.6,   # -40%
    },
}


# ============================================================================
# MACHINE LIMITS (Makita RT0700C Reference)
# ============================================================================

SPINDLE_MAX_RPM = 30000
SPINDLE_MAX_POWER_KW = 0.7  # 700W
