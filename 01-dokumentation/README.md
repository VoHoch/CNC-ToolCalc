# 01-dokumentation - Architektur & Spezifikationen

Hier findest du alle technischen Dokumente für CNC-ToolCalc V4.0.

---

## 📚 Architektur-Dokumente

### 1. CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md (230KB)

**Das Hauptdokument** - Vollständige V4.0 Architektur

**Inhalt:**
- 10-Phase Calculation Workflow (Phasen 1-10)
- 13 Operationen (inkl. SLOT_TROCHOIDAL)
- 8 Materialien (Softwood → Steel Stainless)
- 6 Coating Types
- 4 Surface Quality Levels
- Design System (Dark Theme, 3 Contrast Modes)
- Backend-Architektur (FastAPI)
- Frontend-Architektur (React)
- Export-Modul (Fusion 360)
- User Stories & Epics

**Für wen:**
- Agents: Implementierungs-Spezifikation
- User: Architektur-Verständnis
- Governance: Review-Referenz

---

### 2. OPERATIONALIZATION_STRATEGY.md (26KB)

**Multi-Agent Implementation Strategy**

**Inhalt:**
- 3 Agent-Team (UI, Frontend, Backend)
- Phase 0-5 Rollout Plan
- Quality Gates
- Change Request System
- Context Window Management
- Coordination Protocol

**Für wen:**
- Governance: Orchestrierung
- Agents: Koordination
- User: Projekt-Verständnis

---

## 📋 Contracts & Spezifikationen

### 3. API_CONTRACT.md (16KB)

**Backend REST API Specification**

**Endpoints:**
- `GET /health` - Health Check
- `GET /api/materials` - 8 Materials
- `GET /api/operations` - 13 Operations
- `POST /api/calculate` - Main Calculation
- `POST /api/export/fusion` - Fusion 360 Export
- `POST /api/export/csv` - CSV Export
- `GET /api/health` - System Health

**Schemas:**
- CalculationRequest
- CalculationResponse
- Error Response Format
- Validation Rules

**Für wen:**
- Frontend Agent: API Integration
- Backend Agent: Implementation Spec
- Governance: Contract Validation

---

### 4. COMPONENT_INTERFACE.md (15KB)

**Frontend UI Components Specification**

**Components:**
1. **Slider** (NO visible thumb, gradient background)
2. **CompactSlider** (-100% to +100%, Expert Mode)
3. **Table** (Sortable, selectable, dark theme)
4. **Button** (4 variants)
5. **Card** (Clickable, selectable)
6. **OperationMatrix** (4 groups, 13 operations)
7. **ProgressBar** (6-step indicator)

**Design Tokens:**
- Color palette (Dark Theme)
- Spacing scale (Compact)
- Typography (Inter, Work Sans, Fira Code)
- 3 Contrast Modes (medium, balanced, high)

**Für wen:**
- UI Specialist: Implementation Spec
- Frontend Agent: Component Usage
- Governance: Design Review

---

## 🎯 Wie verwenden?

### Als Agent:
1. **Backend Agent:** Lies `CNC_CALCULATOR_V4_*` Teil 2-3 + `API_CONTRACT.md`
2. **Frontend Agent:** Lies `CNC_CALCULATOR_V4_*` Teil 4 + `API_CONTRACT.md`
3. **UI Agent:** Lies `COMPONENT_INTERFACE.md` + Design System Specs

### Als Governance:
- Alle Dokumente sind Referenz für Reviews
- Validiere Implementations gegen diese Specs
- Check Architecture Compliance

### Als User:
- `CNC_CALCULATOR_V4_*` für Gesamtverständnis
- `OPERATIONALIZATION_STRATEGY.md` für Projekt-Status
- Contracts für technische Details

---

## 📂 Weitere Dokumentation

**Change Requests:** `../02-change-requests/`
**Agent Reports:** `../07-agent-reports/`
**Sprints:** `../06-sprints/`

---

**Zuletzt aktualisiert:** 2025-11-10
**Version:** v0.1.0-alpha
