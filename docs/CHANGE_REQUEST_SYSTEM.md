# Change Request System - CNC-ToolCalc

**Version:** v0.0.1-alpha
**Last Updated:** 2025-11-10

---

## Overview

All code changes in CNC-ToolCalc follow the **Change Request (CR) workflow**:

1. **Governance Agent** creates CR with requirements
2. **Implementation Agent** implements CR
3. **Implementation Agent** runs Audit + Smoke Test
4. **Governance Agent** reviews results
5. **User** performs UAT (User Acceptance Test)
6. **Governance Agent** approves and merges

---

## CR Naming Convention

```
CR-YYYY-MM-DD-NNN

Example: CR-2025-11-10-001
```

- `YYYY-MM-DD`: Date created
- `NNN`: Sequential number (001, 002, ...)

---

## CR Lifecycle

```
┌──────────────────────────────────────────────────────┐
│ 1. DRAFT                                             │
│    - Governance creates CR                           │
│    - Assigns to Agent                                │
│    - Defines requirements                            │
└────────────────┬─────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────┐
│ 2. IN_PROGRESS                                       │
│    - Agent implements changes                        │
│    - Agent writes tests                              │
│    - Agent commits to agent branch                   │
└────────────────┬─────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────┐
│ 3. TESTING                                           │
│    - Agent runs unit tests (>90% coverage)          │
│    - Agent runs integration tests                    │
│    - Agent runs smoke test                           │
│    - Agent updates CR with results                   │
└────────────────┬─────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────┐
│ 4. GOVERNANCE_REVIEW                                 │
│    - Governance reviews code changes                 │
│    - Governance checks architecture compliance       │
│    - Governance validates test results               │
│    - Decision: APPROVED / CHANGES_REQUESTED          │
└────────────────┬─────────────────────────────────────┘
                 │
          ┌──────┴──────┐
          │             │
    [APPROVED]    [CHANGES_REQUESTED]
          │             │
          │             └──→ Back to IN_PROGRESS
          │
┌─────────▼──────────────────────────────────────────┐
│ 5. UAT (User Acceptance Test)                     │
│    - User tests feature manually                   │
│    - User provides feedback in CR                  │
│    - Decision: PASS / FAIL                         │
└────────────────┬───────────────────────────────────┘
                 │
          ┌──────┴──────┐
          │             │
       [PASS]        [FAIL]
          │             │
          │             └──→ Back to IN_PROGRESS (with user feedback)
          │
┌─────────▼──────────────────────────────────────────┐
│ 6. APPROVED                                        │
│    - Governance merges agent branch → develop     │
│    - Updates version number                        │
│    - Tags release                                  │
│    - Closes CR                                     │
└────────────────────────────────────────────────────┘
```

---

## Version Numbering

**Semantic Versioning:** `vMAJOR.MINOR.PATCH`

### During Development (v0.x.y)

```
v0.0.1  → Initial setup
v0.1.0  → Phase 1 complete (Foundation)
v0.2.0  → Phase 2 complete (Calculation Core)
v0.3.0  → Phase 3 complete (Frontend Workflow)
v0.4.0  → Phase 4 complete (Export)
v0.5.0  → Phase 5 complete (Testing & Polish)
v1.0.0  → Production Ready! 🎉
```

### CR Impact on Version

| Change Type | Version Increment | Example |
|-------------|-------------------|---------|
| **Phase Complete** | MINOR (+0.1.0) | v0.1.0 → v0.2.0 |
| **Feature** | PATCH (+0.0.1) | v0.1.0 → v0.1.1 |
| **Enhancement** | PATCH (+0.0.1) | v0.1.1 → v0.1.2 |
| **Bug Fix** | PATCH (+0.0.1) | v0.1.2 → v0.1.3 |
| **Refactoring** | No increment | (same version) |
| **Documentation** | No increment | (same version) |

---

## CR Directory Structure

```
docs/change-requests/
├── CR_TEMPLATE.md                     # Template for new CRs
├── active/                            # In-progress CRs
│   ├── CR-2025-11-10-001.md          # Backend: Phase 1 Setup
│   └── CR-2025-11-10-002.md          # UI: Design System
├── approved/                          # Completed & merged CRs
│   └── CR-2025-11-09-001.md
└── rejected/                          # Rejected CRs (for reference)
    └── CR-2025-11-08-001.md
```

---

## CR Workflow: Detailed Steps

### Step 1: Governance Creates CR

**Governance Agent:**

```bash
# 1. Create new CR from template
cp docs/change-requests/CR_TEMPLATE.md \
   docs/change-requests/active/CR-2025-11-10-001.md

# 2. Fill in CR details:
# - Summary: "Implement Phase 2: Coating Factor Logic"
# - Agent: backend-calculation
# - Requirements from Architecture Doc

# 3. Commit CR
git add docs/change-requests/active/CR-2025-11-10-001.md
git commit -m "[GOVERNANCE] CR-2025-11-10-001: Phase 2 Coating Logic

Assigned to: backend-calculation
Target version: v0.1.1
Phase: 1
"

# 4. Update sprint board
# (Add to agent's TODO list in .agent-reports/)
```

---

### Step 2: Agent Implements CR

**Implementation Agent (e.g., backend-calculation):**

```bash
# 1. Read CR
cat docs/change-requests/active/CR-2025-11-10-001.md

# 2. Implement changes
# - Write code
# - Write tests
# - Update documentation

# 3. Commit changes to agent branch
git checkout agent/backend-calculation
git add backend/calculation/core/phase_02_coating.py
git add backend/tests/test_phase_02_coating.py
git commit -m "[BACKEND-CALC] IMPL: CR-2025-11-10-001 Phase 2 Coating Logic

- Implemented coating factor calculation (6 types)
- TiN: +40%, TiAlN: +60%, AlTiN: +80%, Diamond: +120%, Carbide: +50%
- Unit tests: 12/12 passing
- Coverage: 100%

CR: CR-2025-11-10-001
Agent: backend-calculation
Status: testing
"

# 4. Update CR status → TESTING
# (Edit CR file, change status)
```

---

### Step 3: Agent Runs Audit + Smoke Test

**Implementation Agent:**

```bash
# 1. Run unit tests
pytest backend/tests/test_phase_02_coating.py --cov=backend.calculation.core.phase_02_coating

# 2. Run smoke test (agent creates this)
cat > scripts/smoke-test-cr-2025-11-10-001.sh <<'EOF'
#!/bin/bash
# Smoke Test: CR-2025-11-10-001 - Phase 2 Coating Logic

echo "Testing coating factor calculations..."

# Test TiN coating
python -c "
from backend.calculation.core.phase_02_coating import calculate_coating_factor
from backend.models.coating import CoatingType

factor, vc_final = calculate_coating_factor(100.0, CoatingType.TIN)
assert factor == 1.4, f'TiN factor wrong: {factor}'
assert vc_final == 140.0, f'vc_final wrong: {vc_final}'
print('✓ TiN coating works')
"

# ... more tests

echo "✓ All smoke tests passed!"
EOF

chmod +x scripts/smoke-test-cr-2025-11-10-001.sh
./scripts/smoke-test-cr-2025-11-10-001.sh

# 3. Update CR with test results
# (Paste results into CR file)

# 4. Commit CR update
git add docs/change-requests/active/CR-2025-11-10-001.md
git add scripts/smoke-test-cr-2025-11-10-001.sh
git commit -m "[BACKEND-CALC] TEST: CR-2025-11-10-001 Smoke Test Passed

Unit Tests: 12/12 ✓
Coverage: 100%
Smoke Test: PASSED ✓

CR: CR-2025-11-10-001
Status: governance_review
"

git push origin agent/backend-calculation
```

---

### Step 4: Governance Reviews CR

**Governance Agent:**

```bash
# 1. Pull agent branch
git checkout agent/backend-calculation
git pull

# 2. Read CR results
cat docs/change-requests/active/CR-2025-11-10-001.md

# 3. Review code changes
git diff main..agent/backend-calculation

# 4. Run quality audit checklist:
# - Architecture compliance? ✓
# - No V2.0 dependencies? ✓
# - Tests >90%? ✓
# - Type safety? ✓
# - Security issues? None ✓

# 5. Decision: APPROVED
# Update CR status → UAT

# 6. Notify user (commit message)
git commit --allow-empty -m "[GOVERNANCE] CR-2025-11-10-001: APPROVED for UAT

Code review passed ✓
Architecture compliant ✓
Tests passing ✓

@User: Ready for UAT
Test plan in CR file
"
```

---

### Step 5: User Performs UAT

**User (You):**

```bash
# 1. Checkout agent branch
git checkout agent/backend-calculation

# 2. Run application
npm run dev  # or backend dev server

# 3. Test feature manually according to UAT test plan in CR

# 4. Provide feedback (edit CR file or comment in governance session)

# Example feedback:
"UAT PASSED ✓
- Coating calculation works correctly
- TiN gives +40% as expected
- UI displays coating factor
- No bugs found

Approved for merge."
```

---

### Step 6: Governance Merges CR

**Governance Agent:**

```bash
# 1. User feedback positive → merge

git checkout develop
git merge agent/backend-calculation --no-ff -m "[GOVERNANCE] Merge CR-2025-11-10-001: Phase 2 Coating Logic

UAT: PASSED ✓
User: Approved
Version: v0.0.1 → v0.1.1

CR: CR-2025-11-10-001
Agent: backend-calculation
Phase: 1
"

# 2. Update version
echo "v0.1.1" > VERSION.txt
git add VERSION.txt
git commit -m "[GOVERNANCE] Version bump: v0.0.1 → v0.1.1"

# 3. Tag release
git tag -a v0.1.1 -m "v0.1.1: Phase 2 Coating Logic complete

CR-2025-11-10-001: Coating factor calculation implemented
- 6 coating types supported
- Unit tests: 12/12 passing
- UAT: Passed
"

# 4. Move CR to approved/
git mv docs/change-requests/active/CR-2025-11-10-001.md \
       docs/change-requests/approved/
git commit -m "[GOVERNANCE] Close CR-2025-11-10-001 (APPROVED)"

# 5. Push all
git push origin develop
git push origin v0.1.1

# 6. Merge to main (after quality gate)
git checkout main
git merge develop --no-ff
git push origin main
```

---

## Sprint Planning Integration

### Sprint Structure

```
Sprint 1 (Week 1):
├── CR-2025-11-10-001: Backend Phase 1 Setup
├── CR-2025-11-10-002: UI Design System
└── CR-2025-11-10-003: Frontend State Management

Sprint 2 (Week 2):
├── CR-2025-11-17-001: Backend Phase 2 Coating
├── CR-2025-11-17-002: UI Slider Component
└── ...
```

### Sprint Board

Located in: `.agent-reports/governance/SPRINT_BOARD.md`

```markdown
# Sprint 1: Foundation (2025-11-10 to 2025-11-17)

## Backlog
- [ ] CR-2025-11-10-001: Backend Phase 1 Setup (backend-calculation)
- [ ] CR-2025-11-10-002: UI Design System (ui-specialist)
- [ ] CR-2025-11-10-003: Frontend State (frontend-workflow)

## In Progress
- [🔄] CR-2025-11-10-001 (backend-calculation)

## Testing
- (none)

## UAT
- (none)

## Done
- (none)

## Velocity: 0 / 3 CRs
```

---

## Change Request Communication

### Governance → Agent

Governance assigns CR by:
1. Creating CR in `docs/change-requests/active/`
2. Adding CR to agent's `.agent-reports/<agent>/TODOS.md`
3. Committing with `[GOVERNANCE] CR-XXX assigned to <agent>`

### Agent → Governance

Agent reports progress by:
1. Updating CR status in CR file
2. Updating `.agent-reports/<agent>/STATUS.md`
3. Committing with `[<AGENT>] CR-XXX: <status>`

### User → Governance

User provides feedback by:
1. Editing CR file (UAT section)
2. OR: Creating issue in `.agent-reports/governance/USER_FEEDBACK.md`
3. Governance forwards to relevant agent

---

## Example: Full CR Lifecycle

See: `docs/change-requests/approved/CR-2025-11-09-001-EXAMPLE.md`

---

**Status:** ✅ READY FOR USE
**Last Updated:** 2025-11-10
**Governance Agent:** Approved
