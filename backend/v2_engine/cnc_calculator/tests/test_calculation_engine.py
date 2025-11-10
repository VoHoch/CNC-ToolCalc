"""Tests for calculation engine."""

import pytest
from pathlib import Path
from cnc_calculator.core.config_loader import ConfigLoader
from cnc_calculator.core.calculation_engine import CalculationEngine
from cnc_calculator.models import Tool, Geometry, Holder, PostProcess, ToolType


@pytest.fixture
def config_dir():
    """Get config directory."""
    return Path(__file__).parent.parent / "config"


@pytest.fixture
def config_loader(config_dir):
    """Create config loader."""
    return ConfigLoader(config_dir)


@pytest.fixture
def calc_engine(config_loader):
    """Create calculation engine."""
    return CalculationEngine(config_loader)


@pytest.fixture
def test_tool():
    """Create a test tool."""
    geometry = Geometry(
        DC=6.0, DCX=6.0, NOF=2, LCF=20.0, shoulder_diameter=6.0, shoulder_length=20.0
    )
    holder = Holder()
    post_process = PostProcess(number=1)

    return Tool(
        tool_id="T1",
        number=1,
        description="Test 6mm 2-Flute End Mill",
        type=ToolType.FLAT_END_MILL,
        geometry=geometry,
        holder=holder,
        post_process=post_process,
    )


def test_rpm_calculation(calc_engine):
    """Test RPM calculation."""
    # Formula: n = (vc × 1000) / (π × D)
    # Example: vc=150, D=6 → n ≈ 7958
    n = calc_engine.base_calc.calculate_rpm(vc=150, diameter=6)
    assert 7900 < n < 8000


def test_diameter_scaling(calc_engine):
    """Test diameter scaling of feed per tooth."""
    # fz = fz_base × (D/6)^exp
    # Example: fz_base=0.05, D=12, exp=0.35
    fz = calc_engine.base_calc.scale_fz_by_diameter(
        fz_base=0.05, exponent=0.35, diameter=12
    )
    expected = 0.05 * (12 / 6) ** 0.35
    assert abs(fz - expected) < 0.001


def test_full_calculation_workflow(calc_engine, test_tool):
    """Test complete preset calculation."""
    preset = calc_engine.calculate_preset(
        tool=test_tool, material_id="Alu", operation_id="Schlicht(F)"
    )

    # Basic assertions
    assert preset is not None
    assert preset.n_rpm >= 2000
    assert preset.n_rpm <= 24000
    assert preset.vf_mm_per_min > 0
    assert preset.ae_mm > 0
    assert preset.ap_mm > 0
    assert preset.ap_mm <= test_tool.geometry.LCF  # CRITICAL: ap ≤ LCF

    # Expression validation
    assert len(preset.expressions) == 13
    assert "tool_surfaceSpeed" in preset.expressions
    assert "tool_feedPerTooth" in preset.expressions
    assert "tool_stepdown" in preset.expressions
    assert "tool_stepover" in preset.expressions

    # Validate all expressions present
    missing = preset.validate_expressions()
    assert len(missing) == 0


def test_lcd_adjustment(calc_engine):
    """Test L/D ratio adjustments."""
    # L/D = 3.0 → no adjustment
    adj = calc_engine.lcd_rules.get_adjustment(3.0)
    assert adj.fz_factor == 1.0

    # L/D = 5.0 → 10% reduction
    adj = calc_engine.lcd_rules.get_adjustment(5.0)
    assert adj.fz_factor == 0.9

    # L/D = 7.0 → 20% reduction
    adj = calc_engine.lcd_rules.get_adjustment(7.0)
    assert adj.fz_factor == 0.8


def test_low_rpm_compensation(calc_engine):
    """Test low RPM compensation."""
    # Above threshold → no compensation
    factor = calc_engine.low_rpm_rules.get_fz_adjustment(5000)
    assert factor == 1.0

    # Below threshold → compensation
    factor = calc_engine.low_rpm_rules.get_fz_adjustment(4000)
    assert factor == 0.9


def test_multiple_materials(calc_engine, test_tool):
    """Test calculation across multiple materials."""
    materials = ["Alu", "HolzW", "Brass"]

    for material_id in materials:
        preset = calc_engine.calculate_preset(
            tool=test_tool, material_id=material_id, operation_id="Schruppen"
        )

        assert preset is not None
        assert preset.material == material_id
        assert len(preset.expressions) == 13


def test_expression_completeness(calc_engine):
    """Test that all 13 expressions are generated."""
    from cnc_calculator.models.operation import FeedFactors

    expr = calc_engine.expr_builder.build_expressions(
        vc=377,
        fz=0.09,
        ae=7.5,
        ap=1.5,
        DC=30,
        LCF=8,
        feed_factors=FeedFactors(),
    )

    required_keys = [
        "tool_surfaceSpeed",
        "tool_feedPerTooth",
        "tool_feedEntry",
        "tool_feedExit",
        "tool_feedPlunge",
        "tool_feedRamp",
        "tool_feedTransition",
        "tool_rampSpindleSpeed",
        "tool_stepdown",
        "tool_stepover",
        "tool_coolant",
        "use_tool_stepdown",
        "use_tool_stepover",
    ]

    for key in required_keys:
        assert key in expr, f"Missing expression: {key}"

    assert expr["tool_surfaceSpeed"] == "377.0 mpm"
    assert expr["tool_feedPerTooth"] == "0.090 mm"
