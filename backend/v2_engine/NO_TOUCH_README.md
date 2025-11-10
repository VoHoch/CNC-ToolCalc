# V2.0 Calculation Engine - NO-TOUCH ZONE

**⚠️ WARNING: DO NOT MODIFY THIS CODE ⚠️**

This directory contains the **V2.0 Calculation Engine** from the proven "Last Known Good" implementation.

## NO-TOUCH Principle

**NEVER modify any code in this directory!**

All V4.0 features MUST be implemented via:
- Wrapper services in `backend/services/`
- Additional logic layers
- API transformations

## Why NO-TOUCH?

The V2.0 engine is:
- Battle-tested and proven
- 100% spec-compliant
- Known-good baseline

V3.x failures were caused by modifying the calculation engine directly.

## Architecture Pattern

```
┌─────────────────────────────────────────────┐
│         FastAPI REST API                     │
│         (backend/api/)                       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         Service Layer                        │
│         (backend/services/)                  │
│  - V2Wrapper (calls v2_engine)              │
│  - CoatingService (adds coating logic)      │
│  - SurfaceQualityService (adds quality)     │
│  - ValidationService (8-checks)             │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│    V2.0 Engine (READ-ONLY!)                 │
│    backend/v2_engine/cnc_calculator/        │
│    ⚠️  NO MODIFICATIONS ALLOWED  ⚠️         │
└─────────────────────────────────────────────┘
```

## V2.0 Engine API Surface

### Core Functions

```python
from backend.v2_engine.cnc_calculator import calculate_parameters

# Call V2.0 engine (read-only!)
result = calculate_parameters(
    tool_diameter=6.0,
    tool_length=25.0,
    material="Aluminium",
    operation="FACE_FINISH",
    # ... other params
)

# result contains: vc, n, fz, vf, ae, ap, etc.
```

### What V2.0 Provides

- ✅ Cutting speed (vc) baseline
- ✅ Spindle speed (n)
- ✅ Chip load (fz) baseline
- ✅ Feed rate (vf)
- ✅ Engagement (ae, ap) baseline
- ✅ Power calculation
- ✅ Torque calculation

### What V4.0 Adds (via Wrappers)

- ✨ Tool Coating factors (multiply vc by 1.4-2.2)
- ✨ Surface Quality adjustments (reduce ae/ap)
- ✨ Dry machining corrections (reduce fz)
- ✨ L/D stability warnings
- ✨ Chip temperature analysis
- ✨ Chip formation prediction
- ✨ 8-Checks validation
- ✨ Expert Mode overrides

## Modification Protocol

If you believe the V2.0 engine needs changes:

1. **STOP!** Do not modify.
2. Document the issue in `/docs/issues/V2_ENGINE_ISSUE_<DATE>.md`
3. Escalate to Governance Agent
4. Discuss alternative wrapper approaches
5. Only after consensus and architectural review may V2.0 be touched

## Integrity Check

```bash
# Verify V2.0 engine hasn't been modified
git log backend/v2_engine/

# Should show only initial copy commit
```

## Testing V2.0 Engine

You may test the V2.0 engine in **read-only mode**:

```python
# backend/tests/test_v2_engine_integrity.py
import pytest
from backend.v2_engine.cnc_calculator import calculate_parameters

def test_v2_engine_baseline():
    """Test V2.0 engine returns expected baseline results."""
    result = calculate_parameters(
        tool_diameter=6.0,
        tool_length=25.0,
        material="Aluminium",
        operation="FACE_FINISH"
    )

    # Assert baseline values are as expected
    assert result['vc'] > 0
    assert result['n'] > 0
    # ... more assertions
```

---

**Remember:** This engine is the **foundation**. All V4.0 features build ON TOP, never INSIDE.

**Last Updated:** 2025-11-10
**Status:** ✅ PROTECTED - DO NOT MODIFY
