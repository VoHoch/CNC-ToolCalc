"""
Unit Tests - Phase 6: Engagement (ae, ap) + Dynamic ap-reference
"""

import pytest
from backend.models.schemas import OperationType, SurfaceQuality
from backend.services.calculation_service import CalculationService


def test_ae_face_operation(sample_tool_30mm):
    """Face operations should use 25% DC for ae"""
    service = CalculationService()
    from backend.models.constants import OPERATIONS_MAP

    operation = OPERATIONS_MAP[OperationType.FACE_ROUGH]

    ae = service._calculate_ae(sample_tool_30mm, operation, SurfaceQuality.STANDARD)

    # ae = 30mm * 0.25 = 7.5mm
    assert ae == pytest.approx(7.5, rel=0.01)


def test_ae_slot_full(sample_tool_30mm):
    """Full slotting should use 100% DC for ae"""
    service = CalculationService()
    from backend.models.constants import OPERATIONS_MAP

    operation = OPERATIONS_MAP[OperationType.SLOT_FULL]

    ae = service._calculate_ae(sample_tool_30mm, operation, SurfaceQuality.STANDARD)

    # ae = 30mm * 1.0 = 30mm
    assert ae == pytest.approx(30.0, rel=0.01)


def test_ae_slot_trochoidal(sample_tool_30mm):
    """Trochoidal slotting should use 10% DC for ae"""
    service = CalculationService()
    from backend.models.constants import OPERATIONS_MAP

    operation = OPERATIONS_MAP[OperationType.SLOT_TROCHOIDAL]

    ae = service._calculate_ae(sample_tool_30mm, operation, SurfaceQuality.STANDARD)

    # ae = 30mm * 0.10 = 3.0mm
    assert ae == pytest.approx(3.0, rel=0.01)


def test_ap_reference_dc_for_face(sample_tool_30mm):
    """Face operations should always use DC reference"""
    service = CalculationService()
    from backend.models.constants import OPERATIONS_MAP

    operation = OPERATIONS_MAP[OperationType.FACE_ROUGH]

    ap, ap_ref = service._calculate_ap(
        sample_tool_30mm, operation, SurfaceQuality.STANDARD
    )

    assert ap_ref == "DC"
    # ap = 30mm * 0.25 = 7.5mm
    assert ap == pytest.approx(7.5, rel=0.01)


def test_ap_reference_lcf_for_trochoidal(sample_tool_6mm):
    """Trochoidal slotting should always use LCF reference"""
    service = CalculationService()
    from backend.models.constants import OPERATIONS_MAP

    operation = OPERATIONS_MAP[OperationType.SLOT_TROCHOIDAL]

    ap, ap_ref = service._calculate_ap(sample_tool_6mm, operation, SurfaceQuality.STANDARD)

    assert ap_ref == "LCF"
    # ap = 25mm * 0.50 = 12.5mm
    assert ap == pytest.approx(12.5, rel=0.01)


def test_ap_dynamic_short_tool(sample_tool_30mm):
    """Short tools (L/D < 1.0) with dynamic operations should use DC"""
    service = CalculationService()
    from backend.models.constants import OPERATIONS_MAP

    # L/D = 8/30 = 0.27 < 1.0 → should use DC
    operation = OPERATIONS_MAP[OperationType.SLOT_ROUGH]

    ap, ap_ref = service._calculate_ap(
        sample_tool_30mm, operation, SurfaceQuality.STANDARD
    )

    assert ap_ref == "DC"


def test_ap_dynamic_long_tool(sample_tool_6mm):
    """Long tools (L/D >= 1.0) with dynamic operations should use LCF"""
    service = CalculationService()
    from backend.models.constants import OPERATIONS_MAP

    # L/D = 25/6 = 4.17 >= 1.0 → should use LCF
    operation = OPERATIONS_MAP[OperationType.SLOT_ROUGH]

    ap, ap_ref = service._calculate_ap(sample_tool_6mm, operation, SurfaceQuality.STANDARD)

    assert ap_ref == "LCF"


def test_surface_quality_finishing_reduces_ae(sample_tool_30mm):
    """Finishing quality should reduce ae by 30%"""
    service = CalculationService()
    from backend.models.constants import OPERATIONS_MAP

    operation = OPERATIONS_MAP[OperationType.FACE_ROUGH]

    ae_standard = service._calculate_ae(
        sample_tool_30mm, operation, SurfaceQuality.STANDARD
    )
    ae_finishing = service._calculate_ae(
        sample_tool_30mm, operation, SurfaceQuality.FINISHING
    )

    # Finishing applies 0.7 factor (30% reduction)
    assert ae_finishing == pytest.approx(ae_standard * 0.7, rel=0.01)
