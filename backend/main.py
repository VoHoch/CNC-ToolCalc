"""
CNC-ToolCalc Backend - FastAPI Application
Version: 0.0.1-alpha
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid

from backend.models.schemas import (
    CalculationRequest,
    CalculationResponse,
    Tool,
    ToolGeometry,
)
from backend.models.constants import MATERIALS, OPERATIONS
from backend.services.calculation_service import CalculationService
from backend.services.validation_service import ValidationService


app = FastAPI(
    title="CNC-ToolCalc API",
    version="0.0.1-alpha",
    description="10-Phase CNC Calculation Engine",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
calculation_service = CalculationService()
validation_service = ValidationService()

# In-memory tool storage (replace with DB later if needed)
TOOLS_DB = {}


# ============================================================================
# ENDPOINTS
# ============================================================================


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "0.0.1-alpha",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/materials")
def get_materials():
    """Get all materials (7 materials, hardness-sorted)"""
    return {
        "materials": [
            {
                "id": m.id.value,
                "name": m.name,
                "hardness_order": m.hardness_order,
                "color": m.color,
                "category": m.category,
            }
            for m in MATERIALS
        ]
    }


@app.get("/api/operations")
def get_operations():
    """Get all operations (13 operations)"""
    operations_by_category = {}

    for op in OPERATIONS:
        if op.category not in operations_by_category:
            operations_by_category[op.category] = []

        operations_by_category[op.category].append({
            "id": op.id.value,
            "name": op.name,
            "description": op.description,
            "icon": op.icon,
            "color": op.color,
        })

    return {
        "operations": [
            {"group": category, "operations": ops}
            for category, ops in operations_by_category.items()
        ]
    }


@app.post("/api/tools")
def create_tool(tool: Tool):
    """Create/register a tool"""
    TOOLS_DB[tool.id] = tool
    return {"message": f"Tool {tool.id} registered", "tool": tool}


@app.get("/api/tools/{tool_id}")
def get_tool(tool_id: str):
    """Get a specific tool"""
    if tool_id not in TOOLS_DB:
        raise HTTPException(status_code=404, detail=f"Tool {tool_id} not found")
    return TOOLS_DB[tool_id]


@app.get("/api/tools")
def get_all_tools():
    """Get all registered tools"""
    return {"tools": list(TOOLS_DB.values())}


@app.post("/api/calculate")
def calculate(request: CalculationRequest) -> CalculationResponse:
    """
    Main calculation endpoint

    Executes 10-phase calculation:
    1. Input Parameters
    2. vc + Coating Factor
    3. Spindle Speed (n)
    4. Chip Load (fz) + Dry Correction
    5. Feed Rate (vf)
    6. Engagement (ae, ap) + Surface Quality
    7. Power & Torque
    8. Thermal Analysis
    9. Chip Formation
    10. L/D Stability
    """

    try:
        # Get tool
        if request.tool_id not in TOOLS_DB:
            raise HTTPException(
                status_code=404, detail=f"Tool {request.tool_id} not found"
            )

        tool = TOOLS_DB[request.tool_id]

        # Execute calculation
        results = calculation_service.calculate(request, tool)

        # Validate results
        validation = validation_service.validate(results)

        # Generate warnings
        warnings = results.stability_warnings.copy()

        if not validation.all_passed:
            for check in validation.checks:
                if not check.passed and check.severity in ["warning", "error"]:
                    warnings.append(f"{check.name}: {check.message}")

        # Return response
        return CalculationResponse(
            calculation_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            results=results,
            validation=validation,
            warnings=warnings,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": {"code": "CALCULATION_ERROR", "message": str(e)}},
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
