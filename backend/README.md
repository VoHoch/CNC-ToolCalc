# CNC-ToolCalc Backend

**Version:** 0.0.1-alpha
**Status:** ✅ Phase 1 Complete
**Architecture:** V4 Final Consolidated (100% Cleanroom)
**Implementation:** NO V2.0 dependencies

---

## Overview

FastAPI-based REST API implementing a 10-phase CNC machining calculation engine.

### Key Features

✅ **10-Phase Calculation Workflow**
- Phase 1: Input Parameters (validation)
- Phase 2: vc + Coating Factor (6 coating types)
- Phase 3: Spindle Speed (n = vc×1000 / π×DC)
- Phase 4: Chip Load (fz) + Dry Machining Correction
- Phase 5: Feed Rate (vf, vf_entry, vf_ramp, vf_plunge)
- Phase 6: Engagement (ae/ap with dynamic reference logic)
- Phase 7: Power & Torque (MRR, kW, Nm)
- Phase 8: Thermal Analysis (chip temperature prediction)
- Phase 9: Chip Formation Prediction
- Phase 10: L/D Stability Check + Warnings

✅ **8-Checks Validation System**
1. RPM within spindle limit (≤ 30000)
2. Power available (≤ 0.7 kW for Makita RT0700C)
3. Feed rate reasonable (10-5000 mm/min)
4. Coating valid for material
5. L/D ratio stability
6. Surface quality achievable
7. Tool engagement safe
8. Temperature safe (≤ 700°C)

✅ **Rich Material/Operation Support**
- **8 Materials** (hardness-sorted): Softwood, Hardwood, Acrylic, Aluminium, Brass, Copper, Steel (Mild), Steel (Stainless)
- **13 Operations**: FACE (2), SLOT (4 incl. Trochoidal), GEOMETRY (3), SPECIAL (3)
- **6 Coatings**: None, TiN (+40%), TiAlN (+60%), AlTiN (+80%), Diamond (+120%), Carbide (+50%)
- **4 Surface Quality Levels**: Roughing, Standard, Finishing, High Finish

---

## Installation

### Requirements

- Python 3.11+ (3.12 recommended)
- pip

### Setup

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Server

### Development Server

```bash
# Start with uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m backend.main
```

Server will be available at: http://localhost:8000

### API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## API Endpoints

### Health Check

```bash
GET /health

Response:
{
  "status": "ok",
  "version": "0.0.1-alpha",
  "timestamp": "2025-11-10T10:30:00"
}
```

### Get Materials

```bash
GET /api/materials

Response:
{
  "materials": [
    {
      "id": "softwood",
      "name": "Softwood (Weichholz)",
      "hardness_order": 1,
      "color": "#f4e4c1",
      "category": "wood"
    },
    ...
  ]
}
```

### Get Operations

```bash
GET /api/operations

Response:
{
  "operations": [
    {
      "group": "FACE",
      "operations": [
        {
          "id": "face_rough",
          "name": "Face Milling (Roughing)",
          "description": "Schruppen von großen Flächen",
          "icon": "⬜",
          "color": "#fb923c"
        },
        ...
      ]
    },
    ...
  ]
}
```

### Register Tool

```bash
POST /api/tools

Body:
{
  "id": "T1",
  "name": "30mm Flat End Mill",
  "type": "flat_end_mill",
  "geometry": {
    "DC": 30.0,
    "LCF": 8.0,
    "NOF": 3,
    "DCON": 30.0,
    "OAL": 100.0,
    "SFDM": 30.0
  }
}
```

### Calculate (Main Endpoint)

```bash
POST /api/calculate

Body:
{
  "tool_id": "T1",
  "material": "aluminium",
  "operation": "face_rough",
  "coating": "tin",              // optional, default: "none"
  "surface_quality": "standard",  // optional, default: "standard"
  "coolant": "wet"               // optional, default: "wet"
}

Response:
{
  "calculation_id": "uuid",
  "timestamp": "2025-11-10T10:30:00",
  "results": {
    "tool": {...},
    "material": "aluminium",
    "operation": "face_rough",
    "vc_base": 377.0,
    "coating_factor": 1.4,
    "vc_final": 527.8,
    "n_rpm": 5605,
    "fz_base": 0.0437,
    "dry_factor": 1.0,
    "fz_final": 0.0437,
    "vf_mm_min": 735.0,
    "vf_entry": 367.5,
    "vf_ramp": 367.5,
    "vf_plunge": 245.0,
    "ae_mm": 7.5,
    "ap_mm": 7.5,
    "ap_reference": "DC",
    "mrr": 41.3,
    "power_kw": 0.165,
    "torque_nm": 0.28,
    "chip_temperature_c": 224.4,
    "chip_formation": "segmented",
    "ld_ratio": 0.27,
    "ld_classification": "SHORT",
    "stability_warnings": []
  },
  "validation": {
    "all_passed": true,
    "checks": [...]
  },
  "warnings": []
}
```

---

## Architecture

### Directory Structure

```
backend/
├── main.py                     # FastAPI app entry point
├── requirements.txt            # Python dependencies
├── models/
│   ├── schemas.py             # Pydantic models (Tool, Material, etc.)
│   └── constants.py           # Material/Operation constants
├── services/
│   ├── calculation_service.py # 10-Phase calculation logic
│   └── validation_service.py  # 8-Checks validation
├── api/
│   └── routes/                # (future: endpoint modules)
└── tests/
    ├── conftest.py            # Pytest fixtures
    ├── unit/                  # Unit tests
    │   ├── test_phase_02_coating.py
    │   ├── test_phase_03_spindle.py
    │   ├── test_phase_06_engagement.py
    │   └── test_validation.py
    └── integration/           # API integration tests
        └── test_api.py
```

### Core Services

**CalculationService** (`services/calculation_service.py`)
- Implements 10-phase calculation workflow
- Pure functions for each phase
- Material/operation lookups
- Dynamic ap-reference logic (DC vs LCF based on L/D ratio)

**ValidationService** (`services/validation_service.py`)
- 8 validation checks
- Warning/error severity levels
- Machine limits (Makita RT0700C: 30000 RPM, 0.7 kW)

---

## Testing

### Run Unit Tests

```bash
pytest backend/tests/unit/ -v
```

### Run Integration Tests

```bash
pytest backend/tests/integration/ -v
```

### Run All Tests with Coverage

```bash
pytest backend/tests/ --cov=backend --cov-report=term-missing
```

### Test Coverage Target

- **Unit Tests:** >90% coverage
- **Integration Tests:** All API endpoints

---

## Key Calculations

### Phase 2: Cutting Speed with Coating

```python
vc_final = vc_base × coating_factor

Coating Factors:
- None: 1.0
- TiN: 1.4 (+40%)
- TiAlN: 1.6 (+60%)
- AlTiN: 1.8 (+80%)
- Diamond: 2.2 (+120%, non-ferrous only)
- Carbide: 1.5 (+50%)
```

### Phase 3: Spindle Speed

```python
n [RPM] = (vc [m/min] × 1000) / (π × DC [mm])
```

### Phase 5: Feed Rate

```python
vf [mm/min] = n [RPM] × fz [mm] × NOF

Derived parameters:
- vf_entry = vf × 0.5
- vf_ramp = vf × 0.5
- vf_plunge = vf / NOF
```

### Phase 6: Dynamic ap-Reference Logic

```python
# Operation-specific rules
if operation in [FACE_ROUGH, FACE_FINISH, SLOT_FULL]:
    ap_reference = "DC"
elif operation == SLOT_TROCHOIDAL or SPECIAL_ADAPTIVE:
    ap_reference = "LCF"
else:  # Dynamic based on L/D ratio
    if L/D < 1.0:
        ap_reference = "DC"
    else:
        ap_reference = "LCF"

# Calculate ap
if ap_reference == "DC":
    ap = DC × ap_factor × surface_quality_factor
else:
    ap = LCF × ap_factor × surface_quality_factor
```

### Phase 7: Power & Torque

```python
MRR [cm³/min] = (ae × ap × vf) / 1000

Power [kW] = (kc × ae × ap × vf) / (60 × 1,000,000)

Torque [Nm] = (Power × 9550) / n
```

---

## Material Properties

| Material | kc [N/mm²] | vc_base [m/min] | Dry Factor | Category |
|----------|-----------|----------------|-----------|----------|
| Softwood | 40 | 1000 | 1.0 | wood |
| Hardwood | 80 | 800 | 1.0 | wood |
| Acrylic | 90 | 600 | 0.9 | plastic |
| Aluminium | 600 | 377 | 0.85 | metal |
| Brass | 800 | 200 | 0.9 | metal |
| Copper | 1000 | 150 | 0.85 | metal |
| Steel (Mild) | 1800 | 150 | 0.7 | metal |
| Steel (Stainless) | 2200 | 80 | 0.65 | metal |

---

## Surface Quality Adjustments

| Level | ae Factor | ap Factor | vf Factor |
|-------|-----------|-----------|-----------|
| ROUGHING | 1.0 | 1.0 | 1.2 (+20%) |
| STANDARD | 1.0 | 1.0 | 1.0 |
| FINISHING | 0.7 (-30%) | 0.8 (-20%) | 0.8 (-20%) |
| HIGH_FINISH | 0.5 (-50%) | 0.6 (-40%) | 0.6 (-40%) |

---

## Development

### Code Style

```bash
# Format code
black backend/

# Lint code
ruff check backend/
```

### Adding New Materials

Edit `backend/models/constants.py`:

```python
MATERIALS.append(
    Material(
        id=MaterialType.NEW_MATERIAL,
        name="New Material Name",
        hardness_order=9,
        color="#hexcode",
        category="metal",
        kc=1500,
        vc_base=200,
        dry_factor=0.8,
        max_temp=550,
        k_thermal=3.5
    )
)
```

### Adding New Operations

Edit `backend/models/constants.py`:

```python
OPERATIONS.append(
    Operation(
        id=OperationType.NEW_OP,
        name="New Operation",
        description="Description",
        category="SPECIAL",
        icon="🔧",
        color="#ff0000",
        ae_factor=0.3,
        ap_factor=0.2,
        ap_reference="dynamic"
    )
)
```

---

## Known Limitations

- **Tool Storage:** In-memory only (no database yet)
- **Authentication:** Not implemented
- **Expert Mode:** Not yet implemented (planned)
- **Export Formats:** Fusion 360 / CSV export not yet implemented

---

## Roadmap

- [ ] Add SQLite/PostgreSQL for tool library
- [ ] Implement export endpoints (Fusion 360, CSV)
- [ ] Add Expert Mode (global adjustments, manual overrides)
- [ ] Add preset caching (Redis)
- [ ] Add calculation history
- [ ] Add user authentication

---

## License

Copyright © 2025 Volker Hochgürtel
All rights reserved.

---

**Last Updated:** 2025-11-10
**Implementation:** Backend/Calculation Agent
**Status:** ✅ Phase 1 Complete (1839 lines of code, 20 files)
