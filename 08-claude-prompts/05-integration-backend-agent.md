# Backend Integration Agent Instruction

**MODE:** FULL EXECUTION
**DATE:** 2025-11-11
**TASK:** Backend Integration (Phase 2)
**TIME:** 1 hour
**Working Directory:** `/Users/nwt/developments/cnc-toolcalc`

---

## 🎯 YOUR MISSION

**Merge backend code to `develop` branch and make it running + testable.**

**USER GOAL:** Backend API must be running so frontend can connect to it.

---

## 📋 TASKS (Execute in Order)

### 1. Read Integration CR
```bash
cat 02-change-requests/active/CR-2025-11-11-004-INTEGRATION.md
```

### 2. Switch to develop branch
```bash
git checkout develop || git checkout -b develop
```

### 3. Merge your branch
```bash
git merge agent/backend-calculation --no-ff -m "[BACKEND] Merge backend-calculation to develop

Integration: Phase 2
- 10-Phase Calculation Engine
- FastAPI with 7 endpoints
- 35 Unit Tests + 9 Integration Tests
- Smoke tests: PASSED

Time: $(date +%H:%M)"
```

**Expected:** Clean merge (no conflicts)

### 4. Setup Python Environment
```bash
cd backend

# Create venv
python3.12 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Run Tests
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# With coverage
pytest tests/ --cov=backend --cov-report=term-missing
```

**Expected:** All 44 tests pass, coverage >90%

### 6. Start Server
```bash
# From backend/ directory
uvicorn main:app --reload --port 8000
```

**Keep server running!**

### 7. Test Endpoints (new terminal)
```bash
# Health check
curl http://localhost:8000/health

# Materials
curl http://localhost:8000/api/materials

# Operations
curl http://localhost:8000/api/operations

# Calculate (test payload)
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "tool": {
      "diameter": 10.0,
      "length": 50.0,
      "coating": "TIN",
      "flutes": 2
    },
    "material": "ALUMINIUM",
    "operation": "SLOT",
    "expert_mode": false
  }'
```

**Expected:** All return 200 OK with valid JSON

### 8. Create Integration Report
```bash
cat > .agent-reports/backend-calculation/INTEGRATION_REPORT.md << 'EOF'
# Backend Integration Report

**Date:** $(date +%Y-%m-%d)
**Time:** $(date +%H:%M)
**Status:** ✅ COMPLETE

## Merge Status
- Branch merged: agent/backend-calculation → develop
- Conflicts: NONE
- Merge commit: $(git log -1 --oneline)

## Test Results
- Unit tests: 35 PASSED
- Integration tests: 9 PASSED
- Coverage: >90%

## Server Status
- Server started: ✅
- Port: 8000
- Health endpoint: ✅ 200 OK
- Materials endpoint: ✅ 200 OK (8 materials)
- Operations endpoint: ✅ 200 OK (13 operations)
- Calculate endpoint: ✅ 200 OK (returns results)

## Issues
(none)

## Next Steps
- Keep server running on port 8000
- Frontend will connect to http://localhost:8000
- Monitor logs for errors

**Sign-off:** ✅ Backend READY for Frontend Integration
EOF
```

### 9. Commit Report
```bash
git add .agent-reports/backend-calculation/INTEGRATION_REPORT.md
git commit -m "[BACKEND] Integration complete - Server running on port 8000

Tests: 44/44 PASSED
Coverage: >90%
Server: http://localhost:8000
Status: ✅ READY

Time: $(date +%H:%M)"

git push origin develop
```

### 10. Keep Server Running
**IMPORTANT:** Do NOT stop the server! Frontend needs it.

Open new terminal for next tasks. Server terminal shows:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## ✅ SUCCESS CRITERIA

- [x] Code merged to develop (no conflicts)
- [x] Venv created and activated
- [x] All dependencies installed
- [x] All 44 tests pass
- [x] Coverage >90%
- [x] Server running on port 8000
- [x] All 7 endpoints respond with 200 OK
- [x] Integration report created
- [x] Server kept running for frontend

---

## 🐛 TROUBLESHOOTING

**Problem: "python3.12: command not found"**
```bash
# Check Python version
python3 --version

# Use available Python (3.11 or higher)
python3.11 -m venv venv
```

**Problem: "Port 8000 already in use"**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --reload --port 8001
```

**Problem: "Tests fail"**
```bash
# Show detailed error
pytest tests/ -v -s

# Run specific test
pytest tests/unit/test_phase_02_coating.py -v
```

**Problem: "pip install fails"**
```bash
# Update pip first
pip install --upgrade pip

# Install with verbose
pip install -r requirements.txt -v
```

---

## 📊 EXPECTED OUTPUT

**Terminal 1 (Server):**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Terminal 2 (Tests):**
```
collected 44 items

tests/unit/test_phase_02_coating.py ........  [ 18%]
tests/unit/test_phase_03_spindle.py ........  [ 36%]
tests/unit/test_phase_06_engagement.py ....  [ 45%]
tests/unit/test_validation.py ..............  [ 77%]
tests/integration/test_api.py .........       [100%]

====== 44 passed in 2.34s ======
```

**Terminal 3 (Curl test):**
```json
{
  "vc": 450,
  "n": 14323,
  "fz": 0.08,
  "vf": 2292,
  "ae": 2.5,
  "ap": 5.0,
  ...
}
```

---

## ⏰ TIME ESTIMATE

- Merge: 5 min
- Venv setup: 5 min
- Install deps: 10 min
- Run tests: 10 min
- Start server: 5 min
- Test endpoints: 10 min
- Create report: 10 min
- Commit & push: 5 min

**Total:** ~60 minutes

---

## 📝 FINAL CHECKLIST

Before marking complete:

- [ ] Server is running (check http://localhost:8000/health)
- [ ] All tests passed
- [ ] Integration report created
- [ ] Changes pushed to develop
- [ ] Server terminal still open (don't close!)
- [ ] Notify Governance: "Backend integration complete, server running"

---

**START TIME:** $(date +%H:%M)
**EXPECTED END:** 1 hour from now
**STATUS:** Ready to execute

**🚀 EXECUTE NOW!**
