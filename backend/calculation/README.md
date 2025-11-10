# V1.0 Calculation Engine - 100% CLEANROOM IMPLEMENTATION

**Status:** NEW - Not based on any previous code
**Architecture:** Implements V4 Architecture Document

---

## Cleanroom Guarantee

This calculation engine is:
- ✅ 100% newly written for V1.0
- ✅ NO dependencies on previous versions (V2.0, V3.x)
- ✅ Implemented directly from architecture specification
- ✅ Zero legacy code

---

## Implementation Source

All algorithms implemented from:
- `/docs/architecture/CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md`
- Part 2: 10-Phase Calculation Workflow
- Mathematical formulas documented in architecture

---

## Validation Strategy

**During Development:**
1. Implement calculation from architecture spec
2. Write unit tests with expected values from spec
3. (Optional) Compare results with V2.0 reference values
4. Iterate until correct

**V2.0 Reference (Optional):**
- V2.0 runs as separate installation in `/Users/nwt/developments/Schnitttdaten/`
- Used ONLY for validation: "Does V1.0 calculate same values?"
- NO code sharing, NO imports, NO dependencies
- After validation complete: V2.0 can be deleted

---

## Module Structure

```
backend/calculation/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── phase_01_input.py          # Phase 1: Input Parameters
│   ├── phase_02_coating.py        # Phase 2: vc + Coating Factor
│   ├── phase_03_spindle.py        # Phase 3: n (RPM)
│   ├── phase_04_chipload.py       # Phase 4: fz + Dry Correction
│   ├── phase_05_feedrate.py       # Phase 5: vf
│   ├── phase_06_engagement.py     # Phase 6: ae/ap + Surface Quality
│   ├── phase_07_ap_reference.py   # Phase 7: Dynamic ap Reference Logic
│   ├── phase_08_power.py          # Phase 8: Power + Torque
│   ├── phase_09_thermal.py        # Phase 9: Chip Temperature
│   └── phase_10_ld_stability.py   # Phase 10: L/D Stability
├── validation/
│   ├── __init__.py
│   ├── eight_checks.py            # 8-Checks Validation System
│   └── spindle_limits.py          # Makita RT0700C Limits
├── materials/
│   ├── __init__.py
│   └── material_properties.py     # 7 Materials (hardness-sorted)
├── operations/
│   ├── __init__.py
│   └── operation_types.py         # 13 Operations (incl. SLOT_TROCHOIDAL)
├── coating/
│   ├── __init__.py
│   └── coating_factors.py         # 6 Coating Types
├── surface/
│   ├── __init__.py
│   └── quality_adjustments.py     # 4 Surface Quality Levels
└── workflow.py                     # Main 10-Phase Workflow Orchestrator
```

---

## Implementation Approach

### Phase-by-Phase Implementation

Each phase implemented as pure function:

```python
# Example: Phase 2 - Coating Factor
def calculate_coating_factor(
    vc_base: float,
    coating: CoatingType
) -> tuple[float, float]:
    """
    Phase 2: Apply coating factor to base cutting speed.

    Implementation from: Architecture Doc Part 2, Phase 2

    Args:
        vc_base: Base cutting speed [m/min]
        coating: Coating type

    Returns:
        (coating_factor, vc_final)
    """
    COATING_FACTORS = {
        CoatingType.NONE: 1.0,
        CoatingType.TIN: 1.4,      # +40%
        CoatingType.TIALN: 1.6,    # +60%
        CoatingType.ALTIN: 1.8,    # +80%
        CoatingType.DIAMOND: 2.2,  # +120%
        CoatingType.CARBIDE: 1.5   # +50%
    }

    factor = COATING_FACTORS[coating]
    vc_final = vc_base * factor

    return (factor, vc_final)
```

### Unit Tests with Architecture Spec Values

```python
# tests/test_phase_02_coating.py
def test_coating_tin_increases_vc_by_40_percent():
    """Test from Architecture Doc: TiN coating adds 40%."""
    vc_base = 100.0  # m/min
    coating = CoatingType.TIN

    factor, vc_final = calculate_coating_factor(vc_base, coating)

    assert factor == 1.4
    assert vc_final == 140.0  # 100 * 1.4
```

---

## NO Legacy Code Policy

**FORBIDDEN:**
- ❌ Importing from V2.0 code
- ❌ Copying V2.0 functions
- ❌ Wrapping V2.0 calls
- ❌ V2.0 dependencies in requirements.txt

**ALLOWED:**
- ✅ Reading V2.0 code to understand algorithm
- ✅ Extracting formulas for documentation
- ✅ Running V2.0 separately for validation comparison

---

## Validation Workflow (Optional V2.0 Comparison)

```bash
# 1. Run V1.0 calculation
curl -X POST http://localhost:8000/api/calculate \
  -d '{"tool_id": "T1", "material": "aluminium", "operation": "FACE_FINISH"}'
# → V1.0 Result: vc=168 m/min

# 2. Run V2.0 calculation (separate installation)
cd /Users/nwt/developments/Schnitttdaten
source venv/bin/activate
python -c "from cnc_calculator import calculate; print(calculate(...))"
# → V2.0 Result: vc=168 m/min

# 3. Compare
# If match → V1.0 validated ✅
# If differ → Debug V1.0 implementation
```

---

## Migration from V2.0 (Conceptual Only)

We are NOT migrating code. We are:
1. **Understanding** V2.0 algorithms by reading code
2. **Documenting** formulas in architecture
3. **Implementing** formulas fresh in V1.0
4. **Validating** V1.0 produces same results

This is **specification extraction**, not code migration.

---

## Production Deployment (V1.0 Only)

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    # NO V2.0 references!
    # Only V1.0 calculation/ modules
```

**Guaranteed:** Production deployment contains ZERO V2.0 code.

---

**Status:** ✅ CLEANROOM READY
**Last Updated:** 2025-11-10
**V2.0 Dependencies:** NONE
**Implementation Progress:** 0% (starting fresh)
