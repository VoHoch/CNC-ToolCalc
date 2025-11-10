# CNC-ToolCalc Agent Start Prompts

**Created:** 2025-11-10
**Version:** 1.0
**Status:** PRODUCTION READY

---

## Overview

This directory contains 4 agent start prompts for the CNC-ToolCalc V4.0 multi-agent development project. Each prompt enables autonomous Claude Code agents to execute their assigned responsibilities with full context and guidance.

---

## Files

### 1. **01-governance-agent.md** (488 lines)

**Role:** Orchestrator & Quality Guardian

Responsibilities:
- Multi-agent coordination (UI, Frontend, Backend)
- 5 Quality Gates (per phase)
- Change Request (CR) management
- Architecture compliance & integration testing
- Sprint management & escalation

Key Sections:
- Architecture Context (API Contracts, Component Interfaces)
- Daily Workflow (Phase Planning, Agent Coordination)
- CR Lifecycle (Draft → Approved)
- Git Commands (ready to copy-paste)
- Daily Routine (morning, midday, evening)

**Start This Agent When:** Ready to orchestrate full CNC-ToolCalc V4.0 development

---

### 2. **02-ui-specialist-agent.md** (639 lines)

**Role:** Design System Guardian & Component Architect

Responsibilities:
- Design tokens CSS (30+ variables, dark theme)
- 7 Base Components:
  - Slider (NO visible thumb - CRITICAL!)
  - CompactSlider (bidirectional)
  - Table (sortable, dark)
  - Button, Card, OperationMatrix, ProgressBar
- Storybook setup
- WCAG 2.1 AA accessibility

Key Features:
- Dark theme with 3 contrast modes
- Design tokens: bg-primary (#0b0f15), accent-primary (#6366F1)
- Typography: Inter, Work Sans, Fira Code
- 3 implementation phases (5-6 days)

**Start This Agent When:** Ready to build UI foundation (can run parallel with Backend)

---

### 3. **03-frontend-workflow-agent.md** (910 lines)

**Role:** Application Architect & UX Flow Builder

Responsibilities:
- 6-Screen Workflow:
  1. Tool Selection
  2. Material Selection **PER TOOL** (CRITICAL!)
  3. Operation Selection (13 operations)
  4. Coating + Surface Quality + Coolant
  5. Parameter Configuration + Results + Expert Mode
  6. Export (Fusion, Underscott)
- State Management (5 Zustand/Redux stores)
- Backend API integration
- Progressive disclosure (basic → expert)

Key Features:
- Material selection is **PER TOOL**, not global
- 5 state stores (fully specified)
- Expert mode: global slider (-50 to +50) + parameter overrides
- 3 implementation phases (5-7 days)

**Start This Agent When:** UI foundation complete & Backend API ready

**CRITICAL:** Material selection must be per-tool, not global! This was the root error in V3.0/V3.1.

---

### 4. **04-backend-calculation-agent.md** (855 lines)

**Role:** Calculation Engine Architect & API Developer

Responsibilities:
- V2.0 Engine Wrapper (READ-ONLY, NO-TOUCH)
- 10-Phase Calculation:
  - Phase 1-2: vc baseline + coating factor
  - Phase 3: spindle speed (RPM)
  - Phase 4-5: feed (fz + vf)
  - Phase 6-8: engagement (ae/ap + surface quality)
  - Phase 7: dynamic ap-reference (DC vs LCF)
  - Phase 9: power & temperature
  - Phase 10: chip analysis
- 7 FastAPI Endpoints
- Validation system (8 checks)
- Export service (Fusion .tools ZIP)

Key Features:
- 6 coating types with correct factors (TIN=1.4x, TIALN=1.6x, etc.)
- 4 surface quality levels
- Dynamic ap-reference: IF ld_ratio > 4.0 use LCF, else DC
- 8 validation checks (RPM, power, feed, coating, L/D, surface, engagement, temperature)
- Material table (7 materials, hardness-sorted)
- 3 implementation phases (7-8 days)

**Start This Agent When:** Architecture review complete (can run parallel with UI)

---

## Architecture Foundation

All prompts are based on:

- **CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md** - Complete architecture spec
- **OPERATIONALIZATION_STRATEGY.md** - Multi-agent orchestration plan
- **API_CONTRACT.md** - REST API specification
- **COMPONENT_INTERFACE.md** - UI component specifications
- **CHANGE_REQUEST_SYSTEM.md** - CR workflow
- **CONTROL_PROMPT_TEMPLATE.claude** - Execution mode template

---

## Key Design Decisions

### 1. Multi-Agent Orchestration
```
GOVERNANCE AGENT
├── UI SPECIALIST (Design System)
├── FRONTEND/WORKFLOW (6-Screen UX)
└── BACKEND/CALCULATION (10-Phase Logic)
```

Advantages:
- Parallel execution (4-6 days vs 10-12 sequential)
- Context-efficient (each agent: 25-50% of architecture)
- Specialized expertise per domain
- Clear contracts & interfaces

### 2. Material Selection PER TOOL (CRITICAL!)

**Lesson from V3.0/V3.1:** Global material selection caused fundamental design failure.

**V4.0 Solution:**
```
Screen 1: Select Tool (T1)
Screen 2: Select Materials FOR T1 (e.g., ALU, Steel)
(If multiple tools:)
Screen 2b: Select Materials FOR T2 (e.g., ALU, Brass)
```

**Enforce in Frontend Store:**
```typescript
materialsByTool: Record<string, string[]>  // {T1: ["ALU", "STEEL"], T2: ["ALU"]}
```

### 3. Dynamic ap-Reference Selection

**Critical Business Logic:**
```python
IF tool.ld_ratio > 4.0:
    ap_max = tool.LCF  # Use cutting length for long tools
ELSE:
    ap_max = tool.DC   # Use diameter for normal tools
```

This is implemented in Backend Phase 8 and must be tested rigorously.

### 4. Design System with NO Visible Slider Thumb

**Specification (from COMPONENT_INTERFACE.md):**
```css
.slider-input::-webkit-slider-thumb {
  width: 0;
  height: 0;
  opacity: 0;
}
```

The slider uses **markers** (Conservative, Optimal, Aggressive) instead of thumb visualization.

---

## Execution Mode: FULL EXECUTION

All prompts operate in **FULL EXECUTION** mode:
- No user interaction required
- Autonomous task execution
- Continuous build until completion
- All artifacts documented in audit reports
- Changes tracked via Change Request System

---

## Change Request System

Every task is tracked as a **Change Request (CR)**:

```
CR-YYYY-MM-DD-NNN

Lifecycle:
DRAFT → IN_PROGRESS → TESTING → GOVERNANCE_REVIEW → UAT → APPROVED

Example:
CR-2025-11-10-001: Phase 1 - Foundation (Design System + Base Components)
CR-2025-11-10-002: Phase 2 - Backend Calculation Engine (10 Phases)
CR-2025-11-10-003: Phase 3 - Frontend Workflow (6 Screens)
```

**Located in:** `docs/change-requests/active/` (in progress) or `approved/` (completed)

---

## Quality Gates

5 Quality Gates ensure architecture compliance:

**Gate 1 (Phase 1):** Design System Foundation
- CSS variables load
- Dark theme applied
- Slider component NO visible thumb
- Storybook runs

**Gate 2 (Phase 2):** Calculation Core
- All 10 phases implemented
- Unit tests >90% coverage
- 8 validation checks working
- Coating factors correct (6 types)

**Gate 3 (Phase 3):** Frontend Workflow
- 6 screens navigable
- Material selection PER TOOL (not global!)
- Expert mode functional
- E2E tests >90% pass

**Gate 4 (Phase 4):** Export & Advanced
- Fusion .tools ZIP valid
- 13 parametric expressions correct
- CSV export working
- Round-trip import/export

**Gate 5 (Phase 5):** Integration & Testing
- E2E tests >95% pass
- Performance <100ms (p95)
- Accessibility WCAG 2.1 AA
- Zero security issues

---

## Usage Instructions

### For Each Agent:

1. **Create New Claude Code Session**
   ```bash
   # Copy entire prompt file into Claude Code
   ```

2. **Agent Executes Autonomously**
   - Reads architecture documents
   - Creates Change Requests
   - Implements assigned tasks
   - Runs tests & audit
   - No user interaction needed

3. **Track Progress via CR System**
   ```bash
   # View active CRs
   cat docs/change-requests/active/CR-*.md

   # Check agent status
   cat .agent-reports/<agent-name>/STATUS.md
   ```

4. **Governance Approves & Merges**
   - Reviews CR results
   - Validates against architecture
   - Approves for UAT
   - Merges to develop/main

---

## Timeline Estimate

**Parallel Execution (Recommended):**
- Phase 1 (Foundation): Days 1-2
- Phase 2 (Calculation): Days 2-4 (parallel with Phase 1)
- Phase 3 (Frontend): Days 3-5 (starts after Phase 2 API ready)
- Phase 4 (Export): Days 5-6 (backend extension)
- Phase 5 (Testing): Days 6-8 (integration & optimization)

**Total: 4-6 Days (vs 10-12 sequential)**

---

## Critical Rules

1. **NO-TOUCH V2.0:** V2.0 Calculation Engine is read-only
2. **API Contracts First:** Define API before implementation
3. **Material Selection Per-Tool:** Never use global materials
4. **Test Coverage:** Minimum 90% unit tests (no exceptions)
5. **Dynamic ap-Reference:** Test L/D > 4.0 logic thoroughly

---

## Support Resources

- **Architecture:** `docs/architecture/CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md`
- **Operationalization:** `docs/architecture/OPERATIONALIZATION_STRATEGY.md`
- **API Spec:** `docs/contracts/API_CONTRACT.md`
- **Components:** `docs/contracts/COMPONENT_INTERFACE.md`
- **CR System:** `docs/CHANGE_REQUEST_SYSTEM.md`

---

## Success Criteria

**Project Complete When:**
- ✅ All 5 Quality Gates passed
- ✅ v1.0.0 released and stable
- ✅ E2E tests >95% pass rate
- ✅ Unit tests >90% coverage
- ✅ Accessibility WCAG 2.1 AA
- ✅ Performance <100ms (p95)
- ✅ Zero architecture violations
- ✅ Material selection per-tool verified
- ✅ Expert mode functional
- ✅ Fusion export with 13 expressions

---

**Last Updated:** 2025-11-10
**Version:** 1.0
**Status:** PRODUCTION READY

Ready to start CNC-ToolCalc V4.0 multi-agent development!
