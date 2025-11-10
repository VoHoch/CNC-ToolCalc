# TODOs: Governance Agent

**Last Update:** 2025-11-10

---

## Phase 0: Foundation (CURRENT)

### Project Setup
- [x] Create project directory (cnc-toolcalc)
- [x] Initialize Git repository
- [x] Create directory structure (backend, frontend, docs, .agent-reports)
- [x] Create README.md
- [x] Create VERSION.txt
- [x] Create .gitignore
- [x] Create package.json (root workspace)
- [ ] Create initial commit

### V2.0 Engine Integration
- [ ] Copy V2.0 Engine from /Users/nwt/developments/Schnitttdaten/cnc_calculator
- [ ] Verify V2.0 Engine integrity (NO modifications!)
- [ ] Create wrapper service stub (backend/services/v2_wrapper.py)
- [ ] Document V2.0 API surface

### Contracts & Interfaces
- [ ] Define API Contract (docs/contracts/API_CONTRACT.md)
  - [ ] CalculationRequest schema
  - [ ] CalculationResponse schema
  - [ ] Error response schemas
  - [ ] All 13 operation endpoints
- [ ] Define Component Interfaces (docs/contracts/COMPONENT_INTERFACE.md)
  - [ ] Slider props
  - [ ] CompactSlider props
  - [ ] Table props
  - [ ] OperationMatrix props

### Architecture Documentation
- [ ] Expand CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md
  - [ ] Add Smart Preset Detection (~200 lines)
  - [ ] Add 8 Screen Specifications (~1200 lines)
  - [ ] Add Tool Coating System (~300 lines)
  - [ ] Add Surface Quality System (~250 lines)
  - [ ] Add Expert Mode Details (~400 lines)
  - [ ] Add SLOT_TROCHOIDAL (~100 lines)
  - [ ] Add Mathematical Workbook (~300 lines)
  - [ ] Add Fusion Export 13 Expressions (~250 lines)
  - [ ] Add Component Specifications (~500 lines)
  - [ ] Target: 7500 lines total

### Agent Preparation
- [ ] Create agent branch structure (git checkout -b agent/*)
- [ ] Create agent-specific documentation
  - [ ] docs/agents/ui-specialist/README.md
  - [ ] docs/agents/frontend-workflow/README.md
  - [ ] docs/agents/backend-calculation/README.md
- [ ] Create agent report templates
- [ ] Define agent coordination protocol

### Quality Gate 0
- [ ] Create Quality Gate 0 script (scripts/quality-gate-0.sh)
- [ ] Define Quality Gate 0 checklist
- [ ] Prepare validation criteria

---

## Phase 1: Core Implementation (PENDING)
- [ ] UI Specialist: Design System + Components
- [ ] Frontend: 6-Screen Workflow
- [ ] Backend: FastAPI + V2.0 Wrapper + 10-Phase Calculation

---

## Phase 2: Advanced Features (PENDING)
- [ ] Tool Coating (6 types)
- [ ] Surface Quality (4 levels)
- [ ] Expert Mode
- [ ] SLOT_TROCHOIDAL

---

## Phase 3: Export & Polish (PENDING)
- [ ] Fusion 360 Export
- [ ] Smart Preset Detection
- [ ] Mathematical Workbook

---

## Phase 4: Production Ready (PENDING)
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentation complete
- [ ] v1.0.0 release

---

**Next Action:** Copy V2.0 Engine to backend/v2_engine/
