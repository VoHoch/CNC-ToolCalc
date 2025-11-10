# Change Request: CR-2025-11-11-004 - Integration Day

**Date Created:** 2025-11-11
**Type:** Integration & Deployment
**Priority:** 🚨 CRITICAL
**Status:** IN_PROGRESS
**Assigned To:** ALL AGENTS (Backend, Frontend, UI) + Governance
**Target Version:** v0.1.0-alpha
**Deadline:** 2025-11-11 18:00

---

## 📋 SUMMARY

**Goal:** Merge all agent branches into `develop`, perform integration testing, and deploy to `main` as v0.1.0-alpha - making the application fully testable by the user.

**Scope:**
- Create `develop` branch
- Merge all 3 agent branches (backend, frontend, ui)
- Resolve merge conflicts
- Integration testing (Frontend ↔ Backend)
- Quality Gate 1.5 execution
- Tag v0.1.0-alpha release
- **USER GOAL: App must be testable!**

---

## 🎯 OBJECTIVES

### Primary Goal
✅ **User can test the complete application** (Frontend + Backend working together)

### Secondary Goals
1. ✅ All agent code merged to `develop` branch
2. ✅ No merge conflicts or blocking issues
3. ✅ Backend API running and accessible
4. ✅ Frontend UI connected to Backend
5. ✅ All 6 workflows functional end-to-end
6. ✅ Tag v0.1.0-alpha created

---

## 📊 CURRENT STATE (Starting Point)

### Branch Status
```
main (clean)
  └── Infrastructure files only

agent/backend-calculation ✅ READY
  ├── 2,900 lines of code
  ├── 10-Phase Calculation Engine
  ├── FastAPI with 7 endpoints
  ├── 35 Unit Tests + 9 Integration Tests
  └── Smoke tests PASSED

agent/frontend-workflow ✅ READY
  ├── 800 lines of code
  ├── 6 Screens
  ├── 5 Zustand Stores
  ├── API Client
  └── Smoke tests PASSED

agent/ui-specialist ✅ READY
  ├── 2,462 lines of code
  ├── 7 UI Components
  ├── Design System (105 CSS vars)
  ├── 23 Storybook stories
  └── Smoke tests PASSED (Slider NO thumb ✓)
```

### Known Overlaps
- Both UI and Frontend created state stores → **Merge required**
- Both UI and Frontend created components → **Use UI version (more complete)**
- Both UI and Frontend created screens → **Use Frontend version (6 screens)**

---

## 🔄 INTEGRATION WORKFLOW

### Phase 1: Preparation (Governance) - 30 min
**Responsibility:** Governance Agent

1. ✅ Read yesterday's completion reports
2. ✅ Verify all smoke tests passed
3. Create `develop` branch from `main`
4. Create integration test checklist
5. Prepare merge conflict resolution strategy

### Phase 2: Backend Integration - 1 hour
**Responsibility:** Backend Calculation Agent

**Tasks:**
1. Merge `agent/backend-calculation` → `develop`
2. Setup Python venv in `backend/venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests:
   - Unit tests: `pytest backend/tests/unit/`
   - Integration tests: `pytest backend/tests/integration/`
5. Start server: `uvicorn main:app --reload --port 8000`
6. Verify all 7 endpoints respond:
   - GET `/health`
   - GET `/api/materials`
   - GET `/api/operations`
   - POST `/api/calculate`
   - POST `/api/export/fusion`
   - POST `/api/export/csv`
   - GET `/api/health`
7. Create smoke test run report
8. Keep server running for frontend integration

**Expected Conflicts:** None (backend is isolated)

**Success Criteria:**
- ✅ All tests pass (44 tests)
- ✅ Server runs without errors
- ✅ All endpoints return 200 OK
- ✅ Calculation works (test payload returns results)

### Phase 3: UI Integration - 1 hour
**Responsibility:** UI Specialist Agent

**Tasks:**
1. Merge `agent/ui-specialist` → `develop`
2. Resolve conflicts with frontend files (if any)
3. Install dependencies: `npm install`
4. Build Storybook: `npm run build-storybook`
5. Verify all 7 components:
   - Slider (NO visible thumb!)
   - CompactSlider
   - Table
   - Button
   - Card
   - OperationMatrix
   - ProgressBar
6. Run component tests (if available)
7. Create integration report

**Expected Conflicts:**
- `frontend/src/components/` - Keep UI version
- `frontend/src/styles/` - Keep UI version (Design System)

**Success Criteria:**
- ✅ Storybook builds successfully
- ✅ All 7 components render
- ✅ Design System complete (105 CSS vars)
- ✅ No TypeScript errors

### Phase 4: Frontend Integration - 2 hours
**Responsibility:** Frontend Workflow Agent

**Tasks:**
1. Merge `agent/frontend-workflow` → `develop`
2. Resolve conflicts:
   - State stores: Keep Frontend version
   - Screens: Keep Frontend version (6 screens)
   - Components: Keep UI version (already merged)
3. Update imports to use UI components
4. Configure API client to point to `http://localhost:8000`
5. Install dependencies: `npm install`
6. Build: `npm run build`
7. Start dev server: `npm run dev --port 5173`
8. Connect to backend (verify API calls work)
9. Test all 6 workflows:
   - ToolSelection → MaterialSelection → OperationSelection
   - ParameterConfig → Calculate → Results
   - Export functionality

**Expected Conflicts:**
- `frontend/src/stores/` - Keep Frontend version (5 stores)
- `frontend/src/screens/` - Keep Frontend version (6 screens)
- `frontend/src/components/` - Keep UI version (7 components)

**Success Criteria:**
- ✅ Frontend builds without errors
- ✅ Dev server starts on port 5173
- ✅ API calls to backend succeed
- ✅ All 6 screens render
- ✅ Material selection PER TOOL works
- ✅ Calculation returns results from backend

### Phase 5: Integration Testing - 2 hours
**Responsibility:** ALL AGENTS (coordinated by Governance)

**Test Scenarios:**

#### Test 1: Basic Workflow (30 min)
1. Open `http://localhost:5173`
2. Navigate to Tool Selection
3. Select a tool (e.g., 10mm End Mill)
4. Navigate to Material Selection
5. Select material for this tool (e.g., Aluminium)
6. Navigate to Operation Selection
7. Select operation (e.g., SLOT)
8. Navigate to Parameter Configuration
9. Verify default parameters loaded
10. Click Calculate
11. Verify results displayed
12. Check: vc, n, fz, vf, ae, ap values present

**Expected:** All values calculated correctly, no errors

#### Test 2: Expert Mode (20 min)
1. Enable Expert Mode toggle
2. Verify global slider appears (-100% to +100%)
3. Adjust global slider
4. Verify all parameters update
5. Override individual parameter
6. Calculate
7. Verify overrides respected

**Expected:** Expert mode controls work, overrides apply

#### Test 3: Multi-Tool Workflow (30 min)
1. Add Tool 1 → Select Material A
2. Add Tool 2 → Select Material B (different!)
3. Add Tool 3 → Select Material A (same as Tool 1)
4. Calculate for each tool
5. Verify materials are PER TOOL (not global!)

**Expected:** Each tool has independent material selection

#### Test 4: API Direct Test (20 min)
```bash
# Test backend directly
curl http://localhost:8000/health
curl http://localhost:8000/api/materials
curl http://localhost:8000/api/operations

# Test calculation
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "tool": {"diameter": 10.0, "length": 50.0, "coating": "TIN", "flutes": 2},
    "material": "ALUMINIUM",
    "operation": "SLOT",
    "expert_mode": false
  }'
```

**Expected:** All endpoints return valid JSON

#### Test 5: Design System (20 min)
1. Verify Dark Theme active
2. Test 3 Contrast Modes (medium, balanced, high)
3. Verify Slider has NO visible thumb
4. Test keyboard navigation
5. Test accessibility (screen reader labels)

**Expected:** All design requirements met

**Success Criteria:**
- ✅ All 5 test scenarios pass
- ✅ No errors in browser console
- ✅ No errors in backend logs
- ✅ API responses valid
- ✅ UI renders correctly

### Phase 6: Quality Gate 1.5 - 1 hour
**Responsibility:** Governance Agent

**Checks:**

1. **Code Quality**
   - [ ] No TypeScript errors: `npm run type-check`
   - [ ] No Python syntax errors: `python -m py_compile backend/**/*.py`
   - [ ] Linting passes: `npm run lint` (if configured)

2. **Test Coverage**
   - [ ] Backend unit tests >90%: `pytest --cov`
   - [ ] Frontend tests pass (if available)
   - [ ] Integration tests pass

3. **Performance**
   - [ ] API response time <100ms (p95)
   - [ ] Frontend load time <2s
   - [ ] Calculation time <50ms

4. **Security**
   - [ ] No hardcoded secrets
   - [ ] No SQL injection vulnerabilities
   - [ ] No XSS vulnerabilities
   - [ ] CORS configured correctly

5. **Accessibility**
   - [ ] WCAG 2.1 AA compliance
   - [ ] Keyboard navigation works
   - [ ] Screen reader labels present
   - [ ] Focus indicators visible

6. **Architecture Compliance**
   - [ ] Cleanroom implementation (NO V2.0 code)
   - [ ] Material selection PER TOOL
   - [ ] Slider NO visible thumb
   - [ ] Dark theme + 3 contrast modes

**Success Criteria:**
- ✅ All checks pass
- ✅ No critical issues
- ✅ Minor issues documented for Phase 2

### Phase 7: Release - 30 min
**Responsibility:** Governance Agent

1. **Tag Release**
   ```bash
   git tag -a v0.1.0-alpha -m "Release v0.1.0-alpha

   Features:
   - 10-Phase Calculation Engine
   - 7 UI Components + Design System
   - 6-Screen Workflow
   - Material selection per tool
   - Expert mode with overrides
   - Export to Fusion 360 & CSV

   Components:
   - Backend: FastAPI + Python 3.12
   - Frontend: React + TypeScript + Vite
   - UI: 7 Components, 105 CSS variables

   Tests:
   - 35 Unit Tests
   - 9 Integration Tests
   - 100% Smoke Test Pass Rate

   Status: Alpha (internal testing)"
   ```

2. **Merge to Main**
   ```bash
   git checkout main
   git merge develop --no-ff -m "[RELEASE] v0.1.0-alpha - Integration Complete"
   git push origin main --tags
   ```

3. **Create Release Notes**
   - Document in `04-finale-version/RELEASE_NOTES_v0.1.0-alpha.md`
   - Include screenshots (optional)
   - List known issues
   - Document installation steps

4. **Update Documentation**
   - Update README.md with installation instructions
   - Update SPRINT_BOARD.md (mark Sprint 1 complete)
   - Update STATUS.md

**Success Criteria:**
- ✅ Tag created: v0.1.0-alpha
- ✅ Main branch updated
- ✅ Release notes published
- ✅ User can test app!

---

## 🎯 USER TESTING INSTRUCTIONS

**After integration complete, user can test with:**

### 1. Start Backend
```bash
cd /Users/nwt/developments/cnc-toolcalc
git checkout main  # or develop
cd backend

# Setup (first time only)
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start server
uvicorn main:app --reload --port 8000

# Verify
curl http://localhost:8000/health
```

**Backend runs on:** http://localhost:8000

### 2. Start Frontend (new terminal)
```bash
cd /Users/nwt/developments/cnc-toolcalc/frontend

# Setup (first time only)
npm install

# Start dev server
npm run dev

# Or production build
npm run build
npm run preview
```

**Frontend runs on:** http://localhost:5173

### 3. Test Application
1. Open browser: http://localhost:5173
2. Follow 6-screen workflow
3. Test calculations
4. Test expert mode
5. Test export functionality

---

## 📋 MERGE CONFLICT RESOLUTION STRATEGY

### Conflict Type 1: State Stores
**Location:** `frontend/src/stores/`
**Strategy:** Keep Frontend-Workflow version (5 Zustand stores)
**Reason:** Frontend agent focused on state management

### Conflict Type 2: UI Components
**Location:** `frontend/src/components/`
**Strategy:** Keep UI-Specialist version (7 components)
**Reason:** UI agent focused on component quality

### Conflict Type 3: Screens
**Location:** `frontend/src/screens/`
**Strategy:** Keep Frontend-Workflow version (6 screens)
**Reason:** Frontend agent focused on workflow

### Conflict Type 4: Design System
**Location:** `frontend/src/styles/`
**Strategy:** Keep UI-Specialist version (105 CSS variables)
**Reason:** UI agent owns design system

### General Rules:
1. **When in doubt:** Keep the more complete version
2. **Test after merge:** Run smoke tests again
3. **Document:** Note all conflicts in integration report
4. **Ask Governance:** For ambiguous conflicts

---

## ⚠️ KNOWN RISKS & MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| State store conflicts | HIGH | MEDIUM | Use Frontend version, update imports |
| Component conflicts | MEDIUM | LOW | Use UI version (more complete) |
| Backend port conflicts | LOW | LOW | Use port 8000, check before start |
| CORS issues | MEDIUM | MEDIUM | Configure CORS in FastAPI |
| NPM dependency conflicts | LOW | LOW | `npm install --legacy-peer-deps` |
| Python version issues | LOW | MEDIUM | Document Python 3.12 requirement |

---

## 📊 SUCCESS CRITERIA

### Must Have (Blocking)
- [ ] Backend server starts without errors
- [ ] Frontend dev server starts without errors
- [ ] API calls from frontend to backend succeed
- [ ] At least 1 complete workflow works (Tool → Material → Calculate → Results)
- [ ] No critical errors in console/logs
- [ ] User can test the application

### Should Have (Non-Blocking)
- [ ] All 6 workflows functional
- [ ] Expert mode works
- [ ] Export functionality works
- [ ] All tests pass (35 unit + 9 integration)
- [ ] Storybook builds successfully

### Nice to Have (Optional)
- [ ] Performance <100ms
- [ ] Accessibility 100% compliant
- [ ] No minor bugs
- [ ] Production build works

---

## 📝 DELIVERABLES

### Code Deliverables
1. ✅ `develop` branch with all code merged
2. ✅ `main` branch updated with v0.1.0-alpha
3. ✅ Git tag: v0.1.0-alpha
4. ✅ Working backend (port 8000)
5. ✅ Working frontend (port 5173)

### Documentation Deliverables
1. ✅ Integration test report
2. ✅ Merge conflict resolution log
3. ✅ Release notes (v0.1.0-alpha)
4. ✅ User testing instructions
5. ✅ Known issues document

### Quality Deliverables
1. ✅ Test results (unit + integration + smoke)
2. ✅ Performance metrics
3. ✅ Accessibility audit
4. ✅ Security review

---

## 🕐 TIMELINE

**Total Time:** 7-8 hours

| Phase | Duration | Start | End |
|-------|----------|-------|-----|
| 1. Preparation | 30 min | 09:00 | 09:30 |
| 2. Backend Integration | 1 hour | 09:30 | 10:30 |
| 3. UI Integration | 1 hour | 10:30 | 11:30 |
| 4. Frontend Integration | 2 hours | 11:30 | 13:30 |
| **LUNCH BREAK** | 30 min | 13:30 | 14:00 |
| 5. Integration Testing | 2 hours | 14:00 | 16:00 |
| 6. Quality Gate 1.5 | 1 hour | 16:00 | 17:00 |
| 7. Release | 30 min | 17:00 | 17:30 |
| **BUFFER** | 30 min | 17:30 | 18:00 |

**Deadline:** 18:00 CET

---

## 📞 COORDINATION PROTOCOL

### Communication
- **Governance** coordinates all agents
- **Status updates** every 30 minutes
- **Blockers** escalated immediately
- **Slack/Chat** for quick questions (if available)

### Git Strategy
- **Branch protection:** Don't push directly to `main`
- **Merge commits:** Use `--no-ff` for clean history
- **Commit messages:** Follow format: `[AGENT] ACTION: description`
- **Pull before push:** Always `git pull` before `git push`

### Testing Protocol
- **Test after each merge**
- **Don't break the build**
- **If tests fail:** Fix immediately or revert
- **Document all issues**

---

## ✅ ACCEPTANCE CRITERIA

**This CR is COMPLETE when:**

1. ✅ User can run backend: `uvicorn main:app --reload`
2. ✅ User can run frontend: `npm run dev`
3. ✅ User can open app: http://localhost:5173
4. ✅ User can complete workflow: Tool → Material → Operation → Calculate → Results
5. ✅ All code merged to `main` branch
6. ✅ Tag v0.1.0-alpha created
7. ✅ Integration test report published
8. ✅ No critical blockers

**USER GOAL MET:** ✅ Application is testable!

---

## 📚 REFERENCES

- Phase 1 Completion: `.agent-reports/governance/FINAL_INTEGRATION_READINESS_REPORT.md`
- Smoke Test Results: `.agent-reports/*/SMOKE_TEST_REPORT.md`
- Architecture: `01-dokumentation/CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md`
- API Contract: `01-dokumentation/API_CONTRACT.md`
- Component Interface: `01-dokumentation/COMPONENT_INTERFACE.md`

---

**CR Created:** 2025-11-11 09:00
**CR Owner:** Governance Agent
**Reviewers:** ALL AGENTS
**Status:** IN_PROGRESS → TESTING → UAT → APPROVED → MERGED

---

**🚀 LET'S MAKE THIS APP TESTABLE! 🚀**
