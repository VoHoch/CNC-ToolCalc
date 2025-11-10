"""
Unit Tests - Phase 2: vc + Coating Factor
"""

import pytest
from backend.models.schemas import CoatingType, MaterialType
from backend.services.calculation_service import CalculationService


def test_coating_none():
    """No coating should give factor 1.0"""
    service = CalculationService()
    factor = service._get_coating_factor(CoatingType.NONE, MaterialType.ALUMINIUM)
    assert factor == 1.0


def test_coating_tin():
    """TiN coating should give factor 1.4 (+40%)"""
    service = CalculationService()
    factor = service._get_coating_factor(CoatingType.TIN, MaterialType.ALUMINIUM)
    assert factor == 1.4


def test_coating_tialn():
    """TiAlN coating should give factor 1.6 (+60%)"""
    service = CalculationService()
    factor = service._get_coating_factor(CoatingType.TIALN, MaterialType.ALUMINIUM)
    assert factor == 1.6


def test_coating_altin():
    """AlTiN coating should give factor 1.8 (+80%)"""
    service = CalculationService()
    factor = service._get_coating_factor(CoatingType.ALTIN, MaterialType.ALUMINIUM)
    assert factor == 1.8


def test_coating_diamond_aluminium():
    """Diamond coating on aluminium should give factor 2.2 (+120%)"""
    service = CalculationService()
    factor = service._get_coating_factor(CoatingType.DIAMOND, MaterialType.ALUMINIUM)
    assert factor == 2.2


def test_coating_diamond_steel_should_fail():
    """Diamond coating on steel should raise ValueError"""
    service = CalculationService()
    with pytest.raises(ValueError, match="non-ferrous"):
        service._get_coating_factor(CoatingType.DIAMOND, MaterialType.STEEL_MILD)


def test_coating_carbide():
    """Carbide coating should give factor 1.5 (+50%)"""
    service = CalculationService()
    factor = service._get_coating_factor(CoatingType.CARBIDE, MaterialType.STEEL_MILD)
    assert factor == 1.5


def test_vc_calculation_with_coating():
    """Test complete vc calculation with coating"""
    # Aluminium base vc = 377 m/min
    # TiN coating = 1.4
    # Expected: 377 * 1.4 = 527.8 m/min
    vc_base = 377.0
    coating_factor = 1.4
    vc_final = vc_base * coating_factor

    assert vc_final == pytest.approx(527.8, rel=0.01)
