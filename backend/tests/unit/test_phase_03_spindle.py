"""
Unit Tests - Phase 3: Spindle Speed (n)
"""

import math
import pytest
from backend.services.calculation_service import CalculationService


def test_spindle_speed_calculation():
    """Test spindle speed formula: n = (vc × 1000) / (π × DC)"""
    service = CalculationService()

    # Example: vc=377 m/min, DC=30mm
    # n = (377 * 1000) / (π * 30)
    # n = 377000 / 94.25
    # n ≈ 4000 RPM

    vc = 377.0
    dc = 30.0

    n = service._calculate_spindle_speed(vc, dc)

    expected = (377 * 1000) / (math.pi * 30)
    assert n == pytest.approx(expected, rel=0.01)
    assert n == pytest.approx(4000, abs=10)


def test_spindle_speed_small_tool():
    """Test spindle speed for small tool (6mm)"""
    service = CalculationService()

    # vc=377 m/min, DC=6mm
    # n = (377 * 1000) / (π * 6)
    # n ≈ 20000 RPM

    vc = 377.0
    dc = 6.0

    n = service._calculate_spindle_speed(vc, dc)

    assert n > 15000
    assert n < 25000


def test_spindle_speed_returns_integer():
    """Spindle speed should be returned as integer RPM"""
    service = CalculationService()

    n = service._calculate_spindle_speed(100.0, 10.0)

    assert isinstance(n, int)
