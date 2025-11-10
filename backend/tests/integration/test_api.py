"""
Integration Tests - API Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_health_endpoint():
    """Test /health endpoint"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.0.1-alpha"
    assert "timestamp" in data


def test_get_materials():
    """Test /api/materials endpoint"""
    response = client.get("/api/materials")

    assert response.status_code == 200
    data = response.json()
    assert "materials" in data
    assert len(data["materials"]) == 8  # 8 materials (including copper)

    # Check first material (softwood)
    softwood = data["materials"][0]
    assert softwood["id"] == "softwood"
    assert softwood["hardness_order"] == 1
    assert "color" in softwood


def test_get_operations():
    """Test /api/operations endpoint"""
    response = client.get("/api/operations")

    assert response.status_code == 200
    data = response.json()
    assert "operations" in data

    # Check we have 4 categories
    categories = [group["group"] for group in data["operations"]]
    assert "FACE" in categories
    assert "SLOT" in categories
    assert "GEOMETRY" in categories
    assert "SPECIAL" in categories


def test_create_tool():
    """Test POST /api/tools endpoint"""
    tool_data = {
        "id": "T1",
        "name": "30mm Flat End Mill",
        "type": "flat_end_mill",
        "geometry": {
            "DC": 30.0,
            "LCF": 8.0,
            "NOF": 3,
            "DCON": 30.0,
            "OAL": 100.0,
            "SFDM": 30.0,
        },
    }

    response = client.post("/api/tools", json=tool_data)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Tool T1 registered"


def test_get_tool():
    """Test GET /api/tools/{tool_id} endpoint"""
    # First create a tool
    tool_data = {
        "id": "T2",
        "name": "6mm End Mill",
        "type": "flat_end_mill",
        "geometry": {
            "DC": 6.0,
            "LCF": 25.0,
            "NOF": 2,
            "DCON": 6.0,
            "OAL": 75.0,
            "SFDM": 6.0,
        },
    }
    client.post("/api/tools", json=tool_data)

    # Now get it
    response = client.get("/api/tools/T2")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "T2"
    assert data["geometry"]["DC"] == 6.0


def test_calculate_endpoint():
    """Test POST /api/calculate endpoint (full workflow)"""
    # First create a tool
    tool_data = {
        "id": "T3",
        "name": "30mm Test Tool",
        "type": "flat_end_mill",
        "geometry": {
            "DC": 30.0,
            "LCF": 8.0,
            "NOF": 3,
            "DCON": 30.0,
            "OAL": 100.0,
            "SFDM": 30.0,
        },
    }
    client.post("/api/tools", json=tool_data)

    # Now calculate
    calc_request = {
        "tool_id": "T3",
        "material": "aluminium",
        "operation": "face_rough",
        "coating": "tin",
        "surface_quality": "standard",
        "coolant": "wet",
    }

    response = client.post("/api/calculate", json=calc_request)

    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "calculation_id" in data
    assert "timestamp" in data
    assert "results" in data
    assert "validation" in data
    assert "warnings" in data

    # Check results
    results = data["results"]
    assert results["vc_base"] == 377  # Aluminium base vc
    assert results["coating_factor"] == 1.4  # TiN coating
    assert results["vc_final"] == pytest.approx(377 * 1.4, rel=0.01)
    assert results["n_rpm"] > 0
    assert results["vf_mm_min"] > 0
    assert results["ae_mm"] > 0
    assert results["ap_mm"] > 0

    # Check validation
    assert "all_passed" in data["validation"]
    assert "checks" in data["validation"]
    assert len(data["validation"]["checks"]) == 8  # 8 checks


def test_calculate_tool_not_found():
    """Test calculate with non-existent tool"""
    calc_request = {
        "tool_id": "DOES_NOT_EXIST",
        "material": "aluminium",
        "operation": "face_rough",
    }

    response = client.post("/api/calculate", json=calc_request)

    assert response.status_code == 404


def test_calculate_diamond_coating_on_steel_should_fail():
    """Test that diamond coating on steel is rejected"""
    # Create tool
    tool_data = {
        "id": "T4",
        "name": "Test Tool",
        "type": "flat_end_mill",
        "geometry": {
            "DC": 10.0,
            "LCF": 15.0,
            "NOF": 2,
            "DCON": 10.0,
            "OAL": 50.0,
            "SFDM": 10.0,
        },
    }
    client.post("/api/tools", json=tool_data)

    # Try diamond on steel
    calc_request = {
        "tool_id": "T4",
        "material": "steel_mild",
        "operation": "face_rough",
        "coating": "diamond",
    }

    response = client.post("/api/calculate", json=calc_request)

    assert response.status_code == 400
    assert "non-ferrous" in response.json()["detail"]
