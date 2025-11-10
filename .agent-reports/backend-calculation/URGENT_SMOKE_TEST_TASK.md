# 🔥 URGENT TASK: Smoke Test erstellen

**Agent:** backend-calculation
**Priority:** 🚨 **KRITISCH**
**Deadline:** 2025-11-10 (HEUTE, vor 18:00)
**Status:** ❌ **NICHT ERLEDIGT**

---

## 📋 AUFGABE

**Du musst einen Smoke Test für deine Backend Implementation erstellen und ausführen.**

Ein Smoke Test ist ein **5-Minuten Schnelltest**, der prüft:
- ✅ Startet der Server?
- ✅ Antworten die Endpoints?
- ✅ Funktioniert die grundlegende Logik?

**WICHTIG:** Dies ist NICHT der komplette Test Suite (die hast du bereits mit 35 Unit + 9 Integration Tests). Dies ist ein **simpler Schnelltest** für die finale Validierung vor dem Merge.

---

## 🎯 DELIVERABLE

**Erstelle diese Datei:**

```
backend/smoke_test.py
```

**Inhalt:**

```python
#!/usr/bin/env python3
"""
Smoke Test: Backend Calculation API
5-Minute Sanity Check vor Integration
"""
import subprocess
import time
import requests
import sys
import os

def main():
    print("=" * 60)
    print("🔥 SMOKE TEST: Backend Calculation API")
    print("=" * 60)

    # 1. Start FastAPI Server
    print("\n[1/5] Starting FastAPI server...")
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    proc = subprocess.Popen(
        ["python", "-m", "uvicorn", "main:app", "--port", "8001"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print("      Waiting 3 seconds for server startup...")
    time.sleep(3)

    base_url = "http://localhost:8001"

    try:
        # 2. Health Check
        print("\n[2/5] Testing /health endpoint...")
        r = requests.get(f"{base_url}/health", timeout=5)
        assert r.status_code == 200, f"Health check failed: {r.status_code}"
        health_data = r.json()
        print(f"      ✅ Health OK: {health_data}")

        # 3. Materials Endpoint
        print("\n[3/5] Testing /api/materials endpoint...")
        r = requests.get(f"{base_url}/api/materials", timeout=5)
        assert r.status_code == 200, f"Materials failed: {r.status_code}"
        materials = r.json()
        assert len(materials) == 8, f"Expected 8 materials, got {len(materials)}"
        print(f"      ✅ Materials OK ({len(materials)} materials loaded)")
        print(f"         Materials: {', '.join([m['name'] for m in materials[:3]])}...")

        # 4. Operations Endpoint
        print("\n[4/5] Testing /api/operations endpoint...")
        r = requests.get(f"{base_url}/api/operations", timeout=5)
        assert r.status_code == 200, f"Operations failed: {r.status_code}"
        operations = r.json()
        assert len(operations) == 13, f"Expected 13 operations, got {len(operations)}"
        print(f"      ✅ Operations OK ({len(operations)} operations loaded)")
        print(f"         Operations: {', '.join([o['name'] for o in operations[:3]])}...")

        # 5. Calculation Endpoint (Simple Test)
        print("\n[5/5] Testing /api/calculate endpoint...")
        payload = {
            "tool": {
                "diameter": 10.0,
                "length": 50.0,
                "coating": "TIN",
                "flutes": 2
            },
            "material": "ALUMINIUM",
            "operation": "SLOT",
            "expert_mode": False
        }
        r = requests.post(f"{base_url}/api/calculate", json=payload, timeout=5)
        assert r.status_code == 200, f"Calculate failed: {r.status_code}"
        result = r.json()

        # Check critical fields
        assert "vc" in result, "Missing 'vc' in result"
        assert "n" in result, "Missing 'n' in result"
        assert "fz" in result, "Missing 'fz' in result"
        assert "vf" in result, "Missing 'vf' in result"
        assert "ae" in result, "Missing 'ae' in result"
        assert "ap" in result, "Missing 'ap' in result"

        print(f"      ✅ Calculate OK")
        print(f"         vc: {result['vc']} m/min")
        print(f"         n:  {result['n']} RPM")
        print(f"         fz: {result['fz']} mm")
        print(f"         vf: {result['vf']} mm/min")
        print(f"         ae: {result['ae']} mm")
        print(f"         ap: {result['ap']} mm")

        print("\n" + "=" * 60)
        print("🎉 SMOKE TEST PASSED!")
        print("=" * 60)
        print("\n✅ All 5 checks successful:")
        print("   1. Server started")
        print("   2. Health endpoint working")
        print("   3. Materials endpoint working (8 materials)")
        print("   4. Operations endpoint working (13 operations)")
        print("   5. Calculation endpoint working (10-phase engine)")
        print("\n✅ Backend ready for integration!")
        return 0

    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ SMOKE TEST FAILED: Cannot connect to server")
        print(f"   Error: {e}")
        print(f"\n   Possible causes:")
        print(f"   - Server did not start (check stderr)")
        print(f"   - Port 8001 already in use")
        print(f"   - Missing dependencies")
        return 1

    except AssertionError as e:
        print(f"\n❌ SMOKE TEST FAILED: {e}")
        return 1

    except Exception as e:
        print(f"\n❌ SMOKE TEST FAILED: Unexpected error")
        print(f"   Error: {e}")
        return 1

    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        proc.terminate()
        proc.wait(timeout=5)
        print("   Server stopped")

if __name__ == "__main__":
    sys.exit(main())
```

---

## ⚙️ DEPENDENCIES

**Stelle sicher dass installiert:**

```bash
# In backend/requirements.txt sollte sein:
requests>=2.31.0  # Für smoke test HTTP calls
```

Wenn nicht vorhanden:
```bash
cd backend
pip install requests
```

---

## 🚀 AUSFÜHREN

**1. Script erstellen:**
```bash
# Von cnc-toolcalc/ root directory:
vi backend/smoke_test.py
# (paste code above)
chmod +x backend/smoke_test.py
```

**2. Ausführen:**
```bash
python backend/smoke_test.py
```

**3. Expected Output:**
```
============================================================
🔥 SMOKE TEST: Backend Calculation API
============================================================

[1/5] Starting FastAPI server...
      Waiting 3 seconds for server startup...

[2/5] Testing /health endpoint...
      ✅ Health OK: {'status': 'healthy'}

[3/5] Testing /api/materials endpoint...
      ✅ Materials OK (8 materials loaded)
         Materials: Softwood, Hardwood, Aluminium...

[4/5] Testing /api/operations endpoint...
      ✅ Operations OK (13 operations loaded)
         Operations: FACE, POCKET, SLOT...

[5/5] Testing /api/calculate endpoint...
      ✅ Calculate OK
         vc: 450 m/min
         n:  14323 RPM
         fz: 0.08 mm
         vf: 2292 mm/min
         ae: 2.5 mm
         ap: 5.0 mm

============================================================
🎉 SMOKE TEST PASSED!
============================================================

✅ All 5 checks successful:
   1. Server started
   2. Health endpoint working
   3. Materials endpoint working (8 materials)
   4. Operations endpoint working (13 operations)
   5. Calculation endpoint working (10-phase engine)

✅ Backend ready for integration!

🛑 Stopping server...
   Server stopped
```

---

## 📄 SMOKE TEST REPORT

**Nach erfolgreichem Test, erstelle:**

`.agent-reports/backend-calculation/SMOKE_TEST_REPORT.md`

**Inhalt:**

```markdown
# Smoke Test Report: Backend Calculation

**Agent:** backend-calculation
**Date:** 2025-11-10
**Time:** [HH:MM]
**Status:** ✅ **PASS** / ❌ **FAIL**

---

## Test Execution

**Command:**
\`\`\`bash
python backend/smoke_test.py
\`\`\`

**Duration:** [X seconds]

---

## Test Results

| Test | Endpoint | Status | Details |
|------|----------|--------|---------|
| 1 | Server Start | ✅ PASS | Started in 3s |
| 2 | /health | ✅ PASS | Status: healthy |
| 3 | /api/materials | ✅ PASS | 8 materials loaded |
| 4 | /api/operations | ✅ PASS | 13 operations loaded |
| 5 | /api/calculate | ✅ PASS | 10-phase engine working |

---

## Sample Calculation Result

**Input:**
- Tool: 10mm diameter, TIN coating
- Material: ALUMINIUM
- Operation: SLOT

**Output:**
- vc: 450 m/min
- n: 14323 RPM
- fz: 0.08 mm
- vf: 2292 mm/min
- ae: 2.5 mm
- ap: 5.0 mm

---

## Issues Found

(none) / (list any issues)

---

## Conclusion

✅ Backend Calculation API is **PRODUCTION READY**
- All 7 endpoints working
- 10-Phase calculation engine functional
- 8-Checks validation working
- Cleanroom implementation verified

**Ready for Integration:** YES

---

**Tested by:** Backend Calculation Agent
**Sign-off:** ✅ APPROVED for Integration
```

---

## ✅ COMMIT

**Nach Test erfolgt:**

```bash
git add backend/smoke_test.py
git add .agent-reports/backend-calculation/SMOKE_TEST_REPORT.md
git commit -m "[BACKEND] Add smoke test + report

Smoke Test Results:
- Server start: PASS
- Health endpoint: PASS
- Materials endpoint: PASS (8 materials)
- Operations endpoint: PASS (13 operations)
- Calculate endpoint: PASS (10-phase engine)

Status: ✅ READY FOR INTEGRATION

Time: $(date +%H:%M)"

git push origin agent/backend-calculation
```

---

## 🎯 SUCCESS CRITERIA

- [x] `backend/smoke_test.py` erstellt
- [x] Script ausführbar (`chmod +x`)
- [x] Smoke test erfolgreich ausgeführt (alle 5 checks PASS)
- [x] SMOKE_TEST_REPORT.md erstellt
- [x] Committed & pushed

**Timeline:** 30-45 Minuten

**Wenn fertig:** Update diese Datei mit Status: ✅ **ERLEDIGT**

---

## ❓ FRAGEN?

**Siehe:**
- `.agent-reports/governance/STATUS_REPORT_2025-11-10.md` für Kontext
- `.agent-reports/governance/AGENT_INSTRUCTIONS_URGENT.md` für 30-min commit rule

**Governance Review:** Morgen (2025-11-11) 09:00

---

**Created:** 2025-11-10
**Priority:** 🚨 KRITISCH
**Deadline:** HEUTE (vor 18:00)
