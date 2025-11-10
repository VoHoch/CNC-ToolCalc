# CNC-ToolCalc - Masterplan v0.0.1 → v1.0.0

**Projekt:** CNC Cutting Parameter Calculator
**Ziel:** Production-ready v1.0.0
**Dauer:** ~12 Tage (4 Sprints à 3 Tage)
**Strategie:** Multi-Agent Parallel Development

---

## Roadmap Overview

```
Week 1 (Sprint 1)        Week 2 (Sprint 2)        Week 3 (Sprint 3)        Week 4 (Sprint 4)
├─ v0.1.0               ├─ v0.2.0               ├─ v0.3.0               ├─ v1.0.0
│  Foundation           │  Calculation Core      │  Frontend Complete    │  Production Ready
│  - Design System      │  - 10-Phase Logic      │  - 8 Screens          │  - Export Module
│  - Backend Setup      │  - Coating (6 types)   │  - Expert Mode        │  - E2E Tests
│  - First Screen       │  - Surface Quality     │  - Results Display    │  - Deployment
└─────────────────────  └───────────────────────  └───────────────────── └──────────────────
```

---

## Sprint 1: Foundation (v0.1.0)

**Goal:** Development Foundation Ready

**Features:**
- ✅ Design System (Dark Theme, 3 Contrast Modes)
- ✅ Base Components (Slider, Table, Button, Card)
- ✅ Backend Structure (FastAPI + Pydantic)
- ✅ Tool Selection Screen (basic)
- ✅ State Management (Zustand)

**Deliverables:**
- design-tokens.css
- Slider Component (marker-based, NO thumb)
- Table Component (sortable)
- FastAPI Health Check + Tool Import Endpoint
- Tool Selection UI

---

## Sprint 2: Calculation Core (v0.2.0)

**Goal:** 10-Phase Calculation Implemented

**Features:**
- 🎯 10-Phase Calculation Workflow
  - Phase 1-2: vc + Coating Factor
  - Phase 3: n (RPM)
  - Phase 4-5: fz + Dry Correction
  - Phase 6-8: ae/ap + Surface Quality + Dynamic ap-Reference
  - Phase 9-10: Power + Chip Analysis
- 🎯 Tool Coating System (6 types)
- 🎯 Surface Quality (4 levels)
- 🎯 8-Checks Validation
- 🎯 Material per Tool (NICHT global!)

**Deliverables:**
- backend/calculation/ (all 10 phases)
- Coating Service
- Surface Quality Service
- Validation Service
- Material Selection Screen
- Operation Matrix Screen

---

## Sprint 3: Frontend Complete (v0.3.0)

**Goal:** All 8 Screens Implemented

**Features:**
- 🎯 Screen 1: Import (Smart Preset Detection)
- 🎯 Screen 2: Tool Selection (enhanced)
- 🎯 Screen 3: Material per Tool (pre-selection)
- 🎯 Screen 4: Operation Matrix (tabular)
- 🎯 Screen 5: Coating + Surface Quality + Coolant
- 🎯 Screen 6: Calculation Progress (WebSocket)
- 🎯 Screen 7: Results + Mathematical Workbook
- 🎯 Screen 8: Expert Mode

**Deliverables:**
- All 8 Screens functional
- Expert Mode (Global Slider + Individual Overrides)
- Mathematical Workbook (Formula transparency)
- Results Table (sortable, filterable)
- Progress Tracking

---

## Sprint 4: Production Ready (v1.0.0)

**Goal:** Release v1.0.0

**Features:**
- 🎯 Fusion 360 Export (.tools ZIP mit 13 Expressions)
- 🎯 Underscott CSV Export
- 🎯 E2E Testing (alle 13 Operationen)
- 🎯 Performance Optimization (<100ms calculation)
- 🎯 Security Audit
- 🎯 Documentation (Benutzerhandbuch)
- 🎯 Deployment Setup (Docker)

**Deliverables:**
- Export Module (Fusion + Underscott)
- E2E Test Suite (Playwright)
- Performance Tests
- Production Build
- BENUTZERHANDBUCH_DE.md
- Docker + docker-compose
- v1.0.0 Release! 🎉

---

## Success Metrics

### Technical
- ✅ Test Coverage: >90%
- ✅ Calculation Performance: <100ms (p95)
- ✅ UI Performance: <16ms render (60 FPS)
- ✅ Zero V2.0 Dependencies (Cleanroom)
- ✅ WCAG 2.1 AA Accessibility

### Functional
- ✅ 13 Operations (inkl. SLOT_TROCHOIDAL)
- ✅ 7 Materials (Härte-sortiert)
- ✅ 6 Coating Types
- ✅ 4 Surface Quality Levels
- ✅ Expert Mode (Global + Individual)
- ✅ Fusion 360 Export (13 Expressions)

### User Experience
- ✅ Dark Theme only (3 Contrast Modes)
- ✅ Material per Tool (NICHT global!)
- ✅ Smart Preset Detection
- ✅ Mathematical Workbook
- ✅ Intuitive 8-Screen Workflow

---

## Agent Distribution

| Agent | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 |
|-------|----------|----------|----------|----------|
| **UI Specialist** | Design System<br>Base Components | Surface Quality UI<br>Coating Selector | Expert Mode UI<br>Math Workbook | Polish<br>Final UX |
| **Frontend/Workflow** | Tool Selection<br>State Mgmt | Material Screen<br>Operation Matrix | All 8 Screens<br>Expert Mode Logic | Export UI<br>E2E Tests |
| **Backend/Calc** | FastAPI Setup<br>Import Endpoint | 10-Phase Calc<br>Coating/Surface | Validation<br>Chip Analysis | Export Service<br>Performance |
| **Governance** | CRs + Coordination<br>Quality Gate 0 | Integration Tests<br>Quality Gate 1 | API Integration<br>Quality Gate 2 | Final QA<br>Release v1.0 |

---

## Quality Gates

### Quality Gate 0: Foundation (Ende Sprint 1)
- Architecture Doc complete ✅
- Design System implemented
- Backend runs
- First Screen functional

### Quality Gate 1: Calculation (Ende Sprint 2)
- 10-Phase Calculation works
- All 13 Operations tested
- Unit Tests >90%

### Quality Gate 2: Frontend (Ende Sprint 3)
- All 8 Screens functional
- Expert Mode works
- Integration Tests pass

### Quality Gate 3: Production (Ende Sprint 4)
- Export validated (Fusion + Underscott)
- E2E Tests >95%
- Performance <100ms
- Security audit clean
- User UAT PASSED

---

## Dependencies & Risks

### Critical Dependencies
- ✅ Architecture Document (DONE - 7558 lines)
- ✅ API Contracts (DONE)
- ✅ Component Interfaces (DONE)
- ⏳ Phase 1 CRs (Governance TODO)

### Risks
- ⚠️ **Agent Coordination Overhead** - Mitigation: Daily standup via Git
- ⚠️ **Integration Complexity** - Mitigation: Quality Gates
- ⚠️ **Performance Issues** - Mitigation: Early benchmarking in Sprint 2
- ⚠️ **Scope Creep** - Mitigation: Strict CR process

---

## Timeline

```
Tag  1-3  : Sprint 1 (v0.1.0 Foundation)
Tag  4-6  : Sprint 2 (v0.2.0 Calculation)
Tag  7-9  : Sprint 3 (v0.3.0 Frontend)
Tag 10-12 : Sprint 4 (v1.0.0 Production)
```

**Start:** 2025-11-10 (HEUTE!)
**v1.0.0 Release:** 2025-11-22

---

**Status:** 🚀 ACTIVE
**Current Sprint:** Sprint 1 (Day 1)
**Next Milestone:** Quality Gate 0 (Ende Sprint 1)
