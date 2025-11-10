# Operationalisierungs-Strategie: CNC Calculator V4.0

**Datum:** 2025-11-10
**Status:** PLANUNG
**Ziel:** Strukturierte Umsetzung der konsolidierten Architektur ohne Context-Window-Probleme

---

## EXECUTIVE SUMMARY

Die 3373-Zeilen Architektur muss effizient umgesetzt werden. Diese Strategie adressiert:

1. **Context Window Management** - Wie vermeiden wir Kontext-Überlauf?
2. **Agent-Architektur** - Ein Agent oder Multi-Agent-Orchestrierung?
3. **Team-Struktur** - Governance + 3 Spezialisten
4. **Greenfield vs. Migration** - Neu bauen oder Prototyp anpassen?
5. **Rollout-Plan** - Phasierung mit Validation Gates

**EMPFEHLUNG:** Multi-Agent-Orchestrierung mit Governance (Option B)

---

## 1. CONTEXT WINDOW PROBLEM

### 1.1 Die Herausforderung

```
Architektur-Dokument:     3373 Zeilen (~150 Seiten)
Claude Code Context:      ~200K Tokens
Geschätzter Verbrauch:    ~60K Tokens nur für Architektur
Verbleibend für Code:     ~140K Tokens
```

**Problem:** Bei einem einzelnen Agent würde die komplette Architektur permanent im Context liegen → schnelle Erschöpfung.

### 1.2 Kontext-Verteilung nach Zuständigkeit

| Agent | Relevante Architektur-Sections | Token-Bedarf | % der Gesamt-Architektur |
|-------|-------------------------------|--------------|--------------------------|
| **UI Specialist** | Part 2 (Domain Model - nur Data Structures)<br>Frontend Design System<br>Component Specs | ~15K | 25% |
| **Frontend/Workflow** | Part 2 (10-Phase Workflow)<br>Frontend Screen Specs<br>State Management | ~25K | 40% |
| **Backend/Calculation** | Part 2 (Complete Calculation Logic)<br>Backend API<br>V2.0 Wrapper | ~30K | 50% |
| **Governance** | Part 1 (Executive Summary)<br>Architecture Principles<br>Integration Specs | ~20K | 35% |

**Vorteil:** Jeder Agent benötigt nur 25-50% der Architektur, nicht 100%.

---

## 2. AGENT-ARCHITEKTUR: OPTIONEN

### Option A: Single Agent mit Self-Conversion ❌ NICHT EMPFOHLEN

#### Ansatz
```
1. Agent startet mit Phase 1 (Backend)
2. Bei Context-Limit → Checkpoint erstellen
3. Neuer Agent mit Checkpoint + Phase 2 (Frontend)
4. Wiederholen bis fertig
```

#### Vorteile
- Einfacher Setup
- Keine Koordination nötig
- Linearer Workflow

#### Nachteile
- **KRITISCH:** Kontext-Verlust zwischen Phasen
- Keine Parallelisierung möglich
- Checkpoints fehleranfällig
- Längere Gesamtdauer (sequenziell)
- Schwer zu debuggen bei Fehlern

**Geschätzte Dauer:** 8-12 Tage (sequenziell)

---

### Option B: Multi-Agent-Orchestrierung ✅ EMPFOHLEN

#### Ansatz
```
┌─────────────────────────────────────────────┐
│         GOVERNANCE AGENT (Orchestrator)      │
│  - Architecture Overview (Part 1)            │
│  - Integration Management                    │
│  - Quality Gates                             │
│  - Cross-cutting Concerns                    │
└─────────────┬───────────────────────────────┘
              │
       ┌──────┴───────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
  │   UI    │  │Frontend │  │ Backend │  │ Export  │
  │Specialist│  │/Workflow│  │/Calc    │  │Specialist│
  └─────────┘  └─────────┘  └─────────┘  └─────────┘
```

#### Zuständigkeiten

**GOVERNANCE AGENT** (Koordinator)
- Liest: Part 1 (Executive Summary, Principles, Lessons Learned)
- Aufgaben:
  - Startet und koordiniert Sub-Agents
  - Definiert Schnittstellen zwischen Teams
  - Validiert Integration
  - Führt Quality Gates durch
  - Löst Konflikte
  - Erstellt Final Reports

**UI SPECIALIST AGENT**
- Liest: Design Tokens, Component Specs, Prototype Audit
- Aufgaben:
  - Design System Setup (design-tokens.css)
  - Font Installation (Inter, Work Sans, Fira Code)
  - Base Components (Table, Slider, CompactSlider, Buttons)
  - Dark Theme Implementation
  - Contrast Mode Toggle
  - Component Storybook

**FRONTEND/WORKFLOW AGENT**
- Liest: 10-Phase Workflow, Screen Specs, State Management
- Aufgaben:
  - 6-Screen Workflow Implementation
  - State Management (Tool Selection, Material per Tool)
  - Progressive Disclosure Logic
  - Expert Mode UI (Global Slider + Overrides)
  - Form Validation & UX
  - Integration mit Backend API

**BACKEND/CALCULATION AGENT**
- Liest: Complete Part 2 (Calculation Logic), V2.0 Wrapper Specs
- Aufgaben:
  - V2.0 Engine Wrapper (NO-TOUCH)
  - FastAPI Endpoints (13 Operations)
  - 10-Phase Calculation Implementation
  - Tool Coating Logic (6 types)
  - Surface Quality Logic (4 levels)
  - Dynamic ap-Reference Selection
  - 8-Checks Validation System
  - L/D Stability Reductions
  - Chip Analysis (Temperature, Formation)

**EXPORT SPECIALIST AGENT** (Optional, kann von Backend übernommen werden)
- Liest: Fusion Export Specs, 13 Expressions Schema
- Aufgaben:
  - .tools ZIP Generator
  - Parametric Expression Generator
  - Underscott CSV Export
  - Import Module (Fusion → DB)

#### Vorteile
- ✅ **Parallelisierung:** UI + Frontend + Backend gleichzeitig
- ✅ **Context-Effizienz:** Jeder Agent nur 25-50% der Architektur
- ✅ **Spezialisierung:** Experten für jeden Domain
- ✅ **Rollback:** Fehler isoliert, kein Dominoeffekt
- ✅ **Skalierbar:** Weitere Agents bei Bedarf
- ✅ **Testbar:** Jeder Agent kann unabhängig getestet werden

#### Nachteile
- ⚠️ Komplexerer Setup
- ⚠️ Koordination erforderlich
- ⚠️ Governance Overhead

**Geschätzte Dauer:** 4-6 Tage (parallel)

---

## 3. EMPFOHLENE TEAM-STRUKTUR

### 3.1 Agent-Konfiguration

#### GOVERNANCE AGENT
```yaml
Name: "CNC_Governance"
Model: claude-sonnet-4-5
Context:
  - CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md (Part 1 only)
  - Integration Contracts (API schemas)
  - Quality Gates Checklist
Tasks:
  - Orchestrate sub-agents
  - Define API contracts
  - Run integration tests
  - Validate against architecture
  - Approve milestones
Tools:
  - Task (für Sub-Agent Delegation)
  - Bash (für Integration Tests)
  - Read (für Progress Reports)
```

#### UI SPECIALIST
```yaml
Name: "CNC_UI_Specialist"
Model: claude-sonnet-4-5
Context:
  - DESIGN_TOKENS.md
  - DESIGN_AUDIT_PROTOTYPE_vs_CURRENT.md
  - PROTOTYPE_SPECIFICATION_COMPLETE.md (Component Sections)
  - Part 2 (nur Data Structures für Type Definitions)
Tasks:
  - Implement Design System
  - Create Base Components
  - Ensure Dark Theme Compliance
  - Build Component Library
Deliverables:
  - src/styles/design-tokens.css
  - src/components/common/Slider.tsx + .css
  - src/components/common/CompactSlider.tsx + .css
  - src/components/common/Table.tsx + .css
  - src/components/common/Button.tsx + .css
  - src/components/common/Card.tsx + .css
  - Storybook Stories
```

#### FRONTEND/WORKFLOW AGENT
```yaml
Name: "CNC_Frontend_Workflow"
Model: claude-sonnet-4-5
Context:
  - Part 2 (10-Phase Workflow, Screen Specs)
  - Frontend State Management Specs
  - Expert Mode Specification
Tasks:
  - Implement 6-Screen Workflow
  - State Management (Material per Tool!)
  - Progressive Disclosure
  - Expert Mode (Global Slider + Overrides)
  - Form Validation
  - API Integration
Deliverables:
  - src/screens/ToolSelection.tsx
  - src/screens/OperationSelection.tsx
  - src/screens/MaterialSelection.tsx (per Tool!)
  - src/screens/ParameterConfiguration.tsx
  - src/screens/Results.tsx
  - src/screens/Export.tsx
  - src/state/calculationStore.ts
  - src/state/expertModeStore.ts
```

#### BACKEND/CALCULATION AGENT
```yaml
Name: "CNC_Backend_Calculation"
Model: claude-sonnet-4-5
Context:
  - Part 2 (Complete - All Calculation Logic)
  - V2.0 Engine Specs (NO-TOUCH Principle)
  - Backend Architecture (FastAPI)
Tasks:
  - Wrap V2.0 Engine (NO-TOUCH!)
  - Implement 10-Phase Calculation
  - Coating Logic (6 types)
  - Surface Quality (4 levels)
  - Dynamic ap-Reference
  - 8-Checks Validation
  - L/D Stability
  - Chip Analysis
Deliverables:
  - backend/services/calculation_service.py
  - backend/services/coating_service.py
  - backend/services/surface_quality_service.py
  - backend/services/validation_service.py
  - backend/api/routes/calculate.py (13 Operations)
  - backend/models/schemas.py
  - backend/tests/ (Unit + Integration)
```

### 3.2 Kommunikations-Protokoll

#### Schnittstellen-Definition (GOVERNANCE erstellt diese)

**API Contract: Frontend → Backend**
```typescript
// POST /api/calculate
interface CalculationRequest {
  tool: Tool;              // DC, length, material
  operation: Operation;    // FACE_ROUGH, SLOT_FULL, etc.
  coating: CoatingType;    // NONE, TIN, TIALN, etc.
  surfaceQuality: SurfaceQuality; // ROUGHING, STANDARD, etc.
  coolant: CoolantType;    // WET, DRY, MQL
  expertMode?: {
    globalSlider: number;  // -50 to +50
    overrides?: {
      ae_mm?: number;
      ap_mm?: number;
      fz_mm?: number;
    }
  }
}

interface CalculationResponse {
  results: {
    vc_m_min: number;
    n_rpm: number;
    fz_mm: number;
    vf_mm_min: number;
    ae_mm: number;
    ap_mm: number;
    power_kW: number;
    temperature_C: number;
    chipFormation: ChipFormationType;
  };
  warnings: string[];
  validationChecks: ValidationCheck[];
}
```

**Component Interface: UI → Frontend**
```typescript
// Slider Component Props (UI defines, Frontend uses)
interface SliderProps {
  min: number;
  max: number;
  value: number;
  markers: number[];           // Conservative, Optimal, Aggressive positions
  gradient: [string, string, string]; // Blue → Green → Red
  onChange: (value: number) => void;
  disabled?: boolean;
  compact?: boolean;          // For Expert Mode
  bidirectional?: boolean;    // For Global Slider (-100 to +100)
}
```

#### Workflow

1. **GOVERNANCE:** Erstellt API Contracts + Component Interfaces
2. **UI SPECIALIST:** Implementiert Components gemäß Interface
3. **FRONTEND:** Nutzt Components + ruft Backend API auf
4. **BACKEND:** Implementiert API gemäß Contract
5. **GOVERNANCE:** Integration Test (UI → Frontend → Backend → UI)

---

## 4. GREENFIELD VS. PROTOTYPE MIGRATION

### 4.1 Analyse des Prototypen

**Prototype Location:** `/tmp/cnc-prototype/app/src/`

**Was ist gut am Prototyp?**
- ✅ Design System (design-tokens.css) - **ÜBERNEHMEN**
- ✅ Slider Component (marker-based) - **ÜBERNEHMEN**
- ✅ CompactSlider (bidirectional) - **ÜBERNEHMEN**
- ✅ Table Component (Dark Theme) - **ÜBERNEHMEN**
- ✅ Dark Theme Implementation - **ÜBERNEHMEN**

**Was fehlt im Prototyp?**
- ❌ Kein Backend (nur Frontend)
- ❌ Keine echte Berechnung
- ❌ Kein Tool Coating System
- ❌ Kein Surface Quality System
- ❌ Keine 8-Checks Validation
- ❌ Kein Chip Analysis
- ❌ Kein Export Module

**Was ist schlecht am Prototyp?**
- ⚠️ Möglicherweise V3.x Fehler (globale Material-Auswahl?)
- ⚠️ Unbekannte Code-Qualität

### 4.2 Entscheidungsmatrix

| Kriterium | Greenfield | Migration | Gewinner |
|-----------|-----------|-----------|----------|
| **Design System** | Neu aufbauen (3-4 Tage) | Copy & Paste (1 Tag) | Migration ✅ |
| **Components** | Neu entwickeln (4-5 Tage) | Anpassen (2 Tage) | Migration ✅ |
| **Backend** | Neu bauen (erforderlich) | Neu bauen (erforderlich) | Gleich |
| **Calculation Logic** | Neu implementieren | Neu implementieren | Gleich |
| **Risiko V3.x Fehler** | Kein Risiko | Hohes Risiko | Greenfield ✅ |
| **Lernkurve** | Clean Start | Legacy verstehen | Greenfield ✅ |
| **Zeit gesamt** | 10-12 Tage | 8-10 Tage (wenn kein Legacy-Bug) | Migration (mit Risiko) |
| **Architektur-Konformität** | 100% garantiert | Abhängig von Prototype | Greenfield ✅ |

### 4.3 EMPFEHLUNG: HYBRID-ANSATZ ✅

```
┌─────────────────────────────────────────────────┐
│            HYBRID MIGRATION STRATEGY             │
└─────────────────────────────────────────────────┘

ÜBERNEHMEN VOM PROTOTYP:
✅ Design System (design-tokens.css)
✅ Slider Component (Slider.tsx + .css)
✅ CompactSlider Component (CompactSlider.tsx + .css)
✅ Table Component (Table.tsx + .css)
✅ Base Styles (Dark Theme)

GREENFIELD NEU BAUEN:
🆕 Gesamte Backend-Architektur
🆕 10-Phase Calculation Logic
🆕 Tool Coating System
🆕 Surface Quality System
🆕 8-Checks Validation
🆕 Frontend Workflow (6 Screens)
🆕 State Management (Material per Tool!)
🆕 Expert Mode (Global Slider + Overrides)
🆕 Export Module

VALIDIEREN VOR ÜBERNAHME:
⚠️ Prototyp auf V3.x Fehler prüfen (Material Selection)
⚠️ Code Review aller übernommenen Components
⚠️ Keine Business Logic vom Prototyp übernehmen
```

**Rationale:**
1. Design System ist stabil und CI-konform → übernehmen spart 3-4 Tage
2. Backend/Calculation MUSS neu sein (Prototyp hat keins)
3. Frontend Workflow MUSS neu sein (Material per Tool ist kritisch!)
4. Components sind UI-only, kein Risiko → übernehmen

**Vorgehen:**
1. **Phase 0 (Validation):** Prototyp-Components auf V3.x Fehler prüfen
2. **Phase 1 (Foundation):** Design System + Components übernehmen
3. **Phase 2 (Backend):** Komplett neu bauen
4. **Phase 3 (Frontend):** Workflow neu bauen (nutzt übernommene Components)

---

## 5. PHASEN-ROLLOUT MIT QUALITY GATES

### Phase 0: VALIDATION & SETUP (Tag 1)

**GOVERNANCE AGENT:**
- [ ] Architektur-Dokument aufteilen für Sub-Agents
- [ ] API Contracts definieren
- [ ] Component Interfaces definieren
- [ ] Quality Gates Checklist erstellen

**UI SPECIALIST:**
- [ ] Prototyp Slider.tsx Code Review (V3.x Fehler?)
- [ ] Prototyp Table.tsx Code Review
- [ ] Design Tokens Validierung (CI-konform?)

**QUALITY GATE 0:** ✋
- Alle Components validated?
- Keine V3.x Fehler gefunden?
- API Contracts approved?

---

### Phase 1: FOUNDATION (Tag 2-3)

**UI SPECIALIST:**
- [ ] `src/styles/design-tokens.css` erstellen (vom Prototyp)
- [ ] Fonts installieren (Inter, Work Sans, Fira Code)
- [ ] `src/components/common/Slider.tsx` + `.css` (vom Prototyp)
- [ ] `src/components/common/CompactSlider.tsx` + `.css` (vom Prototyp)
- [ ] `src/components/common/Table.tsx` + `.css` (vom Prototyp)
- [ ] `src/components/common/Button.tsx` + `.css` (neu)
- [ ] `src/components/common/Card.tsx` + `.css` (neu)
- [ ] Storybook Setup + Stories

**BACKEND SPECIALIST:**
- [ ] FastAPI Projekt Setup
- [ ] V2.0 Engine Wrapper (read-only, NO-TOUCH)
- [ ] Pydantic Models (Tool, Operation, Material, etc.)
- [ ] Database Schema (Tools, Presets, Results)
- [ ] Redis Setup (Caching)

**QUALITY GATE 1:** ✋
- Components rendern in Storybook?
- Dark Theme funktioniert?
- Slider ohne Thumb?
- Backend startet ohne Fehler?
- V2.0 Engine wrapper funktioniert?

---

### Phase 2: CALCULATION CORE (Tag 3-5)

**BACKEND SPECIALIST:**
- [ ] Phase 1-10 Calculation Service
  - [ ] Phase 1: vc Baseline
  - [ ] Phase 2: Coating Factor (6 types)
  - [ ] Phase 3: n (RPM)
  - [ ] Phase 4: fz Baseline
  - [ ] Phase 5: Dry/MQL Reduction
  - [ ] Phase 6: vf
  - [ ] Phase 7: ae/ap + Surface Quality
  - [ ] Phase 8: Dynamic ap-Reference Logic
  - [ ] Phase 9: Power + Temperature
  - [ ] Phase 10: Chip Analysis
- [ ] 8-Checks Validation Service
- [ ] L/D Stability Service
- [ ] Unit Tests (90%+ Coverage)

**FRONTEND SPECIALIST:**
- [ ] API Client Setup (OpenAPI generated)
- [ ] Calculation Store (Zustand/Redux)
- [ ] Tool Selection Store (Material per Tool!)

**QUALITY GATE 2:** ✋
- Alle 10 Phasen implementiert?
- Unit Tests >90% Coverage?
- 8-Checks funktionieren?
- Coating Factors korrekt?
- Surface Quality Adjustments korrekt?
- Dynamic ap-Reference Logic validated?
- Integration Test: API Call → Calculation → Response?

---

### Phase 3: FRONTEND WORKFLOW (Tag 5-7)

**FRONTEND SPECIALIST:**
- [ ] Screen 1: Tool Selection (DC, length)
- [ ] Screen 2: Material Selection **PER TOOL** (nicht global!)
- [ ] Screen 3: Operation Selection (13 Operations)
- [ ] Screen 4: Coating + Surface Quality + Coolant
- [ ] Screen 5: Parameter Configuration + Results
  - [ ] Basic Mode: Display only
  - [ ] Expert Mode: Global Slider + Individual Overrides
- [ ] Screen 6: Export (Fusion, Underscott)
- [ ] Progressive Disclosure Logic
- [ ] Form Validation (Client-side)

**UI SPECIALIST:**
- [ ] Screen-spezifische Component Anpassungen
- [ ] Expert Mode UI Polish
- [ ] Responsive Breakpoints

**QUALITY GATE 3:** ✋
- 6 Screens vollständig?
- Material Selection per Tool (nicht global)?
- Expert Mode: Global Slider funktioniert?
- Expert Mode: Individual Overrides funktionieren?
- Progressive Disclosure korrekt?
- Integration Test: UI → API → Results → UI?

---

### Phase 4: EXPORT & ADVANCED FEATURES (Tag 7-8)

**BACKEND SPECIALIST:**
- [ ] Fusion .tools Generator (ZIP)
- [ ] 13 Parametric Expressions Generator
- [ ] Underscott CSV Export
- [ ] Import Module (Fusion → DB)
- [ ] Preset Management API

**FRONTEND SPECIALIST:**
- [ ] Export Screen Integration
- [ ] Preset Save/Load UI
- [ ] Import Module UI

**QUALITY GATE 4:** ✋
- Fusion Export: 13 Expressions korrekt?
- ZIP Format valid?
- Import funktioniert?
- Presets speichern/laden?

---

### Phase 5: INTEGRATION & TESTING (Tag 8-10)

**GOVERNANCE AGENT:**
- [ ] End-to-End Tests (alle 13 Operations)
- [ ] Cross-Browser Testing
- [ ] Performance Testing (Calculation < 100ms)
- [ ] Accessibility Audit (WCAG 2.1 AA)
- [ ] Security Audit (Input Validation, XSS, etc.)

**ALL AGENTS:**
- [ ] Bug Fixes
- [ ] Performance Optimizations
- [ ] Documentation
- [ ] Deployment Prep

**QUALITY GATE 5:** ✋
- Alle E2E Tests grün?
- Performance <100ms?
- Accessibility WCAG 2.1 AA?
- Keine Security Issues?
- Deployment ready?

---

## 6. GOVERNANCE WORKFLOWS

### 6.1 Daily Standup (Async)

**Jeden Tag erstellt jeder Agent einen Progress Report:**

```markdown
# Progress Report: [Agent Name] - [Datum]

## Completed Today
- [ ] Task 1
- [ ] Task 2

## Blocked
- Issue X (needs input from Agent Y)

## Next 24h
- [ ] Task 3
- [ ] Task 4

## Quality Metrics
- Tests: 45/50 (90%)
- Code Coverage: 92%
- Linter Errors: 0
```

**GOVERNANCE AGENT sammelt und prüft:**
- Sind alle Agents on track?
- Gibt es Blocker?
- Müssen API Contracts angepasst werden?

### 6.2 Integration Points

**Nach jeder Phase führt GOVERNANCE einen Integration Test durch:**

```bash
# Phase 1 Integration Test
npm run storybook  # UI Components
npm run test:ui    # Component Tests
npm run backend:test  # Backend Unit Tests

# Phase 2 Integration Test
npm run test:api   # API Integration Tests
pytest backend/tests/integration/

# Phase 3 Integration Test
npm run test:e2e   # End-to-End Tests
playwright test

# Phase 4 Integration Test
npm run test:export  # Export Module Tests

# Phase 5 Integration Test
npm run test:full    # Full Stack Tests
```

### 6.3 Conflict Resolution

**Wenn API Contract geändert werden muss:**

1. **Agent meldet bei GOVERNANCE:** "API Contract X muss angepasst werden wegen Y"
2. **GOVERNANCE prüft Impact:** Welche anderen Agents betroffen?
3. **GOVERNANCE koordiniert:** Alle betroffenen Agents informieren
4. **GOVERNANCE approved:** Neue Contract Version
5. **Agents implementieren:** Anpassungen parallel

---

## 7. TOOLING & AUTOMATION

### 7.1 Agent-Koordination Tools

**Option A: Shared Git Repository**
```bash
git clone <repo>
cd cnc-calculator-v4

# Jeder Agent arbeitet auf eigenem Branch
git checkout -b agent/ui-specialist
git checkout -b agent/frontend-workflow
git checkout -b agent/backend-calculation

# GOVERNANCE merged nach Quality Gates
git checkout main
git merge agent/ui-specialist  # Nach Gate 1
```

**Option B: Claude Code Projects (Parallel Sessions)**
```
Project 1: CNC_UI_Specialist
Project 2: CNC_Frontend_Workflow
Project 3: CNC_Backend_Calculation
Project 4: CNC_Governance (Orchestrator)

# Governance nutzt Task tool um Sub-Agents zu delegieren
```

### 7.2 Continuous Integration

```yaml
# .github/workflows/integration.yml
name: Integration Tests

on:
  push:
    branches: [agent/*]

jobs:
  ui-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run test:ui
      - run: npm run storybook:build

  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest backend/tests/ --cov=backend

  integration-tests:
    needs: [ui-tests, backend-tests]
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:e2e
      - run: npm run test:api
```

---

## 8. RISIKO-MANAGEMENT

### 8.1 Risiken & Mitigations

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| **Context Window Overflow** | Hoch | Kritisch | Multi-Agent Architektur (jeder Agent nur 25-50%) |
| **API Contract Misalignment** | Mittel | Hoch | GOVERNANCE definiert Contracts VOR Implementation |
| **V3.x Fehler im Prototyp** | Mittel | Hoch | Phase 0 Validation (Code Review) |
| **Agent Coordination Overhead** | Mittel | Mittel | Daily Progress Reports + Quality Gates |
| **Integration Bugs** | Mittel | Hoch | Integration Tests nach jeder Phase |
| **Performance Issues** | Niedrig | Mittel | Performance Tests in Phase 5 |
| **Calculation Logic Fehler** | Niedrig | Kritisch | Unit Tests >90% Coverage + E2E Validation |

### 8.2 Rollback-Strategie

**Wenn Quality Gate NICHT bestanden:**

```
Gate Failed → Identify Issue → Assign to Agent → Fix → Re-Test → Gate Retry

Max 2 Retries pro Gate. Bei 3. Failure:
→ GOVERNANCE eskaliert
→ Architektur-Review
→ Eventuell Approach ändern
```

---

## 9. SUCCESS METRICS

### 9.1 Definition of Done

**Gesamt-Projekt:**
- ✅ Alle 5 Quality Gates bestanden
- ✅ E2E Tests >95% Pass Rate
- ✅ Unit Tests >90% Coverage
- ✅ Performance: Calculation <100ms
- ✅ Accessibility: WCAG 2.1 AA
- ✅ Security: Keine kritischen Issues
- ✅ Dokumentation: README + API Docs + Component Docs

**Pro Agent:**

**UI Specialist:**
- ✅ Storybook mit allen Components
- ✅ Dark Theme 100% konform zu Prototyp
- ✅ Slider ohne sichtbaren Thumb
- ✅ Component Tests >90% Coverage

**Frontend/Workflow:**
- ✅ 6 Screens vollständig implementiert
- ✅ Material Selection **per Tool** (nicht global!)
- ✅ Expert Mode: Global Slider + Overrides funktionieren
- ✅ E2E Tests für alle User Flows

**Backend/Calculation:**
- ✅ 10-Phase Calculation korrekt implementiert
- ✅ Alle 13 Operations funktionieren
- ✅ 6 Coating Types korrekt
- ✅ 4 Surface Quality Levels korrekt
- ✅ 8-Checks Validation funktioniert
- ✅ Unit Tests >90% Coverage

### 9.2 Performance Targets

```
Calculation Response Time:  <100ms (p95)
UI Render Time:             <16ms (60 FPS)
API Latency:                <50ms
Export Generation:          <500ms (Fusion .tools)
Page Load:                  <2s (initial)
```

---

## 10. NÄCHSTE SCHRITTE

### SOFORT (vor Start):
1. [ ] **User Approval:** Diese Strategie vom User bestätigen lassen
2. [ ] **Entscheidung:** Greenfield vs. Hybrid Migration bestätigen
3. [ ] **Setup:** Git Repository oder Claude Projects vorbereiten

### TAG 1 (Phase 0):
1. [ ] GOVERNANCE: API Contracts definieren
2. [ ] GOVERNANCE: Component Interfaces definieren
3. [ ] UI SPECIALIST: Prototyp Code Review (V3.x Fehler prüfen)
4. [ ] Quality Gate 0 durchführen

### TAG 2-10:
1. [ ] Phasen 1-5 durchführen gemäß Rollout-Plan
2. [ ] Nach jeder Phase: Quality Gate
3. [ ] Daily Progress Reports von allen Agents

---

## 11. OFFENE FRAGEN AN USER

Vor Start müssen folgende Punkte geklärt werden:

### 11.1 Tooling
- [ ] **Git Repository:** Existiert bereits eines oder neu erstellen?
- [ ] **Branching Strategy:** Feature Branches pro Agent oder Trunk-Based?
- [ ] **CI/CD:** GitHub Actions, GitLab CI, oder andere?

### 11.2 Deployment
- [ ] **Hosting:** Wo soll deployed werden? (Vercel, AWS, self-hosted?)
- [ ] **Database:** PostgreSQL, MongoDB, oder andere?
- [ ] **Redis:** Cloud-Service oder self-hosted?

### 11.3 Migration
- [ ] **Prototyp Location:** Ist `/tmp/cnc-prototype/` der korrekte Pfad?
- [ ] **V2.0 Engine:** Wo liegt der V2.0 Code exakt?

### 11.4 Team
- [ ] **Review Process:** Wer reviewed die Agent Outputs? User oder GOVERNANCE Auto-Approve?
- [ ] **Approval Gates:** Braucht jedes Quality Gate User-Approval oder automatisch?

---

## FAZIT

**EMPFOHLENE STRATEGIE:**

```
┌─────────────────────────────────────────────────────┐
│  MULTI-AGENT ORCHESTRIERUNG (Option B)              │
│  + HYBRID MIGRATION (Prototyp Components + Neu)     │
│  + 5-PHASEN ROLLOUT mit Quality Gates               │
│  = 4-6 Tage Umsetzung (parallel)                    │
└─────────────────────────────────────────────────────┘
```

**Vorteile dieser Strategie:**
1. ✅ Kein Context Window Problem (jeder Agent 25-50%)
2. ✅ Parallelisierung (4-6 Tage statt 10-12)
3. ✅ Spezialisierung (Experten pro Domain)
4. ✅ Risiko-Minimierung (Quality Gates, Rollback)
5. ✅ Zeit-Ersparnis (Prototyp Components übernehmen)
6. ✅ Architektur-Konformität (Greenfield für Business Logic)

**Nächster Schritt:**
→ User-Approval dieser Strategie
→ Dann: Phase 0 starten

---

**Status:** ✅ BEREIT FÜR USER-REVIEW
**Erstellt:** 2025-11-10
**Agent:** Claude Code (Governance Mode)
**Version:** 1.0
