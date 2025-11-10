"""
Unit Tests - Validation Service (8 Checks)
"""

import pytest
from backend.services.validation_service import ValidationService


def test_rpm_within_limit_pass():
    """RPM within limit (30000) should pass"""
    service = ValidationService()
    check = service._check_rpm_within_limit(25000)

    assert check.passed is True
    assert check.severity == "info"


def test_rpm_within_limit_fail():
    """RPM exceeding limit should fail"""
    service = ValidationService()
    check = service._check_rpm_within_limit(35000)

    assert check.passed is False
    assert check.severity == "error"


def test_power_available_pass():
    """Power within limit (0.7 kW) should pass"""
    service = ValidationService()
    check = service._check_power_available(0.5)

    assert check.passed is True
    assert check.severity == "info"


def test_power_available_fail():
    """Power exceeding limit should fail with warning"""
    service = ValidationService()
    check = service._check_power_available(1.2)

    assert check.passed is False
    assert check.severity == "warning"


def test_feed_rate_reasonable_pass():
    """Feed rate 10-5000 mm/min should pass"""
    service = ValidationService()
    check = service._check_feed_rate_reasonable(1000.0)

    assert check.passed is True


def test_feed_rate_too_low():
    """Feed rate < 10 mm/min should fail"""
    service = ValidationService()
    check = service._check_feed_rate_reasonable(5.0)

    assert check.passed is False


def test_feed_rate_too_high():
    """Feed rate > 5000 mm/min should fail"""
    service = ValidationService()
    check = service._check_feed_rate_reasonable(6000.0)

    assert check.passed is False


def test_ld_ratio_stable():
    """L/D ratio < 4.0 should pass"""
    service = ValidationService()
    check = service._check_ld_ratio_stability(3.5)

    assert check.passed is True
    assert check.severity == "info"


def test_ld_ratio_long_tool():
    """L/D ratio > 4.0 should give warning"""
    service = ValidationService()
    check = service._check_ld_ratio_stability(5.0)

    assert check.passed is False
    assert check.severity == "warning"


def test_ld_ratio_very_long_tool():
    """L/D ratio > 6.0 should give error"""
    service = ValidationService()
    check = service._check_ld_ratio_stability(7.0)

    assert check.passed is False
    assert check.severity == "error"


def test_surface_quality_achievable():
    """ae >= 0.5mm should pass"""
    service = ValidationService()
    check = service._check_surface_quality_achievable(1.0)

    assert check.passed is True


def test_surface_quality_not_achievable():
    """ae < 0.5mm should fail"""
    service = ValidationService()
    check = service._check_surface_quality_achievable(0.3)

    assert check.passed is False


def test_tool_engagement_safe():
    """ap <= DC should pass"""
    service = ValidationService()
    check = service._check_tool_engagement_safe(ap=7.5, dc=30.0)

    assert check.passed is True


def test_tool_engagement_unsafe():
    """ap > DC should fail"""
    service = ValidationService()
    check = service._check_tool_engagement_safe(ap=35.0, dc=30.0)

    assert check.passed is False


def test_temperature_safe():
    """Temperature <= 700°C should pass"""
    service = ValidationService()
    check = service._check_temperature_safe(500.0)

    assert check.passed is True


def test_temperature_unsafe():
    """Temperature > 700°C should fail"""
    service = ValidationService()
    check = service._check_temperature_safe(750.0)

    assert check.passed is False
