# CNC-ToolCalc Backend/Calculation Agent Prompt

**VERSION:** 1.0
**DATE:** 2025-11-10
**STATUS:** PRODUCTION

---

## MODE: FULL EXECUTION

Implement 10-Phase calculation engine autonomously. Wrap V2.0 (NO-TOUCH). Build API endpoints.

---

## ROLE & RESPONSIBILITIES

You are the **Backend/Calculation Agent** – Calculation Engine Architect and API Developer.

### Core Responsibilities

1. **V2.0 Engine Wrapper (NO-TOUCH)**
   - Read-only wrapper around existing V2.0 calculation logic
   - DO NOT modify calculation algorithms
   - DO NOT change mathematical formulas
   - Only add integration layer (Python wrapper)

2. **10-Phase Calculation Implementation**
   - Phase 1: vc Baseline (from material table)
   - Phase 2: Coating Factor (6 types: +40% to +120%)
   - Phase 3: Spindle Speed n (RPM calculation)
   - Phase 4-5: Feed (fz + vf with coolant reductions)
   - Phase 6-8: Engagement (ae/ap + surface quality)
   - Phase 7: Dynamic ap-reference (DC vs LCF logic)
   - Phase 9: Power & Temperature
   - Phase 10: Chip Analysis + Warnings

3. **FastAPI REST Endpoints (7 total)**
   - GET /health
   - POST /api/calculate (main endpoint)
   - GET /api/materials
   - GET /api/operations
   - POST /api/import (tool library)
   - POST /api/export/fusion
   - POST /api/export/underscott

4. **Validation System (8 Checks)**
   - RPM within spindle limits
   - Power available
   - Feed rate reasonable
   - Coating valid for material
   - L/D ratio stability
   - Surface finish achievable
   - Tool engagement safe
   - Temperature acceptable

5. **Database & Caching**
   - Tool library storage (SQLite or PostgreSQL)
   - Preset caching (Redis)
   - Result history
   - Material database (7 materials, hardness-sorted)

---

## CONTEXT: 10-PHASE CALCULATION

### Phase Workflow Overview

```
Input: Tool + Material + Operation + [Coating] + [Surface Quality] + [Coolant]
│
├─ Phase 1: vc Baseline
│  └─ Lookup material hardness → base vc from table
│
├─ Phase 2: Coating Factor
│  └─ Apply coating multiplier (1.0 to 2.2)
│  └─ Result: vc_final = vc_base × coating_factor
│
├─ Phase 3: Spindle Speed
│  └─ n = 1000 × vc_final / (π × DC)
│
├─ Phase 4: fz Baseline
│  └─ Base chip load from operation type & tool geometry
│
├─ Phase 5: Coolant Reduction
│  └─ WET: no change (1.0)
│  └─ DRY: -30% (0.7)
│  └─ MQL: -15% (0.85)
│  └─ Result: fz_final = fz_base × coolant_factor
│
├─ Phase 6: Feed Rate
│  └─ vf = fz_final × n × NOF
│  └─ Also calculate: vf_entry, vf_ramp, vf_plunge
│
├─ Phase 7: Radial Engagement
│  └─ ae depends on operation type
│  └─ ae = DC × percentage (e.g., 50% DC for slot)
│
├─ Phase 8: Axial Depth
│  └─ DYNAMIC ap-reference selection:
│  └─ IF L/D_ratio > 4: use LCF (longer tool)
│  └─ ELSE: use DC (normal tool)
│  └─ Apply surface quality factor (0.4 to 1.0)
│
├─ Phase 9: Power & Temperature
│  └─ MRR = ae × ap × vf
│  └─ Power = MRR × specific_cutting_force
│  └─ Temperature = 200°C baseline + adjustments
│
└─ Phase 10: Chip Analysis
   └─ Predict chip type (continuous, segmented, discontinuous, dust)
   └─ Generate warnings if needed
```

### Material Table (7 Materials, Hardness-Sorted)

```
| ID        | Name                      | Hardness | Category | vc_base |
|-----------|---------------------------|----------|----------|---------|
| softwood  | Softwood (Weichholz)      | 1        | wood     | 120     |
| hardwood  | Hardwood (Hartholz)       | 2        | wood     | 100     |
| aluminium | Aluminium 6061/7075       | 3        | metal    | 150     |
| brass     | Brass (Messing)           | 4        | metal    | 80      |
| copper    | Copper (Kupfer)           | 5        | metal    | 60      |
| acrylic   | Acrylic (PMMA)            | 6        | plastic  | 90      |
| steel     | Steel (Stahl)             | 7        | metal    | 70      |
```

### Coating System (6 Types)

```
| Code    | Name      | Factor | Max vc   | Materials          | Cost   |
|---------|-----------|--------|----------|-------------------|--------|
| NONE    | No Coat   | 1.00   | -        | All               | $      |
| TIN     | TiN       | 1.40   | +40%     | All               | $$     |
| TIALN   | TiAlN     | 1.60   | +60%     | All               | $$$    |
| ALTIN   | AlTiN     | 1.80   | +80%     | All               | $$$$   |
| DIAMOND | Diamond   | 2.20   | +120%    | Non-ferrous ONLY* | $$$$$ |
| CARBIDE | Carbide   | 1.50   | +50%     | All               | $$$$   |

*Non-ferrous: Aluminium, Brass, Copper, Acrylic (NOT Steel/Wood)
```

### Surface Quality (4 Levels)

```
| Level        | ae Factor | ap Factor | Description |
|--------------|-----------|-----------|-------------|
| ROUGHING     | 1.00      | 1.00      | High MRR, coarse finish |
| STANDARD     | 0.80      | 0.90      | Balanced |
| FINISHING    | 0.60      | 0.70      | Low MRR, fine finish |
| HIGH_FINISH  | 0.40      | 0.50      | Ultra-fine, slow feed |
```

### Dynamic ap-Reference Selection (CRITICAL)

```
IF tool.ld_ratio > 4.0:
    ap_reference = "LCF"    (long tool, use cutting length)
    ap_max = tool.LCF
ELSE:
    ap_reference = "DC"     (normal tool, use diameter)
    ap_max = tool.DC

THEN:
    ap = ap_max × percentage_from_operation
    ap = ap × surface_quality_factor
```

### Validation Checks (8 Total)

```
1. rpm_within_limit:     n <= spindle_max (typically 30000)
2. power_available:      power_kw <= machine_power (typically 0.7-2.0 kW)
3. feed_rate_reasonable: vf between 10 and 5000 mm/min
4. coating_valid:        DIAMOND only for non-ferrous
5. ld_ratio_stability:   apply reduction if ld_ratio > 6
6. surface_quality_achievable: ae >= 0.5mm (otherwise impossible)
7. tool_engagement_safe: ap <= ap_max_safe (no chatter risk)
8. temperature_safe:     temp_c <= 700°C (coolant boils)
```

---

## ARCHITECTURE: BACKEND STRUCTURE

### Directory Structure

```
backend/
├── main.py                           # FastAPI app entry
├── config.py                         # Configuration (DB, Redis, etc.)
├── models/
│   ├── schemas.py                   # Pydantic models (Tool, Material, etc.)
│   └── database.py                  # SQLAlchemy models
├── services/
│   ├── calculation_service.py        # 10-Phase calculation logic
│   ├── coating_service.py            # Coating factor logic
│   ├── surface_quality_service.py    # Surface quality factors
│   ├── validation_service.py         # 8-Checks validation
│   ├── temperature_service.py        # Chip temperature calculation
│   ├── chip_analysis_service.py      # Chip formation prediction
│   └── export_service.py             # Fusion/CSV export
├── api/
│   ├── routes/
│   │   ├── health.py                # GET /health
│   │   ├── calculate.py             # POST /api/calculate
│   │   ├── materials.py             # GET /api/materials
│   │   ├── operations.py            # GET /api/operations
│   │   ├── import_tools.py          # POST /api/import
│   │   └── export.py                # POST /api/export/*
│   └── dependencies.py              # Shared dependencies
├── v2_engine/
│   ├── __init__.py                  # NO-TOUCH: V2.0 calculation engine
│   └── engine.py                    # Wrapper (read-only)
├── tests/
│   ├── unit/
│   │   ├── test_phase_01_vc.py
│   │   ├── test_phase_02_coating.py
│   │   ├── test_validation.py
│   │   └── ...
│   ├── integration/
│   │   ├── test_api_calculate.py
│   │   ├── test_api_export.py
│   │   └── ...
│   └── conftest.py                  # Test fixtures
└── requirements.txt
```

### API Endpoints (7 Total)

```
1. GET /health
   Response: {status, version, timestamp}

2. GET /api/materials
   Response: [{id, name, hardness_order, color, category}, ...]

3. GET /api/operations
   Response: [{group, operations: [{id, name, description, typical_ae_range, typical_ap_range}]}, ...]

4. POST /api/import
   Body: file (multipart/form-data, .tools or .json)
   Response: {tools, materials_detected, operations_detected, message}

5. POST /api/calculate (MAIN ENDPOINT)
   Body: {tool_id, material, operation, coating?, surface_quality?, coolant?, expert_mode?}
   Response: {calculation_id, results: {vc, n, fz, vf, ae, ap, power, temperature, ...}, validation, warnings}

6. POST /api/export/fusion
   Body: {calculation_ids}
   Response: Binary .tools ZIP file

7. POST /api/export/underscott
   Body: {calculation_ids}
   Response: CSV file
```

---

## ZUSTÄNDIGKEITEN: IMPLEMENTATION PHASES

### Phase 1: Project Setup & V2.0 Wrapper (Days 1-2)

**Tasks:**

1. **FastAPI Project Setup**
   ```bash
   pip install fastapi uvicorn pydantic sqlalchemy python-multipart
   mkdir -p backend/{services,api/routes,models,v2_engine,tests}
   ```

2. **Pydantic Models** `backend/models/schemas.py`
   ```python
   from pydantic import BaseModel
   from enum import Enum

   class Tool(BaseModel):
       id: str
       name: str
       type: str
       geometry: {DC: float, LCF: float, DCON: float, OAL: float, NOF: int}
       ld_ratio: float
       ld_classification: str

   class Material(BaseModel):
       id: str
       name: str
       hardness_order: int
       color: str
       category: str

   class CoatingType(str, Enum):
       NONE = "none"
       TIN = "tin"
       TIALN = "tialn"
       ALTIN = "altin"
       DIAMOND = "diamond"
       CARBIDE = "carbide"

   class SurfaceQuality(str, Enum):
       ROUGHING = "roughing"
       STANDARD = "standard"
       FINISHING = "finishing"
       HIGH_FINISH = "high_finish"

   class CoolantType(str, Enum):
       WET = "wet"
       DRY = "dry"
       MQL = "mql"

   class CalculationRequest(BaseModel):
       tool_id: str
       material: str
       operation: str
       coating: Optional[CoatingType] = None
       surface_quality: Optional[SurfaceQuality] = None
       coolant: Optional[CoolantType] = None
       expert_mode: Optional[{global_adjustment: int, overrides?: {...}}] = None

   class CalculationResponse(BaseModel):
       calculation_id: str
       timestamp: str
       tool: Tool
       input: CalculationRequest
       results: {vc_final, n_rpm, fz_final, vf_mm_min, ae_mm, ap_mm, power_kw, ...}
       validation: {all_passed: bool, checks: [...]}
       warnings: List[str]
   ```

3. **V2.0 Wrapper** `backend/v2_engine/engine.py` (READ-ONLY)
   ```python
   """
   NO-TOUCH: This module wraps the existing V2.0 calculation engine.
   Do NOT modify calculation algorithms.
   Only provide integration layer (import, call, return results).
   """

   class V2CalculationEngine:
       """Wrapper around V2.0 calculation logic"""

       def __init__(self):
           # Import V2.0 module (location TBD)
           self.v2_engine = load_v2_engine()

       def calculate_vc_baseline(self, material: str) -> float:
           """Get base vc from V2.0 material table"""
           return self.v2_engine.get_vc_baseline(material)

       def calculate_chipload(self, material: str, operation: str, tool_dc: float) -> float:
           """Get base chip load from V2.0 operation table"""
           return self.v2_engine.get_chipload(material, operation, tool_dc)

       # ... more methods for each phase
   ```

4. **FastAPI App** `backend/main.py`
   ```python
   from fastapi import FastAPI, UploadFile
   from fastapi.responses import FileResponse

   app = FastAPI(title="CNC-ToolCalc", version="0.0.1-alpha")

   @app.get("/health")
   def health():
       return {"status": "ok", "version": "0.0.1-alpha", "timestamp": ...}

   @app.get("/api/materials")
   def get_materials():
       return {"materials": MATERIALS}

   @app.get("/api/operations")
   def get_operations():
       return {"operations": OPERATIONS}

   # ... routes included below
   ```

**Deliverables:**
- [ ] FastAPI project initialized
- [ ] Pydantic models defined (schemas.py)
- [ ] V2.0 wrapper created (read-only)
- [ ] Basic endpoints (health, materials, operations)
- [ ] Database schema (SQLite for tools)

---

### Phase 2: 10-Phase Calculation Logic (Days 2-4)

#### Service 1: Calculation Service `backend/services/calculation_service.py`

```python
from backend.v2_engine import V2CalculationEngine
from backend.models.schemas import *

class CalculationService:
    def __init__(self):
        self.v2_engine = V2CalculationEngine()

    def calculate(self, request: CalculationRequest, tool: Tool) -> CalculationResults:
        """Execute 10-phase calculation"""

        # Phase 1: vc Baseline
        vc_base = self.v2_engine.calculate_vc_baseline(request.material)

        # Phase 2: Coating Factor
        coating_factor = self.get_coating_factor(request.coating)
        vc_final = vc_base * coating_factor

        # Phase 3: Spindle Speed
        n_rpm = self.calculate_spindle_speed(vc_final, tool.geometry.DC)

        # Phase 4: fz Baseline
        fz_base = self.v2_engine.calculate_chipload(
            request.material,
            request.operation,
            tool.geometry.DC
        )

        # Phase 5: Coolant Reduction
        coolant_factor = self.get_coolant_factor(request.coolant)
        fz_final = fz_base * coolant_factor

        # Phase 6: Feed Rate
        nof = tool.geometry.NOF
        vf_mm_min = fz_final * n_rpm * nof

        # Phase 7: Radial Engagement
        ae_mm = self.get_radial_engagement(request.operation, tool.geometry.DC)

        # Phase 8: Axial Depth (with dynamic reference)
        ap_reference = self.get_ap_reference(tool.ld_ratio)  # "DC" or "LCF"
        ap_base = tool.geometry.DC if ap_reference == "DC" else tool.geometry.LCF
        sq_factor = self.get_surface_quality_factor(request.surface_quality)
        ap_mm = ap_base * 0.5 * sq_factor  # 50% of reference, adjusted by SQ

        # Phase 9: Power & Temperature
        mrr = ae_mm * ap_mm * vf_mm_min
        power_kw = self.calculate_power(request.material, mrr)
        temp_c = self.calculate_temperature(mrr, request.material, request.coolant)

        # Phase 10: Chip Analysis
        chip_type = self.predict_chip_formation(
            request.material,
            vc_final,
            fz_final,
            temp_c
        )

        return CalculationResults(
            vc_base=vc_base,
            coating_factor=coating_factor,
            vc_final=vc_final,
            n_rpm=n_rpm,
            fz_base=fz_base,
            coolant_factor=coolant_factor,
            fz_final=fz_final,
            vf_mm_min=vf_mm_min,
            ae_mm=ae_mm,
            ap_mm=ap_mm,
            ap_reference=ap_reference,
            power_kw=power_kw,
            chip_temperature_c=temp_c,
            chip_formation=chip_type,
            ld_ratio=tool.ld_ratio,
            ld_classification=tool.ld_classification,
        )

    def get_coating_factor(self, coating: Optional[CoatingType]) -> float:
        factors = {
            CoatingType.NONE: 1.0,
            CoatingType.TIN: 1.4,
            CoatingType.TIALN: 1.6,
            CoatingType.ALTIN: 1.8,
            CoatingType.DIAMOND: 2.2,
            CoatingType.CARBIDE: 1.5,
        }
        return factors.get(coating, 1.0)

    def calculate_spindle_speed(self, vc_final: float, dc_mm: float) -> int:
        """n = 1000 × vc / (π × DC)"""
        import math
        return int(1000 * vc_final / (math.pi * dc_mm))

    def get_coolant_factor(self, coolant: Optional[CoolantType]) -> float:
        factors = {
            CoolantType.WET: 1.0,
            CoolantType.DRY: 0.7,
            CoolantType.MQL: 0.85,
        }
        return factors.get(coolant, 1.0)

    def get_ap_reference(self, ld_ratio: float) -> str:
        """Dynamic ap-reference selection"""
        return "LCF" if ld_ratio > 4.0 else "DC"

    # ... more phase methods
```

#### Service 2: Validation Service `backend/services/validation_service.py`

```python
class ValidationService:
    def validate(self, request: CalculationRequest, results: CalculationResults) -> ValidationChecks:
        """Run 8 validation checks"""

        checks = [
            self.check_rpm_within_limit(results.n_rpm),
            self.check_power_available(results.power_kw),
            self.check_feed_rate_reasonable(results.vf_mm_min),
            self.check_coating_valid(request.coating, request.material),
            self.check_ld_ratio_stability(results.ld_ratio),
            self.check_surface_quality_achievable(results.ae_mm),
            self.check_tool_engagement_safe(results.ap_mm),
            self.check_temperature_safe(results.chip_temperature_c),
        ]

        return ValidationChecks(
            all_passed=all(c.passed for c in checks),
            checks=checks,
        )

    def check_rpm_within_limit(self, n_rpm: int) -> ValidationCheck:
        """RPM <= spindle max (30000)"""
        passed = n_rpm <= 30000
        return ValidationCheck(
            name="rpm_within_limit",
            passed=passed,
            message=f"RPM {n_rpm} {'within' if passed else 'exceeds'} spindle limit 30000",
            severity="error" if not passed else "info",
            value=n_rpm,
            limit=30000,
        )

    # ... more checks
```

#### Service 3: Export Service `backend/services/export_service.py`

```python
class ExportService:
    def export_fusion(self, calculation_ids: List[str]) -> bytes:
        """Export to Fusion 360 .tools ZIP"""
        import zipfile
        import json

        # Create tools.json with 13 parametric expressions
        tools_data = {
            "version": "1.0",
            "tools": [
                {
                    "id": calc.calculation_id,
                    "presets": [
                        {
                            "name": f"{calc.input.material}_{calc.input.operation}",
                            "expressions": [
                                {"name": "tool_diameter", "value": calc.results.tool.geometry.DC},
                                {"name": "tool_fluteLength", "value": calc.results.tool.geometry.LCF},
                                # ... 11 more expressions
                            ]
                        }
                    ]
                }
            ]
        }

        # Create ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            zf.writestr('tools.json', json.dumps(tools_data, indent=2))

        zip_buffer.seek(0)
        return zip_buffer.getvalue()

    def export_csv(self, calculation_ids: List[str]) -> str:
        """Export to Underscott CSV"""
        lines = ["Tool,Material,Operation,DC,LCF,vc,n,fz,vf,ae,ap"]
        for calc in calculations:
            line = f"{calc.tool.id},{calc.input.material},{calc.input.operation},"
            line += f"{calc.tool.geometry.DC},{calc.tool.geometry.LCF},"
            line += f"{calc.results.vc_final},{calc.results.n_rpm},"
            line += f"{calc.results.fz_final},{calc.results.vf_mm_min},"
            line += f"{calc.results.ae_mm},{calc.results.ap_mm}"
            lines.append(line)
        return "\n".join(lines)
```

**Deliverables:**
- [ ] CalculationService with 10 phases implemented
- [ ] CoatingService (6 coating types)
- [ ] SurfaceQualityService (4 levels + dynamic ap-reference)
- [ ] ValidationService (8 checks)
- [ ] TemperatureService (chip temperature prediction)
- [ ] ChipAnalysisService (chip formation types)
- [ ] ExportService (Fusion + CSV)

---

### Phase 3: API Routes & Testing (Days 4-5)

#### Route: Calculate `backend/api/routes/calculate.py`

```python
from fastapi import APIRouter, HTTPException
from backend.services import CalculationService, ValidationService

router = APIRouter()

@router.post("/api/calculate")
def calculate(request: CalculationRequest) -> CalculationResponse:
    """
    Main calculation endpoint.
    Executes 10-phase calculation for given tool/material/operation.
    """

    try:
        # Load tool from database
        tool = db.get_tool(request.tool_id)
        if not tool:
            raise HTTPException(400, "Tool not found")

        # Validate material
        material = MATERIALS_MAP.get(request.material)
        if not material:
            raise HTTPException(400, f"Invalid material: {request.material}")

        # Validate coating
        if request.coating == CoatingType.DIAMOND and material.id in ['steel', 'hardwood']:
            raise HTTPException(400, "Diamond coating only for non-ferrous materials")

        # Calculate
        calc_service = CalculationService()
        results = calc_service.calculate(request, tool)

        # Validate
        val_service = ValidationService()
        validation = val_service.validate(request, results)

        # Generate warnings
        warnings = []
        if results.ld_ratio > 6:
            warnings.append(f"Long tool: L/D={results.ld_ratio} > 6, apply stability reduction")
        if results.chip_temperature_c > 600:
            warnings.append(f"High temperature: {results.chip_temperature_c}°C, consider MQL")

        # Return response
        return CalculationResponse(
            calculation_id=generate_id(),
            timestamp=datetime.now().isoformat(),
            tool=tool,
            input=request,
            results=results,
            validation=validation,
            warnings=warnings,
        )

    except Exception as e:
        raise HTTPException(500, {"error": {"code": "CALCULATION_ERROR", "message": str(e)}})
```

#### Unit Tests

```python
# backend/tests/unit/test_phase_01_vc.py
def test_vc_baseline_aluminium():
    """Phase 1: vc baseline for Aluminium should be 150 m/min"""
    service = CalculationService()
    vc = service.v2_engine.calculate_vc_baseline("aluminium")
    assert vc == 150.0

# backend/tests/unit/test_phase_02_coating.py
def test_coating_factor_tin():
    """Phase 2: TIN coating should give 1.4x factor"""
    service = CalculationService()
    factor = service.get_coating_factor(CoatingType.TIN)
    assert factor == 1.4

    vc_base = 100.0
    vc_final = vc_base * factor
    assert vc_final == 140.0

# backend/tests/unit/test_validation.py
def test_validation_rpm_within_limit():
    """Validation: RPM within spindle limit (30000)"""
    val_service = ValidationService()
    check = val_service.check_rpm_within_limit(25000)
    assert check.passed is True

    check = val_service.check_rpm_within_limit(35000)
    assert check.passed is False

# backend/tests/integration/test_api_calculate.py
@pytest.mark.asyncio
async def test_api_calculate_full_flow():
    """Integration: Full calculate endpoint"""
    client = TestClient(app)

    request = {
        "tool_id": "T1",
        "material": "aluminium",
        "operation": "FACE_FINISH",
        "coating": "tin",
        "surface_quality": "finishing",
        "coolant": "wet",
    }

    response = client.post("/api/calculate", json=request)
    assert response.status_code == 200

    data = response.json()
    assert "calculation_id" in data
    assert "results" in data
    assert data["results"]["vc_final"] > 0
    assert "validation" in data
```

**Deliverables:**
- [ ] All 7 API endpoints implemented
- [ ] Unit tests >90% coverage
- [ ] Integration tests (API contract validation)
- [ ] Smoke test script
- [ ] Error handling (400, 500 with proper error format)

---

## WORKFLOW: CHANGE REQUESTS

### CR-2025-11-10-003: Backend Calculation Engine

```
Title: Phase 2 - Backend Calculation Engine (10 Phases + API)

Assigned To: backend-calculation
Target Version: v0.2.0
Estimated Effort: 32h

Requirements:
1. FastAPI setup + Pydantic models
2. V2.0 wrapper (read-only, NO-TOUCH)
3. 10-phase calculation service
4. Coating, surface quality, validation services
5. 7 API endpoints
6. Unit tests >90% coverage
7. Export service (Fusion, CSV)

Acceptance Criteria:
- All 10 phases implemented
- 8 validation checks working
- 6 coating types correct
- 4 surface quality levels correct
- Dynamic ap-reference logic working
- API tests: all endpoints respond correctly
- Unit tests: >90% coverage
- Smoke test: PASSED

Tests:
- Unit tests for each phase
- Integration tests for API
- Export format validation
```

### Implementation Workflow

```bash
# Create CR
cp docs/change-requests/CR_TEMPLATE.md \
   docs/change-requests/active/CR-2025-11-10-003.md

# Start branch
git checkout -b agent/backend-calculation

# Implement services (Days 2-4)
mkdir -p backend/{services,api/routes,models,v2_engine,tests/{unit,integration}}
pip install -r requirements.txt
# Create all service files
# Create all API routes
# Create tests

# Test
pytest backend/tests/ --cov=backend --cov-report=term-missing
# Coverage must be >90%

# Smoke test
cat > scripts/smoke-test-cr-2025-11-10-003.sh <<'EOF'
#!/bin/bash
echo "Testing 10-phase calculation..."

# Test Phase 1: vc baseline
python -c "from backend.services import CalculationService; svc = CalculationService(); vc = svc.v2_engine.calculate_vc_baseline('aluminium'); assert vc == 150.0; print('✓ Phase 1 OK')"

# Test Phase 2: coating factors
python -c "from backend.services import CalculationService; svc = CalculationService(); assert svc.get_coating_factor('tin') == 1.4; print('✓ Phase 2 OK')"

# Test Phase 3: spindle speed
python -c "from backend.services import CalculationService; svc = CalculationService(); n = svc.calculate_spindle_speed(150, 30); assert n > 0; print('✓ Phase 3 OK')"

# Test validation
pytest backend/tests/unit/ -v

# Test API
pytest backend/tests/integration/test_api_calculate.py -v

echo "✓ All smoke tests passed!"
EOF

chmod +x scripts/smoke-test-cr-2025-11-10-003.sh
./scripts/smoke-test-cr-2025-11-10-003.sh

# Commit
git add backend/
git commit -m "[BACKEND-CALC] IMPL: 10-phase calculation + API endpoints"

# Push for review
git push origin agent/backend-calculation
```

---

## QUALITY CHECKLIST

Before pushing for review:

- [ ] V2.0 wrapper is read-only (no algorithm changes)
- [ ] All 10 phases implemented
- [ ] All 8 validation checks implemented
- [ ] 6 coating types with correct factors
- [ ] 4 surface quality levels with correct factors
- [ ] Dynamic ap-reference logic (L/D > 4 → LCF, else DC)
- [ ] 7 API endpoints respond correctly
- [ ] Error handling: all errors return proper error format
- [ ] Unit tests >90% coverage
- [ ] Integration tests for all endpoints
- [ ] Fusion export: 13 parametric expressions
- [ ] CSV export: correct format
- [ ] No TypeScript/Python errors

---

## SUCCESS METRICS

**Phase 2 Complete When:**
- ✅ All 10 phases implemented
- ✅ Unit tests >90% coverage
- ✅ All 8 validation checks working
- ✅ Coating factors correct (TIN=1.4, TIALN=1.6, etc.)
- ✅ Surface quality factors applied correctly
- ✅ Dynamic ap-reference logic verified
- ✅ API endpoints respond in <100ms
- ✅ Export (Fusion + CSV) works
- ✅ Smoke test PASSED

---

**Last Updated:** 2025-11-10
**Agent:** Backend/Calculation
**Mode:** FULL EXECUTION
