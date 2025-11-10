# CNC-ToolCalc Project Instructions für Claude

**VERSION:** 1.1
**DATE:** 2025-11-10
**STATUS:** ACTIVE

---

## 🎯 Projekt-Kontext

CNC-ToolCalc V4.0 - Multi-Agent Software-Entwicklung mit Cleanroom Strategy

- **3 Agent Team**: ui-specialist, frontend-workflow, backend-calculation
- **Governance**: Orchestriert alle Agents via Change Requests
- **Architektur**: 10-Phase Calculation Engine, NO V2.0 Dependency
- **Tech Stack**: React + TypeScript + Vite (Frontend), FastAPI + Python (Backend)

---

## 📁 WICHTIG: Verzeichnisstruktur & Dateien

### ✅ REGEL: Numbered Directories = ECHTE Dateien (NO Symlinks!)

**User-Friendly Navigation Structure:**
```
CNC-ToolCalc/
├── 01-dokumentation/           ← ECHTE Dateien (KEINE Symlinks!)
│   ├── README.md
│   ├── CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_CONSOLIDATED.md
│   ├── OPERATIONALIZATION_STRATEGY.md
│   ├── API_CONTRACT.md
│   └── COMPONENT_INTERFACE.md
│
├── 02-change-requests/         ← ECHTE Dateien (KEINE Symlinks!)
│   ├── README.md
│   └── active/
│       ├── CR-2025-11-11-001.md
│       ├── CR-2025-11-11-002.md
│       └── CR-2025-11-11-003.md
│
├── 03-development/             ← README (erklärt Code-Location)
│   └── README.md               (Code ist in ../backend/ und ../frontend/)
│
├── 06-sprints/                 ← ECHTE Dateien
│   ├── README.md
│   ├── MASTERPLAN.md
│   ├── SPRINT_01.md
│   └── SPRINT_BOARD.md
│
└── 07-agent-reports/           ← Symlink zu .agent-reports/ (EINZIGE Ausnahme!)
    → .agent-reports/           (Agents schreiben in hidden dir)
```

### 🚨 LESSONS LEARNED - Directory Structure

**Problem (2025-11-10):**
- Initial setup verwendete Symlinks: `01-dokumentation/docs -> docs`
- Symlinks waren BROKEN (falscher Pfad `docs -> docs` statt `docs -> ../docs`)
- Symlinks funktionieren nicht auf Windows
- Symlinks sind verwirrend in Git
- User sah: "unter 01 docs keine dateien nur einen link"

**Solution:**
1. **Numbered Directories (01-07) = ECHTE Dateien kopieren**
   ```bash
   # ✅ CORRECT
   cp docs/architecture/* 01-dokumentation/
   cp docs/contracts/* 01-dokumentation/
   cp docs/change-requests/active/* 02-change-requests/active/

   # ❌ WRONG
   ln -s docs 01-dokumentation/docs  # NIEMALS!
   ```

2. **Dateien existieren in ZWEI Orten (Duplikation OK):**
   - **Original Location**: `docs/` (Git standard, für IDEs)
   - **User-Friendly Copy**: `01-dokumentation/` (numbered, einfache Navigation)
   - **Unterschiedliche Inodes** = separate Dateien (nicht gelinkt)

3. **EINZIGE Symlink-Ausnahme:**
   ```bash
   # ✅ ACCEPTABLE (weil Agents in hidden dir schreiben müssen)
   ln -s .agent-reports 07-agent-reports
   ```
   - Agents schreiben in `.agent-reports/` (hidden)
   - User sieht `07-agent-reports/` (numbered)
   - Symlink funktioniert hier weil beide im selben Directory

4. **03-development/ = README only**
   - KEIN Symlink zu `../backend/` oder `../frontend/`
   - README erklärt: "Code ist in ../backend/ und ../frontend/"
   - Grund: Code muss im Root für Tools (npm, pytest, etc.)

### 🔧 Wie neue Dateien hinzufügen?

**Wenn du Architecture Docs aktualisierst:**
```bash
# 1. Original aktualisieren
vi docs/architecture/CNC_CALCULATOR_V4_*.md

# 2. Zu numbered directory kopieren
cp docs/architecture/CNC_CALCULATOR_V4_*.md 01-dokumentation/

# 3. Beide committen
git add docs/architecture/ 01-dokumentation/
git commit -m "[DOCS] Update architecture - copied to 01-dokumentation"
```

**Wenn du Change Requests erstellst:**
```bash
# 1. In docs/ erstellen
vi docs/change-requests/active/CR-2025-11-11-004.md

# 2. Zu numbered directory kopieren
cp docs/change-requests/active/CR-*.md 02-change-requests/active/

# 3. Beide committen
git add docs/change-requests/ 02-change-requests/
git commit -m "[GOVERNANCE] New CR - copied to 02-change-requests"
```

---

## 🏗️ Architektur-Entscheidungen (WICHTIG!)

### 1. ✅ Cleanroom Strategy
- **NO V2.0 Engine** (keine Abhängigkeit, kein Import)
- 100% neu geschrieben
- Alte Formeln als Referenz, aber Code komplett fresh

### 2. ✅ SQLite Usage (entschieden 2025-11-10)
**NUR für Tool Library:**
```python
# backend/data/tools.db (SQLite)
# - Tools (id, name, type, diameter, length, coating)
# - Presets (id, tool_id, material_id, vc, fz, ae, ap)

# ❌ NICHT für:
# - Materials (hardcoded in code)
# - Operations (hardcoded in code)
# - Calculations (in-memory only)
```

### 3. ✅ ae/ap NICHT parametrisch
- **Berechnet**: JA (Phase 6-8)
- **Exportiert zu Fusion**: JA (als Werte)
- **Parametrisch in Fusion**: NEIN (fixed values, nicht als expressions)

```typescript
// ✅ CORRECT Export
{
  "ae": 2.5,              // Fixed value
  "ap": 5.0,              // Fixed value
}

// ❌ WRONG Export
{
  "ae": "DC * 0.25",      // NO parametric expression!
  "ap": "LCF * 0.5",      // NO parametric expression!
}
```

### 4. ✅ Material Selection PER TOOL (nicht global!)
```typescript
// ✅ CORRECT - Material per Tool
const toolMaterials: Record<string, MaterialType> = {
  "T1": "ALUMINIUM",
  "T2": "STEEL_MILD",
  "T3": "ALUMINIUM",  // Same material for different tool = OK
};

// ❌ WRONG - Global Material
const selectedMaterial: MaterialType = "ALUMINIUM";  // NO!
```

### 5. ✅ Slider Component (KRITISCH!)
```typescript
// ✅ MUST HAVE
- NO visible thumb (marker-based design)
- Gradient background
- Dark theme only
- Touch-optimized markers

// ❌ NEVER
- Visible thumb/handle
- Light mode
- Standard browser slider
```

### 6. ✅ 30-Minute Commit Rule (alle Agents)
```bash
# Alle 30 Minuten committen:
git commit -m "[AGENT-NAME] PROGRESS: <task>
- Completed: <done>
- In Progress: <current>
- Next: <next>
Time: $(date +%H:%M)"
```

---

## 🔀 Git Branching Strategy

### Branch Structure
```
main                    ← Production (protected)
develop                 ← Integration (wird bei Integration Day erstellt)
agent/ui-specialist     ← UI Components, Design System
agent/frontend-workflow ← 6 Screens, State Management
agent/backend-calculation ← 10-Phase Engine, API
```

### ⚠️ WICHTIG: Code ist auf Agent Branches!
- **main branch**: Nur Infrastructure (docs/, 01-dokumentation/, etc.)
- **agent/* branches**: Tatsächlicher Code (backend/*.py, frontend/src/*.tsx)
- **User sieht empty directories auf main** = NORMAL (Code nicht gemerged yet)

### Integration Workflow
```bash
# 1. Agent arbeitet auf eigenem Branch
git checkout agent/backend-calculation
git add backend/
git commit -m "[BACKEND] IMPL: ..."
git push origin agent/backend-calculation

# 2. Governance reviewed
git checkout main
git diff main..agent/backend-calculation

# 3. Integration Day: Merge zu develop
git checkout develop
git merge agent/backend-calculation --no-ff
git merge agent/frontend-workflow --no-ff
git merge agent/ui-specialist --no-ff

# 4. Testing auf develop
npm run test:full
pytest backend/tests/

# 5. Release: Merge develop → main
git checkout main
git merge develop --no-ff
git tag -a v0.1.0 -m "Phase 1 Complete"
git push origin main --tags
```

---

## 📋 Change Request System

### CR Lifecycle
```
DRAFT → IN_PROGRESS → TESTING → GOVERNANCE_REVIEW → UAT → APPROVED → MERGED
```

### CR Naming Convention
```
CR-YYYY-MM-DD-NNN.md

Beispiele:
- CR-2025-11-11-001.md  (UI Specialist)
- CR-2025-11-11-002.md  (Frontend Workflow)
- CR-2025-11-11-003.md  (Backend Calculation)
```

### CR Locations (BEIDE!)
```bash
# 1. Original
docs/change-requests/active/CR-2025-11-11-001.md

# 2. User-Friendly Copy (parallel updaten!)
02-change-requests/active/CR-2025-11-11-001.md
```

---

## 🧪 Testing Requirements

### Smoke Tests (vor GOVERNANCE_REVIEW)
**Jeder Agent MUSS:**
```bash
# Backend Agent
pytest backend/tests/unit/         # Unit Tests
pytest backend/tests/integration/  # Integration Tests
python backend/smoke_test.py       # Smoke Test

# Frontend Agent
npm run test                       # Unit Tests
npm run test:integration          # Integration Tests
npm run smoke-test                # Smoke Test

# UI Agent
npm run test                      # Component Tests
npm run storybook                 # Visual Regression
npm run test:visual               # Smoke Test
```

### Coverage Requirements
- **Unit Tests**: >90%
- **Integration Tests**: >85%
- **E2E Tests**: >80%

---

## 📊 Quality Gates

### Gate 0: Foundation (Infrastructure)
- [x] Git Repo Setup
- [x] Directory Structure (mit ECHTEN Dateien!)
- [x] Architecture Docs (in 01-dokumentation/)
- [x] Change Request System
- [x] Agent Prompts

### Gate 1: Phase 1 Implementation
- [ ] UI Components (7) + Storybook
- [ ] Frontend Screens (6) + State (5 Stores)
- [ ] Backend API (7 Endpoints) + 10-Phase Engine
- [ ] Unit Tests >90%
- [ ] Smoke Tests passed

### Gate 2-5: Siehe SPRINT_BOARD.md

---

## 💬 Communication Protocol

### Agent Reports Location
```
.agent-reports/                      ← Agents schreiben hier (hidden)
├── ui-specialist/
│   └── STATUS.md
├── frontend-workflow/
│   └── STATUS.md
├── backend-calculation/
│   └── STATUS.md
└── governance/
    ├── COORDINATION_LOG.md
    ├── SPRINT_BOARD.md
    └── STATUS.md
```

### Daily Standup Format
```markdown
# Agent: [NAME]
**Date:** 2025-11-10
**Time:** HH:MM

## Yesterday
- Completed: [tasks]

## Today
- In Progress: [tasks]
- Blockers: [none/issues]

## Velocity
- Estimated: X hours
- Actual: Y hours
```

---

## 🚀 Nächste Schritte (Current Status)

### Sprint 1, Day 1 Complete (2025-11-10)
- ✅ Phase 0: Infrastructure
- ✅ Phase 1: Alle 3 Agents haben implementiert
  - UI Specialist: 5,028+ lines, 35+ files
  - Frontend Workflow: 800+ lines, 23 files
  - Backend Calculation: 2,500+ lines, 44 tests

### Integration Day (2025-11-11) - PLANNED
```
09:00-11:00  Review Agent Deliverables
11:00-13:00  Smoke Tests ausführen
13:00-15:00  Merge zu develop Branch
15:00-17:00  Integration Testing
17:00-18:00  Quality Gate 1 Review
```

---

## 🔍 Häufige Probleme & Lösungen

### Problem: "Ich sehe keine Dateien in 01-dokumentation/"
**Lösung:**
```bash
# Dateien kopieren (nicht linken!)
cp docs/architecture/* 01-dokumentation/
ls -la 01-dokumentation/  # Sollte Dateien zeigen, nicht Symlinks
```

### Problem: "Backend hat keinen Code?"
**Lösung:**
```bash
# Code ist auf agent branch!
git checkout agent/backend-calculation
ls -la backend/  # Jetzt siehst du .py Dateien
git checkout main  # Zurück zu main
```

### Problem: "Agent Reports sind leer?"
**Lösung:**
```bash
# Nur governance/ hat Files auf main
ls -la .agent-reports/governance/

# Andere Agents auf ihren branches:
git checkout agent/ui-specialist
ls -la .agent-reports/ui-specialist/
```

---

**Last Updated:** 2025-11-10
**Maintained by:** Governance Agent
**Reminder:** Immer bei neuen Lessons Learned diese Datei updaten!
