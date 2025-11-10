"""
Pytest Configuration and Fixtures
"""

import pytest
from backend.models.schemas import Tool, ToolGeometry, MaterialType, OperationType


@pytest.fixture
def sample_tool_30mm():
    """Sample 30mm end mill (short tool, L/D < 1.0)"""
    return Tool(
        id="T1",
        name="30mm Flat End Mill",
        type="flat_end_mill",
        geometry=ToolGeometry(
            DC=30.0,
            LCF=8.0,
            NOF=3,
            DCON=30.0,
            OAL=100.0,
            SFDM=30.0,
        ),
    )


@pytest.fixture
def sample_tool_6mm():
    """Sample 6mm end mill (long tool, L/D > 4.0)"""
    return Tool(
        id="T2",
        name="6mm Flat End Mill",
        type="flat_end_mill",
        geometry=ToolGeometry(
            DC=6.0,
            LCF=25.0,
            NOF=2,
            DCON=6.0,
            OAL=75.0,
            SFDM=6.0,
        ),
    )
