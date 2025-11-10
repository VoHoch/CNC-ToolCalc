# CNC Calculator V4.0 - Final Consolidated Architecture

**Version:** 4.0 Consolidated
**Datum:** 2025-11-10
**Status:** FINAL - Production Ready Specification
**Zweck:** Komplette Architektur-Spezifikation für Greenfield-Implementierung

---

## DOCUMENT METADATA

**Konsolidiert aus:**
- CNC_CALCULATOR_V4_FINAL_ARCHITECTURE_COMPLETE.md
- DELTA_REQUEST_GUI_WORKFLOW_COMPLETE-4.md
- PROTOTYPE_SPECIFICATION_COMPLETE.md
- DESIGN_AUDIT_PROTOTYPE_vs_CURRENT.md
- VERSION_COMPARISON_V2_V3_V3_1.md
- Fusion Tool Import Specifications
- UI Design System v0.3_production

**Autoren:**
- Volker (Fachexperte, Product Owner)
- Claude (Architektur-Konsolidierung)
- Prof. Dr.-Ing. (Berechnungs-Validierung)

**Change Log:**
- v4.0 Consolidated (2025-11-10): Vollständige Konsolidierung aller Dokumente
- v4.0 (2025-11-10): Export Module + Expert Mode Complete
- v3.0 (2025-11-10): Professor Consultation + Coating/Surface Quality
- v2.0 (2025-11-10): User Feedback + ap-reference Logic
- v1.0 (2025-11-10): Initial GUI Workflow Simulation

---

## INHALTSVERZEICHNIS

### TEIL 1: EXECUTIVE SUMMARY
1.1 Projektziele & Vision
1.2 Kritische Lessons Learned (V2/V3 ausführlich)
1.3 Architektur-Prinzipien
1.4 Technologie-Stack
1.5 Projektstruktur-Übersicht

### TEIL 2: DOMÄNENMODELL & BERECHNUNGSLOGIK
2.1 Berechnungs-Workflow (10 Phasen)
2.2 Materialien (7 Materialien, Härte-sortiert)
2.3 Operationen (13 Operationen inkl. SLOT_TROCHOIDAL)
2.4 Tool Coating System (6 Typen)
2.5 Surface Quality System (4 Levels)
2.6 ap-Referenz Logik (dynamisch)
2.7 L/D Stability Reductions
2.8 Chip Temperature Analysis
2.9 Dry Machining Corrections
2.10 Validierung (8 Checks)

### TEIL 3: BACKEND-ARCHITEKTUR
3.1 System-Architektur (API-First)
3.2 REST API Design (FastAPI)
3.3 Calculation Service (V2.0 Wrapper)
3.4 Expert Mode Engine
3.5 Database Schema & Models (Pydantic)
3.6 Async Processing (Celery + Redis)
3.7 File Storage & Management
3.8 Error Handling & Logging
3.9 Security & Authentication

### TEIL 4: FRONTEND-ARCHITEKTUR
4.1 Design System (Prototyp v0.3_production)
4.2 Design Tokens (Dark Theme, 3 Kontrast-Modi)
4.3 Komponenten-Bibliothek
4.4 6-Screen-Workflow (detailliert)
4.5 Expert Mode UI
4.6 Mathematical Workbook
4.7 State Management (Zustand + React Query)
4.8 Responsive Design & Accessibility

### TEIL 5: EXPORT-MODUL
5.1 Fusion 360 Parametric Export
5.2 13 Expression Generator
5.3 CSV/Excel/JSON/PDF Export
5.4 Export Validation & Testing

### TEIL 6: USER STORIES & EPICS
6.1 Epic E1: Tool Import & Selection
6.2 Epic E2: Material & Operation Selection
6.3 Epic E3: Calculation & Results
6.4 Epic E4: Export & Integration
6.5 Epic E5: Expert Mode & Workbook
6.6 Acceptance Criteria (komplett)

### TEIL 7: IMPLEMENTIERUNGS-STRATEGIE
7.1 3-Phasen-Plan
7.2 Phase 9 Reintegration
7.3 Migration vom Prototyp
7.4 Testing Strategie
7.5 Deployment Checklist

### TEIL 8: ANHÄNGE
8.1 Glossar
8.2 API Quick Reference
8.3 Troubleshooting Guide
8.4 Change Request Template

---

# TEIL 1: EXECUTIVE SUMMARY

## 1.1 Projektziele & Vision

### Vision Statement

**"Ein präzises, benutzerfreundliches CNC-Berechnungstool, das Ingenieuren ermöglicht, optimale Schnittparameter zu berechnen und nahtlos in Fusion 360 zu exportieren."**

### Hauptziele

**1. Präzision (NO-TOUCH Prinzip)**
- Bewährte V2.0 Berechnungslogik bleibt unverändert
- Mathematisch validierte Formeln (Prof. Dr.-Ing.)
- Industrie-Standards: VDI 3214, DIN 6527

**2. Benutzerfreundlichkeit**
- Intuitiver 6-Screen-Workflow
- Klare visuelle Hierarchie
- Dark Theme mit hoher Lesbarkeit
- Progressive Disclosure (Basis → Expert Mode)

**3. Produktionsreife**
- Vollständige Test-Coverage
- Robuste Error-Handling
- Performante Berechnung (< 2s für 100 Presets)
- Stabile API

**4. Nahtlose Integration**
- Fusion 360 Parametric Export
- .tools File Import/Export
- CSV/Excel/JSON/PDF Export

### Erfolgskriterien

✅ **Funktional:**
- Alle 13 Operationen implementiert
- Tool Coating & Surface Quality integriert
- Expert Mode voll funktionsfähig
- Export zu Fusion ohne Warnungen

✅ **Qualität:**
- Test Coverage > 85%
- Response Time < 2s (95th percentile)
- Zero Breaking Changes zu V2.0 Berechnungen

✅ **User Experience:**
- Onboarding < 5 Minuten
- Task Success Rate > 90%
- System Usability Scale (SUS) > 80

---

## 1.2 Kritische Lessons Learned (V2/V3 ausführlich)

### Historischer Kontext

**V2.0** war die letzte funktionsfähige Version mit vollständigem Tool-Konzept. **V3.0** und **V3.1** waren Vereinfachungsversuche, die fundamentale Designfehler einführten.

---

### V2.0 - "Last Known Good" ✅

**Zeitraum:** 2024-Q4
**Status:** ERFOLG (mit Einschränkungen)

#### ✅ Stärken (BEHALTEN)

**1. Vollständiger Tool-Flow**
```
Import → Tool Selection → Material per Tool → Operations → Results
```
- Jeder Schritt klar definiert
- Validation verhindert Fehler
- User weiß immer wo er steht

**2. Sequential Workflow mit Progress Indicator**
```
[ ✓ Import ] → [ ✓ Tools ] → [ 3 Materials ] → [ Operations ] → [ Results ]
```
- 5-Step-Stepper immer sichtbar
- Abgeschlossene Schritte markiert
- Kommende Schritte ausgegraut

**3. Material-per-Tool (KERNKONZEPT)**
```typescript
const materialsByTool: Record<string, string[]> = {
  "T1": ["ALU", "STEEL"],
  "T2": ["ALU", "BRASS"],
};
```
- ✅ Korrekte Domänen-Modellierung
- ✅ Verschiedene Materialien für verschiedene Tools
- ✅ Flexibel für echte Anwendungsfälle

**4. Results gruppiert nach Tool**
```
Tool: T1 Planfräser Ø30
├─ ALU + Face Rough:  vc=377 m/min, Status: OK
├─ ALU + Slot Full:   vc=377 m/min, Status: OK
└─ STEEL + Face Rough: vc=240 m/min, Status: WARNING

Tool: T2 Schaftfräser Ø6
└─ ALU + Schlichten:  vc=150 m/min, Status: OK
```
- Hierarchische Darstellung
- Klare Tool-Zuordnung
- Übersichtlich auch bei vielen Results

#### ⚠️ Schwächen (VERBESSERN)

**1. Kein echter .tools File Parser**
```tsx
// ❌ V2.0 hatte nur Mock-Upload
<input type="file" accept=".tools" />
// Aber keine Parser-Logik!
```
→ **V4.0 Lösung:** Vollständiger .tools Parser (ZIP + JSON extraction)

**2. Kein Zurück-Button**
```
Step 1 → Step 2 → Step 3 → Step 4 → Step 5
         (keine Rücknavigation möglich)
```
→ **V4.0 Lösung:** Bi-direktionale Navigation + State-Persistence

**3. Keine Zusammenfassung**
```
User in Step 4: "Welche Tools/Materials hatte ich nochmal gewählt?"
→ Muss zurückblättern
```
→ **V4.0 Lösung:** Persistent Summary Panel (rechte Sidebar)

**4. Mock-Berechnungen**
```typescript
// ❌ Zufallszahlen statt echte Berechnung
const vc = Math.random() * 500;
```
→ **V4.0 Lösung:** Backend-Integration mit V2.0 Calculation Engine

---

### V3.0 - "Single-Page Simplification" ❌

**Zeitraum:** 2025-Q1
**Status:** FEHLGESCHLAGEN (Spec-Compliance: 40%)

#### ❌ Fundamentale Designfehler

**KRITISCH: Kein Tool-Konzept**
```typescript
// ❌ V3.0 State - FEHLT: tools, selectedTools
const [selectedMaterials, setSelectedMaterials] = useState<string[]>([]);
const [selectedOperations, setSelectedOperations] = useState<string[]>([]);
```

**Workflow-Vergleich:**
```
❌ V3.0: Material → Operations → Results
✅ SPEC:  Import → Tools → Material per Tool → Operations → Results
```

**Problem:**
- User kann keine Werkzeuge auswählen
- Material-Auswahl gilt global (nicht pro Tool)
- Verletzt Kern-Anforderung des Systems

**Root Cause Analysis:**
```
Ursache: Versuch zu "vereinfachen" führte zu Über-Vereinfachung
↓
Tool-Dimension komplett entfernt
↓
Material-per-Tool Konzept aufgegeben
↓
System wurde funktional unbrauchbar für echte Anwendungsfälle
```

#### Weitere Probleme

**2. Globale statt tool-spezifische Material-Auswahl**
```tsx
// ❌ V3.0: Alle Materialien für alle (nicht existenten) Tools
<MaterialCard selected={selectedMaterials.includes('ALU')} />

// ✅ V2.0: Pro Tool
<MaterialCard
  selected={materialsByTool[toolId]?.includes('ALU')}
  toolId={toolId}
/>
```

**3. Flache Results ohne Tool-Hierarchie**
```
ALU + Face Rough:  vc=377 m/min
STEEL + Face Rough: vc=240 m/min
ALU + Slot Full:   vc=377 m/min
```
→ Welches Tool? Unklar!

**4. Keine Navigation/Progress-Indicator**
- User scrollt auf Single Page
- Kein Feedback wo er ist
- Kein Überblick über Gesamtzustand

#### Was funktionierte (BEHALTEN)

**1. Sofortiger Überblick**
- Alle Optionen auf einen Blick
- Reduzierte Klicks

**2. Visuelle Hierarchie & Farbcodierung**
```css
FACE:      #fb923c  (Orange)
PERIPHERAL: #3b82f6  (Blue)
GEOMETRY:   #06b6d4  (Cyan)
SPECIAL:    #a855f7  (Purple)
```
→ **V4.0:** Diese Farben ÜBERNEHMEN

**3. Design-Token-Konsistenz**
- Durchgängiges dark-balanced Theme
- Professionelles Erscheinungsbild
→ **V4.0:** Prototyp-Design als Basis

---

### V3.1 - "Tab-Based Attempt" ❌

**Zeitraum:** 2025-Q1
**Status:** FEHLGESCHLAGEN (Spec-Compliance: 40%)

#### Tab-System ohne Tool-Konzept

```tsx
// ❌ V3.1: 5 Tabs, aber FEHLT: Tool-Tab
<Tabs>
  <Tab name="Material" />      {/* Global statt pro Tool */}
  <Tab name="Operations" />
  <Tab name="Results" />
  <Tab name="Expert" />         {/* Nur Placeholder */}
  <Tab name="Workbook" />       {/* Nur Placeholder */}
</Tabs>
```

**Problem:**
- Gleicher Fehler wie V3.0 (kein Tool-Konzept)
- ZUSÄTZLICH: Fragmentierung durch Tabs
- User muss zwischen Tabs springen
- Kein Überblick über Gesamtzustand

#### Lessons Learned

**Was NICHT funktioniert:**

❌ **Vereinfachung durch Weglassen essentieller Konzepte**
- Tool-Konzept ist NICHT optional
- Simplification ≠ Dumbing Down

❌ **Tab-System ohne Tool-Dimension**
- Tabs schaffen Fragmentierung
- Ohne Tool-Konzept bringen sie keinen Mehrwert

❌ **Placeholders als "Features"**
- Expert/Workbook Tabs waren leer
- "Not implemented"-Messages verwirren User

---

### Fundamentale Erkenntnisse für V4.0

#### MUST-HAVE Design-Prinzipien

**1. Tool-Konzept ist NICHT OPTIONAL** ⚠️
```
IMMER: Import → Tool Selection → Material per Tool → ...
NIEMALS: Material (global) → Operations → ...
```

**Begründung:**
- Verschiedene Tools haben verschiedene Eigenschaften
- Materialien müssen pro Tool gewählt werden
- DC, LCF, NOF beeinflussen Berechnungen

**2. Sequential Flow mit Progress Indicator**
```
[ Step 1 ] → [ Step 2 ] → [ Step 3 ] → [ Step 4 ] → [ Step 5 ]
```

**Vorteile:**
- User weiß immer wo er ist
- Validation pro Schritt
- Klarer nächster Schritt

**3. State-Persistence & Bi-Direktionale Navigation**
```
Step 3 → [Back] → Step 2 (State erhalten!)
                  ↓
                  [Edit Tool Selection]
                  ↓
                  [Continue] → Step 3 (aktualisiert!)
```

**4. Hierarchische Results**
```
Tool (Gruppe)
└─ Material + Operation (Rows)
```
Nicht: Flache Liste

**5. NO-TOUCH Berechnungslogik**
- V2.0 Calculation Engine bleibt unverändert
- Wrapper-Service für API
- Keine direkten Änderungen an Formeln

---

### Spec-Compliance-Vergleich

| Requirement | V2.0 | V3.0 | V3.1 | V4.0 (Ziel) |
|-------------|------|------|------|-------------|
| Tool Import/Selection | ✅ | ❌ | ❌ | ✅ |
| Material per Tool | ✅ | ❌ | ❌ | ✅ |
| Operations Matrix | ✅ | ✅ | ⚠️ | ✅ |
| Progress Indicator | ✅ | ❌ | ⚠️ | ✅ |
| Hierarchical Results | ✅ | ❌ | ❌ | ✅ |
| Bi-Directional Navigation | ❌ | ❌ | ❌ | ✅ |
| Real Calculations | ❌ | ❌ | ❌ | ✅ |
| Export Module | ❌ | ❌ | ❌ | ✅ |
| Expert Mode | ❌ | ❌ | ❌ | ✅ |
| **GESAMT** | **60%** | **20%** | **20%** | **100%** |

---

### Architektonische Debt aus V3.x

**1. shadcn/ui Abhängigkeit** ❌
```bash
# V3.0/V3.1 hatten shadcn/ui
npm install @radix-ui/react-* (20+ packages)
```
→ **V4.0:** Eigene Komponenten basierend auf Prototyp (0 External UI-Libs)

**2. Light Theme als Default** ❌
```css
body {
  background: #f5f5f5;  /* V3.x */
}
```
→ **V4.0:** Dark Theme (v0.3_production) als EINZIGES Theme

**3. Fehlende Design Tokens** ❌
→ **V4.0:** design-tokens.css mit ~30 CSS Variables

**4. Keine TypeScript Interfaces für Domain Models** ⚠️
→ **V4.0:** Pydantic Models (Backend) + TS Interfaces (Frontend)

---

### Zusammenfassung: Was wir gelernt haben

#### ✅ DO's (aus V2.0)

1. **Sequential Workflow mit klaren Schritten**
2. **Tool-Konzept als Kern-Dimension**
3. **Material-per-Tool (nicht global)**
4. **Progress Indicator mit Validation**
5. **Hierarchische Results-Darstellung**

#### ❌ DON'Ts (aus V3.x)

1. **Niemals essentielle Konzepte weglassen**
2. **Keine Over-Simplification**
3. **Keine Fragmentierung ohne Mehrwert (Tabs)**
4. **Keine Placeholders als Features**
5. **Keine externe UI-Libraries ohne Evaluierung**

#### 🎯 Ziel für V4.0

**"V2.0 Flow + V3.0 Design + Prototyp Components + Neue Features"**

```
V2.0 Sequential Flow
  +
V3.0 Farb-System & Hierarchie
  +
Prototyp Design System (v0.3_production)
  +
DELTA REQUEST Features (Coating, Surface Quality, Expert Mode)
  +
Backend-Integration (Real Calculations)
  +
Export-Modul (Fusion 360 Parametric)
  =
V4.0 Production-Ready System
```

---

## 1.3 Architektur-Prinzipien

### AP-1: API-First Design

**Prinzip:**
> "Backend exposed als REST API. Frontend kommuniziert ausschließlich über API."

**Begründung:**
- Klare Separation of Concerns
- Ermöglicht zukünftige Mobile App / CLI
- Testbar unabhängig von Frontend

**Implementation:**
```
Frontend (React) ←→ REST API (FastAPI) ←→ Calculation Engine (V2.0)
                        ↓
                   Database (SQLite/PostgreSQL)
```

**Regeln:**
- ❌ KEIN direkter Zugriff auf Calculation Engine vom Frontend
- ❌ KEINE Business-Logik im Frontend (nur Validierung)
- ✅ Alle Berechnungen im Backend
- ✅ Frontend ist "Dumb Client"

---

### AP-2: NO-TOUCH Calculation Engine

**Prinzip:**
> "V2.0 Berechnungslogik bleibt unverändert. Wrapper-Services abstrahieren API."

**Begründung:**
- V2.0 Berechnungen sind validiert (Prof. Dr.-Ing.)
- Industrie-Standards konform (VDI 3214, DIN 6527)
- Kein Risiko durch Breaking Changes

**Implementation:**
```python
# ❌ NICHT: Calculation Engine direkt ändern
def calculate_vc_old(...):
    # Alte Formel

# ✅ STATTDESSEN: Wrapper Service
class CalculationService:
    def calculate_vc_with_coating(self, ...):
        base_vc = calculation_engine.calculate_vc(...)  # V2.0 unverändert
        coated_vc = self._apply_coating_factor(base_vc, coating)
        return coated_vc
```

**Erlaubte Änderungen:**
- ✅ Neue Wrapper-Funktionen (z.B. für Coating)
- ✅ Neue Validierungs-Regeln
- ✅ Neue API-Endpoints

**Verbotene Änderungen:**
- ❌ Änderungen an Kern-Formeln
- ❌ Änderungen an V2.0 Funktionen
- ❌ Entfernen von Parametern

---

### AP-3: Progressive Disclosure

**Prinzip:**
> "Basis-Features zuerst. Experten-Features versteckt bis benötigt."

**UX-Hierarchie:**
```
Level 1: Basis-Workflow (95% der User)
├─ Import Tools
├─ Select Materials
├─ Select Operations
└─ View Results

Level 2: Export-Features (60% der User)
└─ Export to Fusion / CSV / PDF

Level 3: Expert Mode (10% der User)
├─ Individual Parameter Override (ae, ap, fz)
├─ Entry Parameters (vf_ramp, vf_plunge, ramp_angle)
└─ Mathematical Workbook (10-Phasen-Detail)
```

**Implementation:**
```tsx
// Basis-UI immer sichtbar
<BasicWorkflow />

// Expert Mode hinter Toggle
{expertMode && <ExpertPanel />}

// Workbook hinter Tab
<Tabs>
  <Tab>Results</Tab>
  <Tab>Workbook</Tab>  {/* Versteckt für Anfänger */}
</Tabs>
```

---

### AP-4: Dark Theme Only

**Prinzip:**
> "Ein dunkles Theme mit 3 Kontrast-Modi. Kein Light Theme."

**Begründung:**
- CNC-Umgebung: Oft in dunklen Werkstätten
- Reduziert Augenbelastung
- Prototyp-Validierung: User-Feedback positiv

**Kontrast-Modi:**
```
Medium:   Niedrigster Kontrast (borders: 0.06/0.12/0.18)
Balanced: Standard (borders: 0.08/0.14/0.22) ← DEFAULT
High:     Höchster Kontrast (borders: 0.08/0.16/0.24)
```

**NO Light Theme!**
- Vereinfacht Maintenance
- Fokussiert Design-Aufwand
- User-Präferenz klar

---

### AP-5: Typisierung & Validierung

**Prinzip:**
> "Strong Types im Backend (Pydantic) und Frontend (TypeScript). Runtime-Validierung."

**Backend (Pydantic):**
```python
class Tool(BaseModel):
    tool_id: str = Field(..., min_length=1, max_length=50)
    DC: float = Field(..., gt=0, le=300)  # 0 < DC ≤ 300 mm
    NOF: int = Field(..., ge=1, le=12)     # 1 ≤ NOF ≤ 12

    @validator('DC')
    def validate_DC(cls, v, values):
        if 'DCX' in values and v > values['DCX']:
            raise ValueError('DC must be ≤ DCX')
        return v
```

**Frontend (TypeScript):**
```typescript
interface Tool {
  tool_id: string;
  DC: number;
  NOF: number;
  // ... (types match Pydantic)
}

// Runtime Validation (zod)
const toolSchema = z.object({
  tool_id: z.string().min(1).max(50),
  DC: z.number().positive().max(300),
  NOF: z.number().int().min(1).max(12),
});
```

---

### AP-6: Performance Budget

**Prinzip:**
> "Definierte Performance-Ziele für alle Operationen."

**Budgets:**
```
Tool Import (.tools):     < 1s   (für 50 Tools)
Calculation (100 Presets): < 2s   (95th percentile)
Results Rendering:         < 500ms (Initial Load)
Export (Fusion .tools):    < 3s   (für 50 Tools × 10 Presets)
Page Load (First Paint):   < 1.5s
```

**Implementation:**
- Async Processing für lange Operationen (Celery)
- Pagination für Results (50 pro Page)
- Lazy Loading für Workbook
- Memoization für teure Berechnungen

---

### AP-7: Accessibility (WCAG 2.1 Level AA)

**Prinzip:**
> "App ist bedienbar für User mit Behinderungen."

**Requirements:**
- ✅ Tastatur-Navigation (Tab-Order)
- ✅ Screen-Reader-Support (ARIA Labels)
- ✅ Farb-Kontrast ≥ 4.5:1 (Text auf Background)
- ✅ Focus-Indicator sichtbar
- ✅ Keine rein visuelle Information

**Tested mit:**
- Chrome DevTools Lighthouse
- axe DevTools
- NVDA Screen Reader (Windows)
- VoiceOver (macOS)

---

### AP-8: Testbarkeit

**Prinzip:**
> "Jede Komponente/Funktion ist isoliert testbar."

**Test-Coverage-Ziele:**
```
Backend:
  - Unit Tests:       > 90%
  - Integration Tests: > 80%
  - E2E Tests:         > 60%

Frontend:
  - Component Tests:  > 85%
  - Integration Tests: > 70%
  - E2E Tests (Playwright): > 50%
```

**Test-Strategie:**
- Jest (Backend Unit Tests)
- pytest (Backend Unit Tests)
- Vitest (Frontend Unit Tests)
- Testing Library (Component Tests)
- Playwright (E2E)

---

### AP-9: Dokumentation-as-Code

**Prinzip:**
> "Code dokumentiert sich selbst. API-Docs automatisch generiert."

**Tools:**
- **Backend:** FastAPI → OpenAPI/Swagger (automatisch)
- **Frontend:** TSDoc → TypeDoc
- **Components:** Storybook (später)

**Beispiel:**
```python
@router.post("/calculate", response_model=CalculationResult)
async def calculate_presets(
    request: CalculationRequest
) -> CalculationResult:
    """
    Calculate cutting parameters for tool/material/operation combinations.

    Args:
        request: CalculationRequest with tools, materials, operations

    Returns:
        CalculationResult with presets, status, warnings

    Raises:
        ValidationError: If input data invalid
        CalculationError: If calculation fails

    Example:
        POST /api/calculate
        {
          "tools": ["T1"],
          "materials": ["ALU"],
          "operations": ["FACE_ROUGH"]
        }
    """
    ...
```

---

### AP-10: Zero External UI Libraries

**Prinzip:**
> "Keine externen UI-Component-Libraries (shadcn/ui, MUI, etc.). Eigene Komponenten."

**Begründung (Lessons Learned):**
- shadcn/ui Disaster in V3.0
- Overhead durch 20+ radix-ui packages
- Design-Inkonsistenzen
- Schwer zu customizen

**Erlaubt:**
- React (Framework)
- Tailwind CSS (Utility Classes)
- Headless-Libraries für Logic (z.B. @tanstack/react-table)

**Verboten:**
- shadcn/ui
- Material-UI (MUI)
- Ant Design
- Chakra UI
- Jede andere Component-Library

**Implementation:**
- Eigene Komponenten basierend auf Prototyp
- `components/` folder mit Slider, Table, Button, etc.
- Design-System aus v0.3_production

---

## 1.4 Technologie-Stack

### Backend

**Core:**
```
Python:    3.11+
Framework: FastAPI 0.104+
ASGI:      Uvicorn
Validation: Pydantic 2.5+
```

**Database:**
```
Dev/Testing:   SQLite 3.40+
Production:    PostgreSQL 15+ (optional)
ORM:           SQLAlchemy 2.0+
Migrations:    Alembic
```

**Async Processing:**
```
Task Queue: Celery 5.3+
Broker:     Redis 7.0+
Backend:    Redis
```

**File Processing:**
```
ZIP:  zipfile (stdlib)
JSON: orjson (faster than stdlib json)
CSV:  pandas
PDF:  reportlab
```

**Testing:**
```
Unit:        pytest 7.4+
Coverage:    pytest-cov
Fixtures:    pytest-fixtures
HTTP Tests:  httpx (async client)
```

---

### Frontend

**Core:**
```
React:      18.2+
TypeScript: 5.3+
Build:      Vite 5.0+
```

**Styling:**
```
Tailwind CSS: 3.4+
CSS Modules:  ✅ (für Komponenten)
CSS Variables: ✅ (Design Tokens)
```

**State Management:**
```
Local State:  Zustand 4.4+
Server State: @tanstack/react-query 5.0+
Form State:   React Hook Form 7.48+
```

**HTTP Client:**
```
Fetch API (native)
+ @tanstack/react-query für Caching
```

**Validation:**
```
zod 3.22+ (Runtime Validation)
```

**Testing:**
```
Unit:        Vitest 1.0+
Component:   @testing-library/react 14.0+
E2E:         Playwright 1.40+
```

---

### Development Tools

**Code Quality:**
```
Linter (Backend):  ruff (Python)
Linter (Frontend): ESLint + typescript-eslint
Formatter:         Prettier (Frontend), Black (Backend)
Pre-Commit:        husky + lint-staged
```

**Type Checking:**
```
Backend:  mypy (strict mode)
Frontend: tsc --noEmit
```

**Version Control:**
```
Git
Monorepo: ✅ (apps/web, apps/api)
```

**CI/CD:**
```
GitHub Actions (optional)
├─ Lint + Type Check
├─ Unit Tests
├─ Build
└─ Deploy (optional)
```

---

### Design System

**Fonts:**
```
Primary:   Inter Variable (Google Fonts)
Headline:  Work Sans (Google Fonts)
Mono:      Fira Code (Google Fonts)
```

**Icons:**
```
Lucide React (Tree-shakable, MIT License)
```

**Design Tokens:**
```
Source:  design-system@v0.3_production.json
Format:  CSS Variables (design-tokens.css)
Themes:  dark-medium, dark-balanced, dark-high
```

---

### Infrastructure (Optional - Deployment)

**Containerization:**
```
Docker:        24.0+
Compose:       v2
Multi-Stage:   ✅ (Frontend + Backend separate images)
```

**Hosting (Example):**
```
Frontend:   Vercel / Netlify / Cloudflare Pages
Backend:    Fly.io / Railway / Render
Database:   Supabase / PlanetScale
Redis:      Upstash / Redis Cloud
```

---

### Why These Choices?

**FastAPI:**
- ✅ Automatische OpenAPI/Swagger Docs
- ✅ Pydantic-Integration (Types + Validation)
- ✅ Async-Support (für Celery)
- ✅ Beste Python Performance (nur hinter Rust Frameworks)

**Vite:**
- ✅ Extrem schnelle HMR (< 50ms)
- ✅ Natives ES Modules (kein Bundling in Dev)
- ✅ Optimized Production Build
- ✅ TypeScript First-Class Support

**Zustand:**
- ✅ Minimalistisch (< 1kB)
- ✅ Kein Boilerplate (vs Redux)
- ✅ TypeScript-Friendly
- ✅ Devtools-Support

**React Query:**
- ✅ Server State Management
- ✅ Automatisches Caching
- ✅ Optimistic Updates
- ✅ Background Refetching

**Tailwind CSS:**
- ✅ Utility-First (schnelle Iteration)
- ✅ PurgeCSS (kleiner Bundle)
- ✅ Design Tokens als Config
- ✅ Responsive Utilities

---

## 1.5 Projektstruktur-Übersicht

### Monorepo-Struktur

```
cnc-calculator/
├── apps/
│   ├── web/                    # Frontend (React + Vite)
│   │   ├── src/
│   │   │   ├── components/     # UI-Komponenten
│   │   │   ├── features/       # Feature-spezifische Komponenten
│   │   │   ├── pages/          # Screen-Komponenten
│   │   │   ├── stores/         # Zustand Stores
│   │   │   ├── hooks/          # Custom React Hooks
│   │   │   ├── services/       # API Client
│   │   │   ├── types/          # TypeScript Interfaces
│   │   │   ├── styles/         # Global Styles + Tokens
│   │   │   └── utils/          # Helper Functions
│   │   ├── public/
│   │   ├── index.html
│   │   ├── vite.config.ts
│   │   └── package.json
│   │
│   └── api/                    # Backend (FastAPI)
│       ├── src/
│       │   ├── api/            # API Routes
│       │   ├── services/       # Business Logic
│       │   ├── models/         # Pydantic Models
│       │   ├── db/             # Database
│       │   ├── core/           # Config, Logging
│       │   ├── calculation/    # V2.0 Wrapper
│       │   └── utils/          # Helpers
│       ├── tests/
│       ├── alembic/            # DB Migrations
│       ├── main.py             # Entry Point
│       ├── pyproject.toml
│       └── requirements.txt
│
├── packages/                   # Shared Packages (optional)
│   └── types/                  # Shared TS/Python Types
│
├── docs/                       # Documentation
│   ├── architecture/
│   ├── api/                    # API Docs (auto-generated)
│   └── user-guide/
│
├── tools/                      # Build Scripts
│   ├── generate-types.py       # Pydantic → TypeScript
│   └── validate-tokens.js      # Design Token Validator
│
├── .github/                    # CI/CD
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
│
├── docker-compose.yml          # Dev Environment
├── README.md
└── package.json                # Root package.json (workspace)
```

---

### Frontend Struktur (apps/web/src/)

```
src/
├── components/                 # Wiederverwendbare UI-Komponenten
│   ├── ui/                     # Basis-Komponenten (Prototyp-basiert)
│   │   ├── Slider/
│   │   │   ├── Slider.tsx
│   │   │   ├── Slider.css
│   │   │   └── Slider.test.tsx
│   │   ├── CompactSlider/
│   │   │   ├── CompactSlider.tsx
│   │   │   ├── CompactSlider.css
│   │   │   └── CompactSlider.test.tsx
│   │   ├── Table/
│   │   │   ├── Table.tsx
│   │   │   ├── Table.css
│   │   │   └── Table.test.tsx
│   │   ├── Button/
│   │   ├── Card/
│   │   ├── Badge/
│   │   └── Modal/
│   │
│   ├── layout/                 # Layout-Komponenten
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── ProgressStepper.tsx
│   │   └── SummaryPanel.tsx
│   │
│   └── domain/                 # Domänen-spezifische Komponenten
│       ├── ToolCard.tsx
│       ├── MaterialCard.tsx
│       ├── OperationCard.tsx
│       └── PresetRow.tsx
│
├── features/                   # Feature-Module
│   ├── import/
│   │   ├── ImportScreen.tsx
│   │   ├── FileUploader.tsx
│   │   └── ToolParser.ts
│   ├── selection/
│   │   ├── ToolSelectionScreen.tsx
│   │   ├── MaterialSelectionScreen.tsx
│   │   └── OperationSelectionScreen.tsx
│   ├── calculation/
│   │   ├── CalculationProgressScreen.tsx
│   │   └── useCalculation.ts
│   ├── results/
│   │   ├── ResultsScreen.tsx
│   │   ├── ResultsTable.tsx
│   │   └── ResultsFilters.tsx
│   ├── export/
│   │   ├── ExportDialog.tsx
│   │   └── ExportService.ts
│   ├── expert/
│   │   ├── ExpertModePanel.tsx
│   │   ├── ParameterOverride.tsx
│   │   └── ExpertSliders.tsx
│   └── workbook/
│       ├── WorkbookTab.tsx
│       └── WorkbookPhases.tsx
│
├── pages/                      # Screen-Container
│   ├── MainWorkflow.tsx        # Haupt-6-Screen-Workflow
│   ├── ExpertMode.tsx          # Expert Mode View
│   └── Workbook.tsx            # Workbook View
│
├── stores/                     # Zustand State Stores
│   ├── useToolStore.ts         # Tools State
│   ├── useMaterialStore.ts     # Materials State
│   ├── useOperationStore.ts    # Operations State
│   ├── useResultsStore.ts      # Results State
│   ├── useExpertStore.ts       # Expert Mode State
│   └── useWorkflowStore.ts     # Workflow State (current step, etc.)
│
├── hooks/                      # Custom React Hooks
│   ├── useTheme.ts             # Theme Context Hook
│   ├── useCalculation.ts       # Calculation Hook (React Query)
│   ├── useExport.ts            # Export Hook
│   └── useDebounce.ts          # Utility Hook
│
├── services/                   # API Client
│   ├── api.ts                  # Axios/Fetch Setup
│   ├── toolService.ts          # Tool API Calls
│   ├── calculationService.ts   # Calculation API Calls
│   └── exportService.ts        # Export API Calls
│
├── types/                      # TypeScript Interfaces
│   ├── tool.ts
│   ├── material.ts
│   ├── operation.ts
│   ├── preset.ts
│   ├── calculation.ts
│   └── export.ts
│
├── styles/                     # Global Styles
│   ├── design-tokens.css       # CSS Variables (v0.3_production)
│   ├── globals.css             # Global Styles
│   ├── reset.css               # CSS Reset
│   └── tailwind.css            # Tailwind Imports
│
├── utils/                      # Helper Functions
│   ├── format.ts               # Formatierung (Zahlen, Dates)
│   ├── validation.ts           # Client-Side Validation
│   └── color.ts                # Color Utilities
│
├── context/                    # React Context
│   └── ThemeContext.tsx        # Theme + Kontrast Context
│
├── App.tsx                     # Root Component
├── main.tsx                    # Entry Point
└── vite-env.d.ts               # Vite Types
```

---

### Backend Struktur (apps/api/src/)

```
src/
├── api/                        # API Routes (FastAPI Routers)
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── tools.py            # POST /tools/parse, GET /tools
│   │   ├── calculation.py      # POST /calculate
│   │   ├── export.py           # POST /export/fusion, /export/csv
│   │   └── health.py           # GET /health
│   └── deps.py                 # Dependency Injection
│
├── services/                   # Business Logic Layer
│   ├── tool_service.py         # Tool-Logik
│   ├── calculation_service.py  # Wrapper für V2.0 Engine
│   ├── expert_service.py       # Expert Mode Logik
│   ├── export_service.py       # Export-Logik
│   └── validation_service.py   # 8 Checks Validation
│
├── models/                     # Pydantic Models
│   ├── tool.py                 # Tool, Geometry, Holder
│   ├── material.py             # Material, MaterialType
│   ├── operation.py            # Operation, OperationType
│   ├── preset.py               # Preset, CuttingParams
│   ├── calculation.py          # CalculationRequest, CalculationResult
│   ├── export.py               # ExportRequest, FusionExport
│   └── expert.py               # ExpertModeOverrides
│
├── db/                         # Database
│   ├── models.py               # SQLAlchemy Models
│   ├── session.py              # Database Session
│   └── init_db.py              # Database Init
│
├── core/                       # Core Config
│   ├── config.py               # Settings (Pydantic Settings)
│   ├── logging.py              # Logging Setup
│   └── security.py             # Auth (später)
│
├── calculation/                # V2.0 Calculation Engine Wrapper
│   ├── engine.py               # Wrapper für V2.0
│   ├── formulas.py             # V2.0 Formeln (NO-TOUCH!)
│   ├── coating.py              # Coating-Faktoren
│   ├── surface_quality.py      # Surface Quality Adjustments
│   ├── chip_analysis.py        # Chip Temperature
│   └── l_d_stability.py        # L/D Reductions
│
├── utils/                      # Helpers
│   ├── file_utils.py           # ZIP, JSON Parsing
│   ├── fusion_utils.py         # Fusion .tools Generator
│   ├── csv_utils.py            # CSV Export
│   └── validation_utils.py     # Validation Helpers
│
├── schemas/                    # Request/Response Schemas (Pydantic)
│   ├── tool_schemas.py
│   ├── calculation_schemas.py
│   └── export_schemas.py
│
└── main.py                     # FastAPI App Entry Point
```

---

### Key Files

**Frontend:**
```
apps/web/src/styles/design-tokens.css    # CSS Variables (30 Tokens)
apps/web/src/components/ui/Slider/       # Slider-Komponente (Prototyp)
apps/web/src/pages/MainWorkflow.tsx      # 6-Screen-Workflow
apps/web/src/stores/useWorkflowStore.ts  # Workflow State
```

**Backend:**
```
apps/api/src/calculation/engine.py       # V2.0 Wrapper
apps/api/src/services/calculation_service.py  # Calculation Logic
apps/api/src/api/v1/calculation.py       # Calculation Endpoint
apps/api/src/models/calculation.py       # Calculation Models
```

**Design:**
```
docs/design-system@v0.3_production.json  # Design Tokens (Source of Truth)
```

---

### Naming Conventions

**Files:**
```
React Components:  PascalCase (ToolCard.tsx)
CSS Modules:       PascalCase (ToolCard.module.css)
Utilities:         camelCase (formatNumber.ts)
Types:             camelCase (tool.ts)
Python Modules:    snake_case (tool_service.py)
Python Classes:    PascalCase (ToolService)
```

**Variables:**
```typescript
// TypeScript
const toolId: string          // camelCase
const MAX_TOOLS = 50          // UPPER_CASE (constants)
interface Tool {}             // PascalCase
type ToolId = string          // PascalCase
```

```python
# Python
tool_id: str                  # snake_case
MAX_TOOLS = 50                # UPPER_CASE (constants)
class Tool(BaseModel):        # PascalCase
```

---

### File Size Guidelines

**Components:**
- Max 300 lines (inkl. Styles)
- Bei > 300 Zeilen: Split in Sub-Components

**Services:**
- Max 400 lines
- Bei > 400 Zeilen: Split in separate Modules

**Stores:**
- Max 200 lines
- Ein Store pro Domain (Tool, Material, etc.)

---

# TEIL 2: DOMÄNENMODELL & BERECHNUNGSLOGIK

## 2.1 Berechnungs-Workflow (10 Phasen)

### Übersicht

Der Berechnungs-Workflow besteht aus **10 aufeinanderfolgenden Phasen**, die für jedes Tool+Material+Operation-Preset durchlaufen werden.

```
Phase 1: Input Parameters (Tool Geometry + Material + Operation)
   ↓
Phase 2: Cutting Speed (vc) + Coating Factor
   ↓
Phase 3: Spindle Speed (n)
   ↓
Phase 4: Chip Load (fz) + Dry Machining Correction
   ↓
Phase 5: Feed Rate (vf)
   ↓
Phase 6: Engagement (ae, ap) + Surface Quality Adjustment
   ↓
Phase 7: Power & Torque Analysis
   ↓
Phase 8: Thermal Analysis (Chip Temperature)
   ↓
Phase 9: Chip Formation Prediction
   ↓
Phase 10: L/D Stability Check + Warnings
```

---

### Phase 1: Input Parameters

**Eingangsparameter sammeln:**

```python
# Tool Geometry
DC: float      # Cutting Diameter [mm]
LCF: float     # Length of Cut [mm]
NOF: int       # Number of Flutes
DCX: float     # Max Cutting Diameter [mm]
OAL: float     # Overall Length [mm]
SFDM: float    # Shank Diameter [mm]

# Material
material: MaterialType  # SOFTWOOD, HARDWOOD, ALU, BRASS, ACRYLIC, STEEL_MILD, STEEL_STAINLESS

# Operation
operation: OperationType  # FACE_ROUGH, FACE_FINISH, SLOT_ROUGH, ...

# Optional Modifiers
coating: CoatingType | None         # None, TIN, TIALN, ALTIN, DIAMOND, CARBIDE
surface_quality: SurfaceQuality     # ROUGHING, STANDARD, FINISHING, HIGH_FINISH
dry_machining: bool                 # True/False
```

**Validation:**
- DC > 0 und DC ≤ DCX
- LCF > 0
- NOF ≥ 1 und NOF ≤ 12
- Material + Operation Kombination gültig

---

### Phase 2: Cutting Speed (vc) + Coating Factor

**Formel (V2.0 Basis):**

```python
# Base Cutting Speed (ohne Coating)
vc_base = get_base_vc(material, operation)  # V2.0 Lookup-Table

# Coating Factor Application
if coating == CoatingType.NONE:
    coating_factor = 1.0
elif coating == CoatingType.TIN:
    coating_factor = 1.4   # +40%
elif coating == CoatingType.TIALN:
    coating_factor = 1.6   # +60%
elif coating == CoatingType.ALTIN:
    coating_factor = 1.8   # +80%
elif coating == CoatingType.DIAMOND:
    # Diamond nur für Non-Ferrous (ALU, BRASS, COPPER, PLASTIC)
    if material in [MaterialType.ALU, MaterialType.BRASS, MaterialType.ACRYLIC]:
        coating_factor = 2.2  # +120%
    else:
        raise ValidationError("Diamond coating only for non-ferrous materials")
elif coating == CoatingType.CARBIDE:
    coating_factor = 1.5   # +50%

# Final vc
vc = vc_base * coating_factor  # [m/min]
```

**Base vc Lookup-Table (Beispiel):**

| Material | FACE_ROUGH | FACE_FINISH | SLOT_ROUGH | SLOT_FINISH |
|----------|-----------|-------------|------------|-------------|
| ALU      | 377       | 400         | 300        | 350         |
| BRASS    | 200       | 220         | 160        | 180         |
| STEEL_MILD | 150     | 170         | 120        | 140         |
| STEEL_STAINLESS | 80 | 100        | 60         | 80          |

(Vollständige Tabelle: alle 7 Materialien × 13 Operationen)

---

### Phase 3: Spindle Speed (n)

**Formel:**

```python
n = (vc * 1000) / (math.pi * DC)  # [RPM]
```

**Beispiel:**
```
vc = 377 m/min
DC = 30 mm

n = (377 * 1000) / (π * 30)
n = 377000 / 94.25
n = 4000.09 RPM
```

**Validation:**
- n > 0
- n < MAX_RPM (abhängig von Maschine, z.B. 30000 RPM)

---

### Phase 4: Chip Load (fz) + Dry Machining Correction

**Formel (V2.0 Basis):**

```python
# Base fz (ohne Dry Correction)
fz_base = get_base_fz(material, operation, DC)  # V2.0 Lookup

# Dry Machining Correction
if dry_machining:
    dry_factor = get_dry_factor(material)  # Material-spezifisch
    fz = fz_base * dry_factor
else:
    fz = fz_base  # [mm]
```

**Dry Machining Factors:**

| Material | Dry Factor | Begründung |
|----------|-----------|-------------|
| SOFTWOOD | 1.0 | Keine Korrektur (natürlich trocken) |
| HARDWOOD | 1.0 | Keine Korrektur |
| PLASTIC (ACRYLIC) | 0.9 | -10% (Hitze-Probleme) |
| ALU | 0.85 | -15% (Verschweißung vermeiden) |
| BRASS | 0.9 | -10% |
| COPPER | 0.85 | -15% |
| STEEL_MILD | 0.7 | -30% (hohe Hitze) |
| STEEL_STAINLESS | 0.65 | -35% (noch höhere Hitze) |

**Validation:**
- fz > 0
- fz < MAX_FZ (z.B. 0.5 mm)

---

### Phase 5: Feed Rate (vf)

**Formel:**

```python
vf = n * fz * NOF  # [mm/min]
```

**Beispiel:**
```
n = 4000 RPM
fz = 0.09 mm
NOF = 3

vf = 4000 * 0.09 * 3
vf = 1080 mm/min
```

**Derived Entry Parameters (DELTA REQUEST Feature):**

```python
# Entry Feed (Rampen-Eintritt)
vf_entry = vf * 0.5     # 50% von vf (Standard)

# Ramp Feed
vf_ramp = vf * 0.5      # 50%

# Plunge Feed (Senk-Eintritt)
vf_plunge = vf / NOF    # vf dividiert durch Anzahl Schneiden (Standard)

# Exit Feed
vf_exit = vf * 1.0      # 100% (keine Reduktion)

# Transition Feed
vf_transition = vf * 1.0  # 100%
```

**Ramp Angle:**
```python
ramp_angle = 2.0  # Grad (Standard für Metalle)
# Kann überschrieben werden im Expert Mode
```

---

### Phase 6: Engagement (ae, ap) + Surface Quality Adjustment

#### 6.1 ap (Axial Depth of Cut) - Dynamische Referenz-Logik

**DELTA REQUEST Feature: Intelligente ap-Referenz**

```python
def calculate_ap(tool: Tool, operation: OperationType, surface_quality: SurfaceQuality) -> tuple[float, str]:
    """
    Berechnet ap basierend auf dynamischer Referenz-Logik.

    Priority-Hierarchie:
    1. Expert Mode Manual Override (wenn gesetzt)
    2. Operation Type Rules
    3. L/D Ratio Rules

    Returns:
        (ap_value, ap_reference)  # z.B. (1.5, "LCF") oder (7.5, "DC")
    """

    # Step 1: Berechne L/D Ratio
    L_D_ratio = tool.LCF / tool.DC

    # Step 2: Operation-spezifische Logik
    if operation in [OperationType.FACE_ROUGH, OperationType.FACE_FINISH]:
        # FACE operations immer DC-basiert
        ap_reference = "DC"
        ap_factor = 0.25  # 25% von DC (Standard für Face)

    elif operation == OperationType.SLOT_FULL:
        # SLOT_FULL immer DC-basiert
        ap_reference = "DC"
        ap_factor = 0.5   # 50% von DC

    elif operation == OperationType.SPECIAL_ADAPTIVE:
        # ADAPTIVE immer LCF-basiert (nutzt volle Schneidenlänge)
        ap_reference = "LCF"
        ap_factor = 0.3   # 30% von LCF

    else:
        # Step 3: L/D Ratio-basierte Entscheidung für andere Ops
        if L_D_ratio < 1.0:
            # Kurze Tools (L/D < 1.0) → DC-Referenz
            ap_reference = "DC"
            ap_factor = 0.1875  # 18.75% von DC
        else:
            # Lange Tools (L/D ≥ 1.0) → LCF-Referenz
            ap_reference = "LCF"
            ap_factor = 0.1875  # 18.75% von LCF

    # Step 4: Berechne Basis-ap
    if ap_reference == "DC":
        ap_base = tool.DC * ap_factor
    else:  # "LCF"
        ap_base = tool.LCF * ap_factor

    # Step 5: Surface Quality Adjustment
    sq_factor = get_surface_quality_factor(surface_quality, "ap")
    ap_final = ap_base * sq_factor

    return (ap_final, ap_reference)
```

**Surface Quality Factors (ap):**

| Surface Quality | ap Adjustment | ae Adjustment | vf Adjustment |
|----------------|---------------|---------------|---------------|
| ROUGHING       | +0%           | +0%           | +20%          |
| STANDARD       | +0%           | +0%           | +0%           |
| FINISHING      | -20%          | -30%          | -20%          |
| HIGH_FINISH    | -40%          | -50%          | -40%          |

**Beispiele:**

```python
# Tool: DC=30mm, LCF=8mm, L/D=0.27
# Operation: FACE_ROUGH
→ ap_reference = "DC" (wegen Face Operation)
→ ap_base = 30 * 0.25 = 7.5 mm
→ ap_final = 7.5 mm (Surface Quality: STANDARD)

# Tool: DC=6mm, LCF=25mm, L/D=4.17
# Operation: SLOT_ROUGH
→ ap_reference = "LCF" (wegen L/D ≥ 1.0)
→ ap_base = 25 * 0.1875 = 4.69 mm
→ ap_final = 4.69 mm

# Tool: DC=6mm, LCF=25mm
# Operation: FACE_FINISH, Surface Quality: FINISHING
→ ap_reference = "DC"
→ ap_base = 6 * 0.25 = 1.5 mm
→ ap_final = 1.5 * 0.8 = 1.2 mm  (Surface Quality -20%)
```

---

#### 6.2 ae (Radial Width of Cut)

**Formel:**

```python
def calculate_ae(tool: Tool, operation: OperationType, surface_quality: SurfaceQuality) -> float:
    """
    Berechnet ae (radiale Zustellung).
    Immer DC-basiert!
    """

    # Operation-spezifischer Faktor
    ae_factor = get_ae_factor(operation)

    # Beispiele:
    # FACE_ROUGH:  ae_factor = 0.25  (25% von DC)
    # SLOT_FULL:   ae_factor = 1.0   (100% von DC - voller Nutbreite)
    # CONTOUR_*:   ae_factor = 0.1   (10% von DC - Finishing)

    ae_base = tool.DC * ae_factor

    # Surface Quality Adjustment
    sq_factor = get_surface_quality_factor(surface_quality, "ae")
    ae_final = ae_base * sq_factor

    return ae_final
```

**ae Factors pro Operation:**

| Operation | ae Factor | Beschreibung |
|-----------|-----------|--------------|
| FACE_ROUGH | 0.25 | 25% DC |
| FACE_FINISH | 0.25 | 25% DC |
| SLOT_ROUGH | 1.0 | 100% DC (voller Slot) |
| SLOT_FINISH | 1.0 | 100% DC |
| SLOT_FULL | 1.0 | 100% DC |
| SLOT_TROCHOIDAL | 0.1 | 10% DC (kleine Kreise) |
| CONTOUR_2D | 0.1 | 10% DC (Finishing) |
| CONTOUR_3D | 0.1 | 10% DC |
| SPECIAL_ADAPTIVE | 0.4 | 40% DC (variable) |
| SPECIAL_PLUNGE | 0.0 | 0% (nur axial) |
| SPECIAL_DRILL | 0.0 | 0% (nur axial) |
| GEO_CHAMFER | 0.05 | 5% DC (minimal) |
| GEO_RADIUS | 0.05 | 5% DC |

---

### Phase 7: Power & Torque Analysis

**Formeln (V2.0 Basis, vereinfacht):**

```python
# Specific Cutting Force (kc) [N/mm²]
kc = get_kc(material)  # Material-spezifisch

# Material Removal Rate (MRR) [cm³/min]
MRR = (ae * ap * vf) / 1000  # ae, ap in mm, vf in mm/min

# Cutting Power (Pc) [kW]
Pc = (kc * ae * ap * vf) / (60 * 1000000)

# Torque (M) [Nm]
M = (Pc * 9550) / n  # n in RPM

# Spindle Power (required) [kW]
P_spindle = Pc / efficiency  # efficiency ≈ 0.8 (80%)
```

**kc Values (Beispiel):**

| Material | kc [N/mm²] |
|----------|-----------|
| SOFTWOOD | 40 |
| HARDWOOD | 80 |
| ACRYLIC | 90 |
| ALU | 600 |
| BRASS | 800 |
| COPPER | 1000 |
| STEEL_MILD | 1800 |
| STEEL_STAINLESS | 2200 |

**Validation:**
```python
if P_spindle > MAX_SPINDLE_POWER:
    warnings.append(f"Spindle power {P_spindle:.1f}kW exceeds max {MAX_SPINDLE_POWER}kW")
    status = Status.WARNING
```

---

### Phase 8: Thermal Analysis (Chip Temperature)

**DELTA REQUEST Feature: Chip Temperature Prediction**

**Formel (vereinfacht):**

```python
def calculate_chip_temperature(material: MaterialType, vc: float, fz: float, ap: float) -> float:
    """
    Berechnet geschätzte Chip-Temperatur.
    Basiert auf empirischen Formeln.
    """

    # Material-spezifische Konstanten
    k_thermal = get_thermal_constant(material)

    # Chip Temperature Formel
    T_chip = k_thermal * (vc**0.6) * (fz**0.3) * (ap**0.2)  # [°C]

    return T_chip
```

**Thermal Constants:**

| Material | k_thermal | Max Safe Temp [°C] |
|----------|-----------|-------------------|
| SOFTWOOD | 0.5 | 200 |
| HARDWOOD | 0.7 | 250 |
| ACRYLIC | 1.2 | 150 (niedrig!) |
| ALU | 2.0 | 400 |
| BRASS | 2.2 | 450 |
| COPPER | 2.5 | 500 |
| STEEL_MILD | 4.0 | 600 |
| STEEL_STAINLESS | 5.0 | 700 |

**Warnings:**

```python
if T_chip > max_safe_temp:
    warnings.append(
        f"Chip temperature {T_chip:.0f}°C exceeds safe limit {max_safe_temp}°C. "
        "Consider: (1) Reduce vc, (2) Enable coolant, (3) Use coating"
    )
    status = Status.WARNING

if T_chip > max_safe_temp * 1.2:
    status = Status.ERROR  # Kritisch!
```

---

### Phase 9: Chip Formation Prediction

**DELTA REQUEST Feature: Chip Type Analysis**

```python
def predict_chip_formation(material: MaterialType, operation: OperationType, h: float) -> ChipType:
    """
    Vorhersage der Spanform basierend auf Material, Operation, und Spandicke.

    h = Spandicke = fz * sin(angle)  (vereinfacht: h ≈ fz für Face Operations)
    """

    if material in [MaterialType.ALU, MaterialType.BRASS, MaterialType.COPPER]:
        # Duktile Materialien
        if h < 0.05:
            chip_type = ChipType.CONTINUOUS_THIN  # Problematisch: Verschweißung
        elif h < 0.15:
            chip_type = ChipType.CONTINUOUS_OPTIMAL  # Optimal
        else:
            chip_type = ChipType.CONTINUOUS_THICK  # Schwer zu brechen

    elif material in [MaterialType.STEEL_MILD, MaterialType.STEEL_STAINLESS]:
        # Stähle
        if h < 0.03:
            chip_type = ChipType.SHEAR  # Zu dünn
        elif h < 0.10:
            chip_type = ChipType.SEGMENTED_OPTIMAL  # Optimal
        else:
            chip_type = ChipType.SEGMENTED_HEAVY  # Zu dick

    else:  # Holz, Kunststoff
        chip_type = ChipType.DISCONTINUOUS  # Brüchig

    return chip_type
```

**Chip Type Descriptions:**

| Chip Type | Beschreibung | Empfehlung |
|-----------|--------------|------------|
| CONTINUOUS_THIN | Dünne, lange Späne | Gefahr: Verschweißung. → Erhöhe fz |
| CONTINUOUS_OPTIMAL | Mittlere Späne | Optimal! |
| CONTINUOUS_THICK | Dicke, schwer zu brechende Späne | → Reduziere fz |
| SEGMENTED_OPTIMAL | Segmentierte Späne (Stahl) | Optimal! |
| SHEAR | Scherspäne (zu dünn) | → Erhöhe fz |
| DISCONTINUOUS | Brüchige Späne (Holz) | Normal |

**Warnings:**
```python
if chip_type == ChipType.CONTINUOUS_THIN:
    warnings.append("Thin chips may cause welding. Increase fz.")
```

---

### Phase 10: L/D Stability Check + Warnings

**DELTA REQUEST Feature: L/D Ratio Reductions**

```python
def apply_ld_stability_reductions(tool: Tool, vc: float, fz: float, ae: float, ap: float) -> dict:
    """
    Reduziert Parameter basierend auf L/D Ratio für Werkzeug-Stabilität.
    """

    L_D_ratio = tool.LCF / tool.DC

    if L_D_ratio <= 3.0:
        # Kurze, stabile Tools → Keine Reduktion
        reduction_factor = 1.0
        status = "STABLE"

    elif 3.0 < L_D_ratio <= 5.0:
        # Mittlere Länge → Leichte Reduktion
        reduction_factor_vc_fz = 0.8   # -20%
        reduction_factor_ae_ap = 0.9   # -10%
        status = "MODERATE"
        warnings.append("L/D ratio 3.0-5.0: Reduced parameters by 20%/10% for stability")

    elif 5.0 < L_D_ratio <= 8.0:
        # Lange Tools → Starke Reduktion
        reduction_factor_vc_fz = 0.6   # -40%
        reduction_factor_ae_ap = 0.8   # -20%
        status = "UNSTABLE"
        warnings.append("L/D ratio 5.0-8.0: Reduced parameters by 40%/20%. High vibration risk!")

    else:  # L_D_ratio > 8.0
        # Sehr lange Tools → Kritisch
        reduction_factor_vc_fz = 0.4   # -60%
        reduction_factor_ae_ap = 0.7   # -30%
        status = "CRITICAL"
        warnings.append(
            f"L/D ratio {L_D_ratio:.2f} > 8.0: CRITICAL! "
            "Reduced parameters by 60%/30%. Consider shorter tool or special holder."
        )

    # Apply Reductions
    vc_reduced = vc * reduction_factor_vc_fz
    fz_reduced = fz * reduction_factor_vc_fz
    ae_reduced = ae * reduction_factor_ae_ap
    ap_reduced = ap * reduction_factor_ae_ap

    # Recalculate dependent values
    n_reduced = (vc_reduced * 1000) / (math.pi * tool.DC)
    vf_reduced = n_reduced * fz_reduced * tool.NOF

    return {
        "vc": vc_reduced,
        "n": n_reduced,
        "fz": fz_reduced,
        "vf": vf_reduced,
        "ae": ae_reduced,
        "ap": ap_reduced,
        "L_D_ratio": L_D_ratio,
        "stability_status": status,
        "reduction_applied": reduction_factor_vc_fz,
    }
```

**Final Status Determination:**

```python
def determine_final_status(warnings: list, errors: list, L_D_status: str, T_chip: float, max_safe_temp: float) -> Status:
    """
    Finaler Status basierend auf allen Checks.
    """

    if errors:
        return Status.ERROR

    if L_D_status == "CRITICAL" or T_chip > max_safe_temp * 1.2:
        return Status.ERROR

    if L_D_status in ["UNSTABLE", "MODERATE"] or T_chip > max_safe_temp:
        return Status.WARNING

    if warnings:
        return Status.WARNING

    return Status.OK
```

---

### 10-Phasen Workflow: Vollständiges Beispiel

**Input:**
```python
Tool:
  tool_id = "T1"
  DC = 30 mm
  LCF = 8 mm
  NOF = 3
  L_D = 0.27

Material: ALU
Operation: FACE_ROUGH
Coating: TIN
Surface Quality: STANDARD
Dry Machining: False
```

**Durchlauf:**

```
Phase 1: Input Parameters
  → Validated ✓

Phase 2: Cutting Speed
  vc_base = 377 m/min (ALU, FACE_ROUGH)
  coating_factor = 1.4 (TIN)
  vc = 377 * 1.4 = 527.8 m/min

Phase 3: Spindle Speed
  n = (527.8 * 1000) / (π * 30)
  n = 5600 RPM

Phase 4: Chip Load
  fz_base = 0.09 mm
  dry_factor = 1.0 (not dry)
  fz = 0.09 mm

Phase 5: Feed Rate
  vf = 5600 * 0.09 * 3 = 1512 mm/min
  vf_plunge = 1512 / 3 = 504 mm/min
  vf_ramp = 1512 * 0.5 = 756 mm/min

Phase 6: Engagement
  ap: DC-Referenz (Face Operation)
      ap = 30 * 0.25 = 7.5 mm
  ae: ae = 30 * 0.25 = 7.5 mm

Phase 7: Power & Torque
  kc = 600 N/mm² (ALU)
  MRR = (7.5 * 7.5 * 1512) / 1000 = 85.1 cm³/min
  Pc = (600 * 7.5 * 7.5 * 1512) / 60000000 = 0.85 kW
  M = (0.85 * 9550) / 5600 = 1.45 Nm
  P_spindle = 0.85 / 0.8 = 1.06 kW

Phase 8: Thermal Analysis
  T_chip = 2.0 * (527.8^0.6) * (0.09^0.3) * (7.5^0.2)
  T_chip ≈ 180°C (< 400°C safe limit) ✓

Phase 9: Chip Formation
  h = fz = 0.09 mm
  Chip Type: CONTINUOUS_OPTIMAL ✓

Phase 10: L/D Stability
  L_D = 0.27 (< 3.0)
  Status: STABLE
  Reductions: NONE

Final Status: OK ✓
Warnings: []
```

---

## 2.2 Materialien (7 Materialien, Härte-sortiert)

### Material-Hierarchie

**DELTA REQUEST Spezifikation: Sortierung nach Härte (weich → hart)**

```python
class MaterialType(str, Enum):
    SOFTWOOD = "Softwood"               # 1. Weichste
    HARDWOOD = "Hardwood"               # 2.
    ACRYLIC = "Acrylic"                 # 3. (Kunststoff)
    ALUMINIUM = "Aluminium"             # 4.
    BRASS = "Brass"                     # 5.
    STEEL_MILD = "Steel (Mild)"         # 6.
    STEEL_STAINLESS = "Steel (Stainless)"  # 7. Härteste
```

**Warum diese Reihenfolge?**
- Logische Progression für User
- Von einfach zu schwierig
- Beginners starten oben (Holz)
- Experten scrollen nach unten (Stähle)

---

### Material-Eigenschaften

**Tabelle:**

| Material | Härte [HB] | kc [N/mm²] | vc_base [m/min] | Dry Factor | Max Temp [°C] | k_thermal |
|----------|-----------|-----------|----------------|-----------|--------------|-----------|
| Softwood | 20 | 40 | 1000 | 1.0 | 200 | 0.5 |
| Hardwood | 60 | 80 | 800 | 1.0 | 250 | 0.7 |
| Acrylic | 80 | 90 | 600 | 0.9 | 150 | 1.2 |
| Aluminium | 70 | 600 | 377 | 0.85 | 400 | 2.0 |
| Brass | 100 | 800 | 200 | 0.9 | 450 | 2.2 |
| Steel (Mild) | 150 | 1800 | 150 | 0.7 | 600 | 4.0 |
| Steel (Stainless) | 180 | 2200 | 80 | 0.65 | 700 | 5.0 |

---

### Material-Farben (UI)

**Design System (v0.3_production):**

```json
"materials": {
  "softwood": "#f4e4c1",    // Beige
  "hardwood": "#8b6f47",    // Braun
  "plastic": "#60a5fa",     // Blau (für Acrylic)
  "brass": "#fbbf24",       // Gold
  "aluminium": "#94a3b8",   // Grau
  "steel": "#475569",       // Dunkelgrau (Mild Steel)
  "stainless": "#1e293b"    // Schwarz (Stainless)
}
```

**Verwendung in UI:**
```tsx
<MaterialCard
  material="Aluminium"
  color="#94a3b8"
  selected={selected}
/>
```

---

### Material-Kombinations-Regeln

**Coating Restrictions:**

```python
# Diamond Coating NUR für Non-Ferrous
if coating == CoatingType.DIAMOND:
    allowed_materials = [
        MaterialType.SOFTWOOD,
        MaterialType.HARDWOOD,
        MaterialType.ACRYLIC,
        MaterialType.ALUMINIUM,
        MaterialType.BRASS,
    ]
    if material not in allowed_materials:
        raise ValidationError(
            "Diamond coating can only be used with non-ferrous materials "
            "(Wood, Plastic, Aluminium, Brass)"
        )
```

**Operation Restrictions:**

```python
# Trochoidal Slotting nicht sinnvoll für Holz
if operation == OperationType.SLOT_TROCHOIDAL:
    if material in [MaterialType.SOFTWOOD, MaterialType.HARDWOOD]:
        warnings.append(
            "Trochoidal slotting is typically not used for wood. "
            "Consider SLOT_FULL instead."
        )
```

---

## 2.3 Operationen (13 Operationen inkl. SLOT_TROCHOIDAL)

### Operations-Hierarchie

**4 Kategorien:**

```
1. FACE (Planfräsen) - 2 Operationen
2. SLOT (Nuten) - 4 Operationen (INKL. TROCHOIDAL!)
3. GEOMETRY (Geometrie) - 3 Operationen
4. SPECIAL (Spezial) - 3 Operationen
```

---

### FACE Category (Orange #fb923c)

**1. FACE_ROUGH**
```yaml
Name: "Face Milling (Roughing)"
Description: "Schruppen von großen Flächen"
Category: FACE
Icon: "⬜" (Square)
Color: #fb923c (Orange)

Parameters:
  ae_factor: 0.25  # 25% DC
  ap_factor: 0.25  # 25% DC
  ap_reference: "DC"  # IMMER DC für Face Ops

Typical Use:
  - Große plane Flächen
  - Hohe MRR erwünscht
  - Oberflächenqualität sekundär

Recommendations:
  - Coating: TiN oder TiAlN
  - Surface Quality: ROUGHING oder STANDARD
```

**2. FACE_FINISH**
```yaml
Name: "Face Milling (Finishing)"
Description: "Schlichten von Flächen für gute Oberfläche"
Category: FACE
Icon: "⬜"
Color: #fb923c

Parameters:
  ae_factor: 0.25
  ap_factor: 0.15  # Reduziert für Finishing
  ap_reference: "DC"

Typical Use:
  - Letzte Bearbeitung von Flächen
  - Gute Oberflächenqualität
  - Nach Roughing

Recommendations:
  - Surface Quality: FINISHING oder HIGH_FINISH
  - Höhere vc, niedrigere fz
```

---

### SLOT Category (Blue #3b82f6)

**3. SLOT_ROUGH**
```yaml
Name: "Slot Milling (Roughing)"
Description: "Schruppen von Nuten"
Category: SLOT
Icon: "▭"
Color: #3b82f6 (Blue)

Parameters:
  ae_factor: 1.0   # 100% DC (voller Nutbreite)
  ap_factor: 0.30  # 30% LCF (oder DC, abhängig von L/D)
  ap_reference: "dynamic"  # Abhängig von L/D Ratio

Typical Use:
  - Nuten fräsen
  - Volle Nutbreite
  - Material schnell entfernen
```

**4. SLOT_FINISH**
```yaml
Name: "Slot Milling (Finishing)"
Description: "Schlichten von Nuten"
Category: SLOT
Icon: "▭"
Color: #3b82f6

Parameters:
  ae_factor: 1.0
  ap_factor: 0.15  # Reduziert für Finishing
  ap_reference: "dynamic"

Typical Use:
  - Letzte Bearbeitung von Nuten
  - Gute Oberflächenqualität
  - Maßgenauigkeit
```

**5. SLOT_FULL**
```yaml
Name: "Full Slotting"
Description: "Volle Nutbreite + maximale Tiefe"
Category: SLOT
Icon: "▭"
Color: #3b82f6

Parameters:
  ae_factor: 1.0   # 100% DC
  ap_factor: 0.50  # 50% DC (IMMER DC für Full Slotting!)
  ap_reference: "DC"  # FIXIERT auf DC

Typical Use:
  - Schnelle Nutbearbeitung
  - Volle Belastung
  - Robuste Tools erforderlich

Warnings:
  - Hohe Schnittkräfte
  - L/D Ratio beachten (max 3.0 empfohlen)
```

**6. SLOT_TROCHOIDAL** ⭐ **NEU aus DELTA REQUEST**
```yaml
Name: "Trochoidal Slotting"
Description: "Zirkular-interpolierte Nuten mit geringer Radiallast"
Category: SLOT
Icon: "⟳"
Color: #3b82f6

Parameters:
  ae_factor: 0.10  # NUR 10% DC (kleine Kreis-Inkremente)
  ap_factor: 0.50  # Volle Tiefe möglich
  ap_reference: "LCF"  # Nutzt volle Schneidenlänge

Typical Use:
  - Harte Materialien (Stahl, Stainless)
  - Tiefe Nuten bei kleinen Werkzeugen
  - Reduzierte Werkzeugbelastung
  - Moderne CNC-Maschinen mit High-Speed-Interpolation

Advantages:
  - Geringere Radialkräfte (nur 10% ae)
  - Höhere Vorschübe möglich
  - Bessere Wärmeabfuhr (Chip-Thinning-Effekt)
  - Längere Werkzeug-Lebensdauer

Requirements:
  - CNC mit Trochoidal-Funktion (Fusion 360, HSM, etc.)
  - Stabile Aufspannung
  - Programmierung: Kreisbahn-Strategie

Recommendations:
  - Coating: AlTiN oder TiAlN (für Stahl)
  - Erhöhe vf um 50-100% (gegenüber SLOT_FULL)
  - Stepover: 5-10% DC
```

**Trochoidal vs. Full Slotting Vergleich:**

| Parameter | SLOT_FULL | SLOT_TROCHOIDAL | Unterschied |
|-----------|-----------|-----------------|-------------|
| ae | 100% DC | 10% DC | -90% Radiallast |
| ap | 50% DC | 50% LCF | Gleiche Tiefe |
| Radialkraft | Hoch | Niedrig | Faktor 10x |
| vf | Standard | +50-100% | Schneller |
| Werkzeug-Leben | Standard | +50-200% | Länger |
| CNC-Anforderungen | Basic | Advanced | Interpolation |

---

### GEOMETRY Category (Cyan #06b6d4)

**7. GEO_CHAMFER**
```yaml
Name: "Chamfering"
Description: "Fasen/Anfasen von Kanten"
Category: GEOMETRY
Icon: "◢"
Color: #06b6d4 (Cyan)

Parameters:
  ae_factor: 0.05  # 5% DC (minimal)
  ap_factor: 0.10  # Fla che Zustellung
  ap_reference: "DC"

Typical Use:
  - Kanten brechen
  - 45° Fasen
  - Entgraten

Recommendations:
  - Spezielle Chamfer-Tools (45° oder 60°)
  - Niedrige vf
  - Hohe Oberflächenqualität
```

**8. GEO_RADIUS**
```yaml
Name: "Radius Milling"
Description: "Radiusfräsen (innen/außen)"
Category: GEOMETRY
Icon: "◡"
Color: #06b6d4

Parameters:
  ae_factor: 0.05
  ap_factor: 0.20
  ap_reference: "LCF"

Typical Use:
  - Innen-/Außenradien
  - Kontur-Übergänge
  - Profil-Fräsen

Tool Requirements:
  - Ball-Nose oder Corner-Radius Tools
  - RE (Corner Radius) > 0
```

**9. GEO_BALL**
```yaml
Name: "Ball Nose Milling"
Description: "3D-Kontur-Fräsen mit Kugelfräser"
Category: GEOMETRY
Icon: "◉"
Color: #06b6d4

Parameters:
  ae_factor: 0.10
  ap_factor: 0.15
  ap_reference: "LCF"

Typical Use:
  - 3D-Oberflächen
  - Freiform-Flächen
  - Formen/Gravuren

Tool Requirements:
  - Ball-Nose Tool (RE = DC/2)

Recommendations:
  - Surface Quality: FINISHING oder HIGH_FINISH
  - Kleine Stepover (5-10% DC) für gute Oberfläche
```

---

### SPECIAL Category (Purple #a855f7)

**10. SPECIAL_ADAPTIVE**
```yaml
Name: "Adaptive Clearing"
Description: "Adaptives Schruppen mit variabler Belastung"
Category: SPECIAL
Icon: "⟿"
Color: #a855f7 (Purple)

Parameters:
  ae_factor: 0.40  # 40% DC (variable)
  ap_factor: 0.30  # 30% LCF
  ap_reference: "LCF"  # IMMER LCF (nutzt volle Länge)

Typical Use:
  - HSM (High-Speed-Machining)
  - Taschenbearbeitung
  - Konstante Werkzeugbelastung
  - Moderne CAM-Software (Fusion 360 Adaptive)

Advantages:
  - Höhere MRR als Standard
  - Konstante Schnittkraft
  - Längere Werkzeug-Lebensdauer

Requirements:
  - CAM mit Adaptive-Strategie
  - Stabile Maschine
```

**11. SPECIAL_PLUNGE**
```yaml
Name: "Plunge Milling"
Description: "Axiales Eintauchen (Senken)"
Category: SPECIAL
Icon: "↓"
Color: #a855f7

Parameters:
  ae_factor: 0.0   # Keine radiale Bewegung
  ap_factor: 0.50  # Axial
  ap_reference: "LCF"

Typical Use:
  - Tiefe Taschen
  - Vor-Bohren für Slots
  - Schneller Z-Vorschub

Recommendations:
  - vf_plunge = vf / NOF (Standard)
  - Ramping bevorzugen wenn möglich
```

**12. SPECIAL_DRILL**
```yaml
Name: "Drilling"
Description: "Bohren (für Referenz, nicht primäre Funktion)"
Category: SPECIAL
Icon: "⊕"
Color: #a855f7

Parameters:
  ae_factor: 0.0
  ap_factor: 1.0  # Volle Bohrtiefe
  ap_reference: "LCF"

Note:
  Primär für Vergleich mit echten Bohrern.
  CNC Calculator fokussiert auf Fräsen.
```

**13. SPECIAL_HELICAL** (Optional für V4.1)
```yaml
Name: "Helical Interpolation"
Description: "Spiral-Rampe (kreisförmig + axial)"
Category: SPECIAL
Icon: "⟲"
Color: #a855f7

Status: NOT IMPLEMENTED in V4.0
Reason: Weniger verbreitet, kann später hinzugefügt werden
```

---

### Operations-Matrix: Material × Operation

**Empfohlene Kombinationen:**

|  | SOFT | HARD | ACRY | ALU | BRASS | MILD | STAIN |
|---|------|------|------|-----|-------|------|-------|
| FACE_ROUGH | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| FACE_FINISH | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SLOT_ROUGH | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SLOT_FINISH | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SLOT_FULL | ✅ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ❌ |
| **SLOT_TROCHOIDAL** | ❌ | ❌ | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| GEO_CHAMFER | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GEO_RADIUS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GEO_BALL | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| SPECIAL_ADAPTIVE | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SPECIAL_PLUNGE | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SPECIAL_DRILL | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Legende:**
- ✅ = Empfohlen
- ⚠️ = Mit Einschränkungen / Warnung
- ❌ = Nicht empfohlen

---

## 2.4 Tool Coating System (6 Typen)

### Coating Types

```python
class CoatingType(str, Enum):
    NONE = "None"              # Uncoated / Base Tool
    TIN = "TiN"                # Titanium Nitride (Gold)
    TIALN = "TiAlN"            # Titanium Aluminum Nitride (Violet)
    ALTIN = "AlTiN"            # Aluminum Titanium Nitride (Dark Violet/Black)
    DIAMOND = "Diamond"        # Diamond (PCD / CVD)
    CARBIDE = "Carbide"        # Solid Carbide (Upgraded Material)
```

---

### Coating Properties

| Coating | Color | vc Factor | Max Temp [°C] | Best For | Cost | Restrictions |
|---------|-------|-----------|---------------|----------|------|--------------|
| **None** | Metal (Silver) | 1.0× | Base | General | $ | None |
| **TiN** | Gold | 1.4× (+40%) | 600 | General Purpose, ALU | $$ | None |
| **TiAlN** | Violet | 1.6× (+60%) | 800 | Steel, Stainless, High Temp | $$$ | None |
| **AlTiN** | Dark Violet | 1.8× (+80%) | 900 | Stainless, Hard Steel | $$$$ | None |
| **Diamond** | Clear/White | 2.2× (+120%) | 800 | ALU, Brass, Composites | $$$$$ | **Non-Ferrous ONLY** |
| **Carbide** | Dark Gray | 1.5× (+50%) | 700 | General Upgrade | $$$ | None |

---

### Coating Factor Application

**Code:**
```python
def apply_coating_factor(vc_base: float, coating: CoatingType, material: MaterialType) -> float:
    """
    Applies coating factor to base cutting speed.

    Raises:
        ValidationError: If Diamond coating used with ferrous material
    """

    if coating == CoatingType.NONE:
        return vc_base

    elif coating == CoatingType.TIN:
        return vc_base * 1.4

    elif coating == CoatingType.TIALN:
        return vc_base * 1.6

    elif coating == CoatingType.ALTIN:
        return vc_base * 1.8

    elif coating == CoatingType.DIAMOND:
        # Validation: Diamond only for non-ferrous
        if material in [MaterialType.STEEL_MILD, MaterialType.STEEL_STAINLESS]:
            raise ValidationError(
                "Diamond coating cannot be used with ferrous materials (Steel). "
                "Diamond reacts with iron at high temperatures causing rapid tool wear. "
                "Use TiAlN or AlTiN for steel instead."
            )
        return vc_base * 2.2

    elif coating == CoatingType.CARBIDE:
        return vc_base * 1.5

    else:
        return vc_base
```

---

### Coating Recommendations by Material

**Recommendation Matrix:**

| Material | Best Coating | Alternative | Not Recommended |
|----------|-------------|-------------|-----------------|
| Softwood | None / TiN | - | Diamond (overkill) |
| Hardwood | TiN | TiAlN | Diamond |
| Acrylic | TiN / Diamond | None | - |
| Aluminium | **Diamond** (best) | TiN, Carbide | TiAlN (too hard, chips plastic behavior) |
| Brass | Diamond | TiN | - |
| Steel (Mild) | **TiAlN** | AlTiN, Carbide | **Diamond** ❌ |
| Steel (Stainless) | **AlTiN** (best) | TiAlN | **Diamond** ❌ |

---

### UI Implementation

**Dropdown in Screen 2 (Tool Selection):**

```tsx
<Select coating={selectedCoating} onChange={setSelectedCoating}>
  <Option value="NONE">None (Uncoated)</Option>
  <Option value="TIN">TiN (+40% vc) - Gold</Option>
  <Option value="TIALN">TiAlN (+60% vc) - Violet</Option>
  <Option value="ALTIN">AlTiN (+80% vc) - Dark Violet</Option>
  <Option value="DIAMOND">Diamond (+120% vc) - Non-Ferrous Only!</Option>
  <Option value="CARBIDE">Carbide (+50% vc) - Upgraded Material</Option>
</Select>

{selectedCoating === 'DIAMOND' && (
  <Warning>
    Diamond coating can ONLY be used with non-ferrous materials
    (Wood, Plastic, Aluminium, Brass).
    NOT compatible with Steel!
  </Warning>
)}
```

---

## 2.5 Surface Quality System (4 Levels)

### Surface Quality Enum

```python
class SurfaceQuality(str, Enum):
    ROUGHING = "Roughing"         # Schruppen (schnell, grob)
    STANDARD = "Standard"         # Standard (ausgeglichen)
    FINISHING = "Finishing"       # Schlichten (langsam, fein)
    HIGH_FINISH = "High Finish"   # Hochglanz (sehr langsam, sehr fein)
```

---

### Adjustment Factors

**Factors applied to cutting parameters:**

| Surface Quality | ae Adjustment | ap Adjustment | vf Adjustment | Description |
|----------------|---------------|---------------|---------------|-------------|
| **ROUGHING** | +0% | +0% | **+20%** | Maximum MRR, rougher surface |
| **STANDARD** | +0% | +0% | +0% | Balanced (default) |
| **FINISHING** | **-30%** | **-20%** | **-20%** | Smooth surface, reduced loads |
| **HIGH_FINISH** | **-50%** | **-40%** | **-40%** | Mirror finish, minimal loads |

**Logic:**
- **ROUGHING**: Erhöht vf (+20%) für schnelleres Material-Removal
- **FINISHING**: Reduziert ae/ap/vf für sanftere Schnitte
- **HIGH_FINISH**: Maximal reduziert für Hochglanz-Oberflächen

---

### Implementation

```python
def get_surface_quality_factor(quality: SurfaceQuality, parameter: str) -> float:
    """
    Returns adjustment factor for given parameter based on surface quality.

    Args:
        quality: Surface quality level
        parameter: "ae", "ap", or "vf"

    Returns:
        Multiplier (0.5 = -50%, 1.0 = no change, 1.2 = +20%)
    """

    factors = {
        SurfaceQuality.ROUGHING: {
            "ae": 1.0,
            "ap": 1.0,
            "vf": 1.2,  # +20%
        },
        SurfaceQuality.STANDARD: {
            "ae": 1.0,
            "ap": 1.0,
            "vf": 1.0,
        },
        SurfaceQuality.FINISHING: {
            "ae": 0.7,  # -30%
            "ap": 0.8,  # -20%
            "vf": 0.8,  # -20%
        },
        SurfaceQuality.HIGH_FINISH: {
            "ae": 0.5,  # -50%
            "ap": 0.6,  # -40%
            "vf": 0.6,  # -40%
        },
    }

    return factors[quality][parameter]
```

**Application Example:**
```python
# Base values
ae_base = 7.5 mm
ap_base = 7.5 mm
vf_base = 1080 mm/min

# Apply FINISHING quality
ae_final = ae_base * get_surface_quality_factor(SurfaceQuality.FINISHING, "ae")  # 7.5 * 0.7 = 5.25 mm
ap_final = ap_base * get_surface_quality_factor(SurfaceQuality.FINISHING, "ap")  # 7.5 * 0.8 = 6.0 mm
vf_final = vf_base * get_surface_quality_factor(SurfaceQuality.FINISHING, "vf")  # 1080 * 0.8 = 864 mm/min
```

---

### Recommendations by Operation

| Operation | Recommended Quality | Alternative | Not Recommended |
|-----------|-------------------|-------------|-----------------|
| FACE_ROUGH | **ROUGHING** or STANDARD | - | HIGH_FINISH (waste of time) |
| FACE_FINISH | FINISHING or **HIGH_FINISH** | STANDARD | ROUGHING |
| SLOT_ROUGH | ROUGHING or **STANDARD** | - | HIGH_FINISH |
| SLOT_FINISH | **FINISHING** | HIGH_FINISH | ROUGHING |
| SLOT_TROCHOIDAL | STANDARD or **ROUGHING** | - | HIGH_FINISH |
| GEO_* (Geometry) | **FINISHING** or HIGH_FINISH | STANDARD | ROUGHING |
| SPECIAL_ADAPTIVE | STANDARD or **ROUGHING** | - | FINISHING |

---

## 2.6 Dry Machining Corrections

**Feature:** Reduzierung von fz bei Trockenzerspanung (ohne Kühlmittel)

### Dry Machining Factors

```python
DRY_MACHINING_FACTORS = {
    MaterialType.SOFTWOOD: 1.0,        # Kein Kühlmittel nötig
    MaterialType.HARDWOOD: 1.0,        # Kein Kühlmittel nötig
    MaterialType.ACRYLIC: 0.9,         # -10% (Hitzeprobleme)
    MaterialType.ALUMINIUM: 0.85,      # -15% (Verschweißung)
    MaterialType.BRASS: 0.9,           # -10%
    MaterialType.STEEL_MILD: 0.7,      # -30% (hohe Hitze)
    MaterialType.STEEL_STAINLESS: 0.65, # -35% (sehr hohe Hitze)
}
```

### Logic

```python
def apply_dry_correction(fz_base: float, material: MaterialType, dry: bool) -> float:
    """
    Reduces fz when machining without coolant.
    """
    if not dry:
        return fz_base  # Mit Kühlmittel: keine Korrektur

    factor = DRY_MACHINING_FACTORS[material]
    return fz_base * factor
```

**Rationale:**
- Ohne Kühlmittel → höhere Temperaturen
- Höhere Temps → Werkzeugverschleiß steigt
- Reduzierte fz → geringere Hitze-Erzeugung
- Besonders kritisch für Metalle (Stahl!)

---

## 2.7 L/D Stability Reductions

**Feature:** Automatische Parameter-Reduktion bei langen Werkzeugen (L/D > 3.0)

### L/D Ratio Ranges

| L/D Ratio | Status | vc/fz Reduction | ae/ap Reduction | Warning Level |
|-----------|--------|-----------------|-----------------|---------------|
| ≤ 3.0 | **STABLE** | 0% | 0% | None |
| 3.0 - 5.0 | **MODERATE** | -20% | -10% | ⚠️ Warning |
| 5.0 - 8.0 | **UNSTABLE** | -40% | -20% | ⚠️⚠️ High Risk |
| > 8.0 | **CRITICAL** | -60% | -30% | 🚨 Critical |

### Implementation (bereits in Phase 10 dokumentiert)

Siehe Phase 10: L/D Stability Check für vollständige Implementierung.

---

## 2.8 Chip Temperature Analysis

**Feature:** Schätzung der Span-Temperatur zur Vermeidung von Überhitzung

### Formula (Empirical)

```python
T_chip = k_thermal * (vc^0.6) * (fz^0.3) * (ap^0.2)  # [°C]
```

**Thermal Constants:**
- Siehe Phase 8 für vollständige Tabelle

### Warning Thresholds

```python
if T_chip > max_safe_temp:
    status = Status.WARNING
    warnings.append(
        f"Chip temperature {T_chip:.0f}°C exceeds safe limit {max_safe_temp}°C. "
        "Consider: (1) Reduce vc, (2) Enable coolant, (3) Use coating"
    )

if T_chip > max_safe_temp * 1.2:
    status = Status.ERROR  # CRITICAL!
```

---

## 2.9 Chip Formation Prediction

**Feature:** Vorhersage der Spanform zur Optimierung der Zerspanungsbedingungen

### Chip Types

```python
class ChipType(str, Enum):
    CONTINUOUS_THIN = "Continuous (Thin)"        # Problematisch
    CONTINUOUS_OPTIMAL = "Continuous (Optimal)"  # Gut für Alu
    CONTINUOUS_THICK = "Continuous (Thick)"      # Schwer zu brechen
    SEGMENTED_OPTIMAL = "Segmented (Optimal)"    # Gut für Stahl
    SHEAR = "Shear (Thin)"                       # Zu dünn
    DISCONTINUOUS = "Discontinuous"              # Brüchig (Holz)
```

**Logic:** Siehe Phase 9 für vollständige Implementierung

---

## 2.10 Validierung (8 Checks)

### 8-Checks-System

**Alle Presets müssen 8 Validierungs-Checks bestehen:**

#### Check 1: Geometry Validation

```python
def check_geometry(tool: Tool) -> list[str]:
    """
    Validates tool geometry consistency.
    """
    errors = []

    if tool.DC <= 0:
        errors.append("DC must be > 0")

    if tool.DC > tool.DCX:
        errors.append(f"DC ({tool.DC}) must be ≤ DCX ({tool.DCX})")

    if tool.LCF <= 0:
        errors.append("LCF must be > 0")

    if tool.NOF < 1 or tool.NOF > 12:
        errors.append("NOF must be between 1 and 12")

    if tool.LCF > tool.OAL:
        errors.append(f"LCF ({tool.LCF}) must be ≤ OAL ({tool.OAL})")

    return errors
```

---

#### Check 2: Material/Coating Compatibility

```python
def check_coating_compatibility(material: MaterialType, coating: CoatingType) -> list[str]:
    """
    Checks if coating is compatible with material.
    """
    errors = []

    if coating == CoatingType.DIAMOND:
        if material in [MaterialType.STEEL_MILD, MaterialType.STEEL_STAINLESS]:
            errors.append(
                "Diamond coating cannot be used with steel (ferrous materials). "
                "Diamond reacts with iron at high temperatures."
            )

    return errors
```

---

#### Check 3: Cutting Speed Range

```python
def check_vc_range(vc: float, material: MaterialType) -> list[str]:
    """
    Validates cutting speed is within reasonable range.
    """
    warnings = []

    # Material-specific limits (example)
    vc_max = {
        MaterialType.SOFTWOOD: 2000,
        MaterialType.HARDWOOD: 1500,
        MaterialType.ACRYLIC: 1000,
        MaterialType.ALUMINIUM: 1200,
        MaterialType.BRASS: 600,
        MaterialType.STEEL_MILD: 400,
        MaterialType.STEEL_STAINLESS: 300,
    }

    if vc > vc_max[material]:
        warnings.append(
            f"vc ({vc:.0f} m/min) exceeds typical maximum for {material.value} "
            f"({vc_max[material]} m/min). Verify coating and machine capability."
        )

    if vc < 10:
        warnings.append("vc is very low (< 10 m/min). Check calculation.")

    return warnings
```

---

#### Check 4: Spindle Speed Limit

```python
def check_rpm_limit(n: float, max_rpm: float = 30000) -> list[str]:
    """
    Validates spindle speed doesn't exceed machine limit.
    """
    errors = []
    warnings = []

    if n > max_rpm:
        errors.append(
            f"Spindle speed {n:.0f} RPM exceeds machine limit {max_rpm} RPM. "
            "Reduce vc or use larger tool."
        )

    if n > max_rpm * 0.9:
        warnings.append(
            f"Spindle speed {n:.0f} RPM is near machine limit ({max_rpm} RPM)."
        )

    return errors + warnings
```

---

#### Check 5: Feed Rate Sanity

```python
def check_vf_range(vf: float) -> list[str]:
    """
    Validates feed rate is reasonable.
    """
    warnings = []

    if vf > 10000:
        warnings.append(
            f"Feed rate {vf:.0f} mm/min is very high (> 10000). "
            "Verify machine rapids capability."
        )

    if vf < 50:
        warnings.append(
            f"Feed rate {vf:.0f} mm/min is very low (< 50). "
            "May cause chatter or poor surface finish."
        )

    return warnings
```

---

#### Check 6: Power & Torque Limits

```python
def check_power(Pc: float, M: float, max_power: float = 5.0, max_torque: float = 50.0) -> list[str]:
    """
    Validates cutting power and torque are within machine limits.
    """
    errors = []
    warnings = []

    if Pc > max_power:
        errors.append(
            f"Cutting power {Pc:.2f} kW exceeds spindle limit {max_power} kW. "
            "Reduce ae, ap, or vf."
        )

    if M > max_torque:
        errors.append(
            f"Torque {M:.2f} Nm exceeds spindle limit {max_torque} Nm."
        )

    if Pc > max_power * 0.8:
        warnings.append(f"Power {Pc:.2f} kW is near spindle limit.")

    return errors + warnings
```

---

#### Check 7: Thermal Limits

```python
def check_temperature(T_chip: float, max_safe_temp: float) -> list[str]:
    """
    Validates chip temperature is within safe range.
    """
    errors = []
    warnings = []

    if T_chip > max_safe_temp * 1.2:
        errors.append(
            f"Chip temperature {T_chip:.0f}°C is critically high "
            f"(> {max_safe_temp * 1.2:.0f}°C). Tool failure risk!"
        )

    if T_chip > max_safe_temp:
        warnings.append(
            f"Chip temperature {T_chip:.0f}°C exceeds safe limit "
            f"({max_safe_temp}°C). Consider coolant or reduced parameters."
        )

    return errors + warnings
```

---

#### Check 8: L/D Stability

```python
def check_ld_stability(L_D_ratio: float) -> list[str]:
    """
    Validates L/D ratio and provides warnings for unstable tools.
    """
    warnings = []

    if L_D_ratio > 8.0:
        warnings.append(
            f"L/D ratio {L_D_ratio:.2f} > 8.0 is CRITICAL. "
            "Very high vibration risk. Consider shorter tool or special holder."
        )
    elif L_D_ratio > 5.0:
        warnings.append(
            f"L/D ratio {L_D_ratio:.2f} > 5.0 is UNSTABLE. "
            "High vibration risk. Reduced parameters applied."
        )
    elif L_D_ratio > 3.0:
        warnings.append(
            f"L/D ratio {L_D_ratio:.2f} > 3.0 is MODERATE. "
            "Some vibration risk. Slightly reduced parameters applied."
        )

    return warnings
```

---

### Validation Workflow

```python
def validate_preset(preset: CalculatedPreset) -> ValidationResult:
    """
    Runs all 8 validation checks on a calculated preset.

    Returns:
        ValidationResult with status (OK, WARNING, ERROR) and messages
    """

    errors = []
    warnings = []

    # Check 1: Geometry
    errors.extend(check_geometry(preset.tool))

    # Check 2: Coating Compatibility
    errors.extend(check_coating_compatibility(preset.material, preset.coating))

    # Check 3: Cutting Speed
    warnings.extend(check_vc_range(preset.vc, preset.material))

    # Check 4: RPM
    errors.extend(check_rpm_limit(preset.n))

    # Check 5: Feed Rate
    warnings.extend(check_vf_range(preset.vf))

    # Check 6: Power & Torque
    errors.extend(check_power(preset.Pc, preset.M))

    # Check 7: Temperature
    errors.extend(check_temperature(preset.T_chip, preset.max_safe_temp))

    # Check 8: L/D Stability
    warnings.extend(check_ld_stability(preset.L_D_ratio))

    # Determine final status
    if errors:
        status = Status.ERROR
    elif warnings:
        status = Status.WARNING
    else:
        status = Status.OK

    return ValidationResult(
        status=status,
        errors=errors,
        warnings=warnings,
        preset=preset
    )
```

---

# TEIL 3-8: BACKEND, FRONTEND, EXPORT, EPICS & IMPLEMENTIERUNG (ZUSAMMENFASSUNG)

> **Hinweis:** Die restlichen Teile sind hier kompakt zusammengefasst. Vollständige Details befinden sich in den Quell-Dokumenten (DELTA_REQUEST, Prototyp-Spezifikation, etc.)

## TEIL 3: BACKEND-ARCHITEKTUR (DETAILED)

### 3.1 System-Architektur

**Pattern:** API-First + Clean Architecture
- **Frontend** (React) → REST API → **Backend** (FastAPI) → **V2.0 Engine** (NO-TOUCH)
- **Async Processing:** Celery + Redis für große Berechnungen
- **Database:** SQLite (Dev) / PostgreSQL (Prod)

**Architecture Layers:**

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐      │
│  │ Screens │  │  State  │  │  API    │  │  Design  │      │
│  │         │  │ (Zustand│  │ Client  │  │  System  │      │
│  └─────────┘  └─────────┘  └─────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────┘
                        ▲
                        │ HTTP/REST (JSON)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│               BACKEND API (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               REST API Layer                          │  │
│  │  • Request Validation (Pydantic)                     │  │
│  │  • Response Serialization                            │  │
│  │  • Error Handling Middleware                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                        ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Service Layer                              │  │
│  │  • ToolParserService                                  │  │
│  │  • CalculationService                                 │  │
│  │  • ExpertModeService                                  │  │
│  │  • ValidationService                                  │  │
│  │  • ExportService                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                        ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Domain/Business Logic                        │  │
│  │  • V2.0 Calculation Engine (NO-TOUCH!)                │  │
│  │  • 10-Phase Workflow                                  │  │
│  │  • Material Database                                  │  │
│  │  • Operation Logic                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                        ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Data Layer                                   │  │
│  │  • Database (SQLite/PostgreSQL)                       │  │
│  │  • Redis Cache                                        │  │
│  │  • File Storage                                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

### 3.2 FastAPI Application Structure

**File Structure:**

```
backend/
├── main.py                      # FastAPI app initialization
├── requirements.txt             # Dependencies
├── config.py                    # Configuration
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── router.py           # Main router
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── tools.py        # Tool parsing endpoints
│   │   │   ├── calculate.py    # Calculation endpoints
│   │   │   ├── expert.py       # Expert mode endpoints
│   │   │   └── export.py       # Export endpoints
│   │   └── dependencies.py     # Shared dependencies
├── services/
│   ├── __init__.py
│   ├── tool_parser.py          # Parse .tools files
│   ├── calculation.py          # Calculation service
│   ├── expert_mode.py          # Expert mode logic
│   ├── validation.py           # Validation service
│   └── export.py               # Export service
├── core/
│   ├── __init__.py
│   ├── v2_engine.py            # V2.0 Engine Wrapper (NO-TOUCH)
│   ├── materials.py            # Material database
│   └── operations.py           # Operation logic
├── models/
│   ├── __init__.py
│   ├── schemas.py              # Pydantic models
│   └── domain.py               # Domain models
├── workers/
│   ├── __init__.py
│   ├── celery_app.py           # Celery configuration
│   └── tasks.py                # Async tasks
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_services.py
    └── test_calculations.py
```

---

### 3.3 Main Application (main.py)

```python
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import time

from api.v1.router import api_router
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting CNC Calculator API v4.0")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    # Initialize services
    # ... initialization code ...

    yield

    # Shutdown
    logger.info("Shutting down CNC Calculator API")
    # ... cleanup code ...


# Create FastAPI app
app = FastAPI(
    title="CNC Calculator API",
    description="REST API for CNC cutting parameter calculation",
    version="4.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error occurred",
            "type": type(exc).__name__
        }
    )


# Include API router
app.include_router(api_router, prefix="/api/v1")


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "4.0.0",
        "environment": settings.ENVIRONMENT
    }


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "CNC Calculator API v4.0",
        "docs": "/api/docs" if settings.DEBUG else "disabled in production"
    }
```

---

### 3.4 Configuration (config.py)

```python
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "CNC Calculator"
    VERSION: str = "4.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here-change-in-production"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Database
    DATABASE_URL: str = "sqlite:///./cnc_calculator.db"
    DATABASE_ECHO: bool = False

    # Redis (for Celery)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    UPLOAD_FOLDER: str = "./uploads"
    ALLOWED_EXTENSIONS: set = {".tools", ".json"}

    # Calculation
    MAX_CONCURRENT_CALCULATIONS: int = 5
    CALCULATION_TIMEOUT: int = 300  # 5 minutes

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "cnc_calculator.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

---

### 3.5 REST API Endpoints (COMPLETE)

**3.5.1 Tool Parser Endpoints (api/v1/endpoints/tools.py)**

```python
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List

from services.tool_parser import ToolParserService
from models.schemas import (
    ToolParseResponse,
    Tool,
    PresetAnalysis
)
from config import settings

router = APIRouter(prefix="/tools", tags=["tools"])
parser_service = ToolParserService()


@router.post("/parse", response_model=ToolParseResponse)
async def parse_tools_file(
    file: UploadFile = File(...)
):
    """
    Parse Fusion 360 .tools file and extract tool geometries.

    - Validates ZIP structure
    - Parses tools.json
    - Calculates L/D ratios
    - Detects existing presets (Smart Detection)
    - Returns tool list with preset analysis
    """
    # Validate file extension
    if not file.filename.endswith('.tools'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Expected .tools file."
        )

    # Validate file size
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024} MB"
        )

    # Parse file
    try:
        result = await parser_service.parse_tools_file(contents, file.filename)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid .tools file: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse file: {str(e)}"
        )


@router.get("/validate/{tool_id}")
async def validate_tool_geometry(tool_id: str):
    """
    Validate tool geometry for calculation suitability.

    Checks:
    - DC > 0
    - LCF > 0
    - NOF >= 1
    - L/D ratio warnings
    """
    # Implementation
    pass
```

**3.5.2 Calculation Endpoints (api/v1/endpoints/calculate.py)**

```python
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import List, Optional
from uuid import uuid4

from services.calculation import CalculationService
from services.validation import ValidationService
from workers.tasks import calculate_presets_async
from models.schemas import (
    CalculationRequest,
    CalculationResponse,
    PresetResult,
    AsyncTaskResponse,
    TaskStatus
)

router = APIRouter(prefix="/calculate", tags=["calculate"])
calculation_service = CalculationService()
validation_service = ValidationService()


@router.post("/", response_model=CalculationResponse)
async def calculate_presets(
    request: CalculationRequest
):
    """
    Synchronous calculation of cutting parameters.

    Use for small batches (< 20 presets).
    For larger batches, use /calculate/async instead.

    Process:
    1. Validate request
    2. Run 10-phase calculation for each preset
    3. Apply coating factors
    4. Apply surface quality adjustments
    5. Apply expert mode overrides (if any)
    6. Validate results (8-check system)
    7. Return all results
    """
    # Validate request
    validation_result = validation_service.validate_calculation_request(request)
    if not validation_result.valid:
        raise HTTPException(
            status_code=422,
            detail=validation_result.errors
        )

    # Check preset count
    total_presets = len(request.tool_ids) * len(request.materials) * len(request.operations)
    if total_presets > 20:
        raise HTTPException(
            status_code=400,
            detail=f"Too many presets ({total_presets}). Use /calculate/async for batches > 20."
        )

    # Calculate
    try:
        results = await calculation_service.calculate_batch(request)
        return CalculationResponse(
            success=True,
            total_presets=len(results),
            results=results,
            warnings=validation_result.warnings
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Calculation failed: {str(e)}"
        )


@router.post("/async", response_model=AsyncTaskResponse)
async def calculate_presets_async_endpoint(
    request: CalculationRequest,
    background_tasks: BackgroundTasks
):
    """
    Asynchronous calculation using Celery.

    Use for large batches (> 20 presets).

    Returns task_id immediately.
    Client polls /calculate/status/{task_id} for progress.
    """
    # Validate request
    validation_result = validation_service.validate_calculation_request(request)
    if not validation_result.valid:
        raise HTTPException(
            status_code=422,
            detail=validation_result.errors
        )

    # Create task
    task = calculate_presets_async.delay(request.dict())

    return AsyncTaskResponse(
        task_id=task.id,
        status="PENDING",
        message="Calculation task created. Poll /calculate/status/{task_id} for progress."
    )


@router.get("/status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """
    Get status of async calculation task.

    Poll this endpoint every 1-2 seconds to monitor progress.

    States:
    - PENDING: Task queued
    - STARTED: Calculation in progress
    - SUCCESS: Completed successfully
    - FAILURE: Error occurred
    """
    from celery.result import AsyncResult

    task = AsyncResult(task_id)

    if task.state == 'PENDING':
        return TaskStatus(
            task_id=task_id,
            state=task.state,
            status='Task is waiting to start',
            progress=0
        )
    elif task.state == 'STARTED':
        # Get progress from task meta
        meta = task.info or {}
        return TaskStatus(
            task_id=task_id,
            state=task.state,
            status='Calculating presets...',
            progress=meta.get('progress', 0),
            current_preset=meta.get('current_preset'),
            total_presets=meta.get('total_presets')
        )
    elif task.state == 'SUCCESS':
        return TaskStatus(
            task_id=task_id,
            state=task.state,
            status='Calculation completed',
            progress=100,
            result=task.result
        )
    elif task.state == 'FAILURE':
        return TaskStatus(
            task_id=task_id,
            state=task.state,
            status='Calculation failed',
            error=str(task.info)
        )
    else:
        return TaskStatus(
            task_id=task_id,
            state=task.state,
            status=f'Unknown state: {task.state}'
        )
```

**3.5.3 Expert Mode Endpoints (api/v1/endpoints/expert.py)**

```python
from fastapi import APIRouter, HTTPException
from typing import List

from services.expert_mode import ExpertModeService
from models.schemas import (
    ExpertModeRequest,
    ExpertModeResponse,
    ExpertModeValidation
)

router = APIRouter(prefix="/expert", tags=["expert"])
expert_service = ExpertModeService()


@router.post("/calculate", response_model=ExpertModeResponse)
async def calculate_with_expert_mode(
    request: ExpertModeRequest
):
    """
    Calculate with expert mode overrides.

    Supports:
    - Global adjustment slider (-50% to +50%)
    - ap reference override (DC/LCF)
    - Individual parameter overrides (ae, ap, fz, vc)

    Calculation order:
    1. Base calculation
    2. Apply global adjustment
    3. Apply individual overrides
    4. Validate (with warnings for aggressive settings)
    """
    # Validate overrides
    validation = expert_service.validate_overrides(request.overrides)
    if validation.has_errors:
        raise HTTPException(
            status_code=422,
            detail=validation.errors
        )

    # Calculate with overrides
    try:
        result = await expert_service.calculate_with_overrides(request)
        return ExpertModeResponse(
            success=True,
            result=result,
            validation=validation
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Expert mode calculation failed: {str(e)}"
        )


@router.post("/validate", response_model=ExpertModeValidation)
async def validate_expert_overrides(
    request: ExpertModeRequest
):
    """
    Validate expert mode overrides without calculating.

    Returns warnings for:
    - ap reference conflicts
    - Aggressive parameters (> 150% of base)
    - Unsafe combinations
    """
    validation = expert_service.validate_overrides(request.overrides)
    return validation
```

**3.5.4 Export Endpoints (api/v1/endpoints/export.py)**

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import io

from services.export import ExportService
from models.schemas import (
    ExportRequest,
    ExportFormat
)

router = APIRouter(prefix="/export", tags=["export"])
export_service = ExportService()


@router.post("/fusion")
async def export_to_fusion(
    request: ExportRequest
):
    """
    Export calculation results to Fusion 360 .tools file.

    Creates ZIP with:
    - tools.json (with 13 expressions per preset)
    - Proper preset naming
    - Full parameter set

    Returns binary ZIP file for download.
    """
    try:
        # Generate .tools file
        tools_file = await export_service.create_fusion_export(request.results)

        # Return as download
        return StreamingResponse(
            io.BytesIO(tools_file),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=cnc_presets_{request.batch_id}.tools"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(e)}"
        )


@router.post("/csv")
async def export_to_csv(request: ExportRequest):
    """Export results to CSV format."""
    pass


@router.post("/excel")
async def export_to_excel(request: ExportRequest):
    """Export results to Excel (XLSX) format."""
    pass


@router.post("/json")
async def export_to_json(request: ExportRequest):
    """Export results to JSON format."""
    pass
```

---

### 3.6 Celery Worker Configuration

**workers/celery_app.py:**

```python
from celery import Celery
from config import settings

# Create Celery app
celery_app = Celery(
    "cnc_calculator",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)
```

**workers/tasks.py:**

```python
from celery import Task
from celery.utils.log import get_task_logger

from workers.celery_app import celery_app
from services.calculation import CalculationService
from models.schemas import CalculationRequest

logger = get_task_logger(__name__)
calculation_service = CalculationService()


class ProgressTask(Task):
    """Base task with progress reporting."""

    def update_progress(self, current: int, total: int, current_preset: str = None):
        """Update task progress."""
        self.update_state(
            state='STARTED',
            meta={
                'progress': int((current / total) * 100),
                'current': current,
                'total': total,
                'current_preset': current_preset
            }
        )


@celery_app.task(base=ProgressTask, bind=True)
def calculate_presets_async(self, request_data: dict):
    """
    Async calculation task.

    Reports progress as it processes each preset.
    """
    logger.info(f"Starting async calculation task {self.request.id}")

    # Parse request
    request = CalculationRequest(**request_data)

    # Calculate total presets
    total_presets = len(request.tool_ids) * len(request.materials) * len(request.operations)
    logger.info(f"Total presets to calculate: {total_presets}")

    results = []
    current = 0

    try:
        # Process each preset
        for tool_id in request.tool_ids:
            for material in request.materials:
                for operation in request.operations:
                    # Update progress
                    current += 1
                    preset_name = f"{material}_{operation}"
                    self.update_progress(current, total_presets, preset_name)

                    # Calculate
                    result = calculation_service.calculate_single_preset(
                        tool_id=tool_id,
                        material=material,
                        operation=operation,
                        coating=request.coating,
                        surface_quality=request.surface_quality,
                        coolant=request.coolant
                    )

                    results.append(result)

                    logger.info(f"Calculated preset {current}/{total_presets}: {preset_name}")

        logger.info(f"Calculation completed successfully. {len(results)} presets calculated.")
        return {
            'success': True,
            'total_presets': len(results),
            'results': [r.dict() for r in results]
        }

    except Exception as e:
        logger.error(f"Calculation failed: {str(e)}", exc_info=True)
        raise
```

---



## TEIL 4: FRONTEND-ARCHITEKTUR (Zusammenfassung)

### 4.1 Design System

**Basis:** Prototyp v0.3_production (Dark Theme ONLY)
- **Fonts:** Inter (Primary), Work Sans (Headline), Fira Code (Mono)
- **Spacing:** Compact Scale (2/4/8/12/16/20/24/32px)
- **Kontrast-Modi:** medium / balanced (default) / high

### 4.2 Core Components (Prototyp-basiert)

1. **Slider** - Marker-basiert, OHNE sichtbaren Thumb, Gradient (Blue→Green→Red)
2. **CompactSlider** - Bidirektional (-100% bis +100%), für Expert Mode
3. **Table** - Sortierbar, Clickable Rows, Status-Badges
4. **OperationCard** - Farbcodiert (Orange/Blue/Cyan/Purple)
5. **MaterialCard** - Material-spezifische Farben

### 4.3 6-Screen-Workflow

```
Screen 1: Import Tools (.tools File Upload)
   ↓
Screen 2: Tool Selection + Coating Dropdown
   ↓
Screen 3: Material Selection (PER TOOL!) + Härte-sortiert
   ↓
Screen 4: Operation Matrix (13 Ops, 4 Kategorien, kompakt)
   ↓
Screen 5: Calculation Progress (mit Celery Status)
   ↓
Screen 6: Results + Filtering (OK/Warning/Error) + Dynamic Headers
   ↓
Screen 7: Export Dialog (Fusion CSV priority)
   ↓
Screen 8: Expert Mode (Global Slider + Individual Parameters)
```

---

## 4.4 DETAILED SCREEN SPECIFICATIONS

### 4.4.1 Screen 1: Tool Import with Smart Preset Detection

**Purpose:** Import Fusion 360 .tools file and automatically detect existing presets

**Layout:**

```
┌──────────────────────────────────────────────────────────────┐
│ [← Back] Step 1 of 6: Import Tools                           │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  📁 Import Fusion 360 Tool Library                           │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │           Drag & Drop .tools file here                 │ │
│  │                    or                                   │ │
│  │              [Browse Files...]                          │ │
│  │                                                         │ │
│  │  Supported: .tools (Fusion 360 Tool Library ZIP)      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  ℹ️  What happens during import:                            │
│  1. Extract tools.json from ZIP archive                     │
│  2. Parse tool geometries (DC, LCF, NOF, etc.)              │
│  3. Calculate L/D ratios for stability analysis             │
│  4. Detect existing presets (Smart Detection)               │
│  5. Extract material + operation from preset names          │
│  6. Pre-select materials and operations for next screens    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**After Upload - Analysis Results:**

```
┌──────────────────────────────────────────────────────────────┐
│ ⏳ Importing and analyzing...                                │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ ✓ Parsed 13 tools from Fusion 360 Library                   │
│ ✓ Validated all geometries                                  │
│ ✓ Calculated L/D ratios                                     │
│ ✓ Detecting existing presets...                             │
│                                                               │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ 🔍 SMART PRESET DETECTION RESULTS                           │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                               │
│ 📌 T1 - Planfräser Ø30mm (3 flutes)                        │
│    ✓ Found 6 existing presets:                              │
│                                                               │
│    Materials detected (sorted by hardness):                  │
│    • Softwood    ← WoodS_Face_Finish, WoodS_Face_Rough      │
│    • Hardwood    ← WoodH_Face_Finish, WoodH_Face_Rough      │
│    • Aluminium   ← Alu_Face_Finish, Alu_Face_Rough          │
│                                                               │
│    Operations detected:                                      │
│    • FACE_ROUGH  (Schruppen)                                │
│    • FACE_FINISH (Schlichten)                               │
│                                                               │
│    → ✅ Pre-selected: 3 materials × 2 operations = 6 presets│
│    → 💾 Reference values stored for Mathematical Workbook   │
│                                                               │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                               │
│ 📌 T3 - End Mill Ø6mm (2 flutes)                           │
│    ⚠️  No presets found                                     │
│                                                               │
│    → 🎯 Default pre-selection: Aluminium only               │
│    → 🎯 Default operations: FACE_FINISH, SLOT_FINISH        │
│                                                               │
│ SUMMARY:                                                      │
│ ✓ 13 tools imported successfully                            │
│ ✓ 6 presets detected (covering 1 tool)                      │
│ ✓ 12 tools use default configuration                        │
│ • 0 import errors                                            │
│                                                               │
│ [Continue to Tool Selection →]                              │
└──────────────────────────────────────────────────────────────┘
```

**Smart Preset Detection Logic:**

```python
# Preset Name Parser
FUSION_MATERIAL_MAP = {
    'WoodS': 'Softwood',
    'WoodH': 'Hardwood',
    'Wood': 'Hardwood',
    'Alu': 'Aluminium',
    'Brass': 'Brass',
    'Acry': 'Acrylic',
    'Cu': 'Copper',
    'Steel': 'Steel_Mild',
    'V2A': 'Steel_Stainless',
    'Ti': 'Titanium'
}

FUSION_OPERATION_MAP = {
    'Face_Rough': 'FACE_ROUGH',
    'Face_Finish': 'FACE_FINISH',
    'Slot_Rough': 'SLOT_ROUGH',
    'Slot_Finish': 'SLOT_FINISH',
    'Slot_Full': 'SLOT_FULL',
    'Slot_Trochoidal': 'SLOT_TROCHOIDAL',
    'Chamfer': 'GEOMETRY_CHAMFER',
    'Radius': 'GEOMETRY_RADIUS',
    'Ball': 'GEOMETRY_BALL',
    'Adaptive': 'SPECIAL_ADAPTIVE',
    'Plunge': 'SPECIAL_PLUNGE',
    'Drill': 'SPECIAL_DRILL'
}

def parse_preset_name(name: str) -> Optional[dict]:
    """
    Parses Fusion 360 preset names.

    Examples:
        "WoodS_Face_Rough" → {'material': 'Softwood', 'operation': 'FACE_ROUGH'}
        "Alu_Face_Finish" → {'material': 'Aluminium', 'operation': 'FACE_FINISH'}
        "V2A_Slot_Trochoidal" → {'material': 'Steel_Stainless', 'operation': 'SLOT_TROCHOIDAL'}
    """
    if not name or '_' not in name:
        return None

    parts = name.split('_')
    material_abbr = parts[0]
    operation_name = '_'.join(parts[1:])

    material = FUSION_MATERIAL_MAP.get(material_abbr)
    operation = FUSION_OPERATION_MAP.get(operation_name)

    if not material or not operation:
        return None

    return {
        'material': material,
        'operation': operation
    }


def detect_presets(tool: Tool) -> PresetAnalysis:
    """
    Analyzes tool for existing presets and creates pre-selection.

    Returns:
        PresetAnalysis with detected materials, operations, and reference values
    """
    detected_presets = []
    materials = set()
    operations = set()
    reference_values = {}

    # Parse each preset in tool
    for preset in tool.presets:
        parsed = parse_preset_name(preset.name)
        if parsed:
            detected_presets.append({
                'name': preset.name,
                'material': parsed['material'],
                'operation': parsed['operation']
            })
            materials.add(parsed['material'])
            operations.add(parsed['operation'])

            # Store reference cutting data for Mathematical Workbook
            reference_values[preset.name] = {
                'vc': preset.cutting_data.get('vc'),
                'n': preset.cutting_data.get('n'),
                'fz': preset.cutting_data.get('fz'),
                'vf': preset.cutting_data.get('vf'),
                'ae': preset.cutting_data.get('ae'),
                'ap': preset.cutting_data.get('ap')
            }

    # Sort materials by hardness
    materials_sorted = sorted(
        materials,
        key=lambda m: MATERIAL_HARDNESS_ORDER.get(m, 999)
    )

    # Sort operations by category and type
    operations_sorted = sorted(
        operations,
        key=lambda o: OPERATION_SORT_ORDER.get(o, 999)
    )

    return PresetAnalysis(
        has_presets=len(detected_presets) > 0,
        detected_presets=detected_presets,
        pre_selected_materials=materials_sorted,
        pre_selected_operations=operations_sorted,
        reference_values=reference_values
    )
```

**User Interactions:**

1. **Drag & Drop:**
   - Hover effect on drop zone
   - Visual feedback during upload
   - Progress indicator for large files

2. **Analysis Phase:**
   - Animated spinner during parsing
   - Real-time status updates
   - Estimated time remaining

3. **Results Display:**
   - Expandable tool sections
   - Hover tooltips for detected presets
   - Visual indicators (✓ detected, ⚠️ defaults)

4. **Continue:**
   - Button enabled only after successful import
   - Preserves all detection data in state
   - Navigates to Tool Selection screen

**State Changes:**

```typescript
interface ImportState {
  status: 'idle' | 'uploading' | 'parsing' | 'complete' | 'error';
  tools: Tool[];
  detectedPresets: PresetAnalysis[];
  error: string | null;
}

// After successful import
const importState = {
  status: 'complete',
  tools: [...], // 13 tools parsed
  detectedPresets: [
    {
      toolId: 'T1',
      hasPresets: true,
      detectedPresets: [/* ... */],
      preSelectedMaterials: ['Softwood', 'Hardwood', 'Aluminium'],
      preSelectedOperations: ['FACE_ROUGH', 'FACE_FINISH'],
      referenceValues: {/* ... */}
    },
    // ... rest of tools
  ],
  error: null
};
```

**Validation Rules:**

- ✅ File must be valid ZIP archive
- ✅ Must contain `tools.json` at root
- ✅ JSON must have valid schema
- ✅ At least 1 tool required
- ✅ All geometries must be valid (DC > 0, etc.)
- ⚠️ Missing presets → use defaults (not an error)

**Error Handling:**

```
┌──────────────────────────────────────────────────────────────┐
│ ❌ Import Failed                                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ Error: Invalid tools.json format                             │
│                                                               │
│ Details:                                                      │
│ • Expected "tools" array at root                             │
│ • Found invalid JSON syntax at line 42                       │
│                                                               │
│ [Try Another File] [View Documentation]                     │
└──────────────────────────────────────────────────────────────┘
```

---

### 4.4.2 Screen 2: Tool Selection with Multi-Select

**Purpose:** Select which tools to calculate presets for

**Layout:**

```
┌──────────────────────────────────────────────────────────────┐
│ [← Back] Step 2 of 6: Select Tools                           │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  [🔍 Search tools...] [Filter: All Types ▼] [Sort: Number ▼]│
│  [☐ Select All]  0 of 13 tools selected                      │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ [☐] T1 - Planfräser Ø30mm (3 flutes)                  │ │
│  │     DC: 30mm | LCF: 8mm | L/D: 0.27                   │ │
│  │     💾 6 presets detected                              │ │
│  │     [Softwood] [Hardwood] [Aluminium]                  │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ [☐] T2 - End Mill Ø12mm (4 flutes)                    │ │
│  │     DC: 12mm | LCF: 30mm | L/D: 2.5                   │ │
│  │     ⚠️  No presets (will use defaults)                │ │
│  │     [Aluminium]                                         │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ [☐] T3 - Ball Nose Ø6mm (2 flutes)                    │ │
│  │     DC: 6mm | LCF: 15mm | L/D: 2.5                    │ │
│  │     ⚠️  High L/D ratio (reduced stability)            │ │
│  │     [Aluminium]                                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  [Cancel] [Continue with 0 tools →] (disabled)              │
└──────────────────────────────────────────────────────────────┘
```

**Key Features:**

1. **Multi-Select:**
   - Individual checkboxes per tool
   - "Select All" toggle
   - Visual count of selected tools
   - Continue button shows count

2. **Search & Filter:**
   - Search by tool number, name, diameter
   - Filter by tool type (End Mill, Ball Nose, etc.)
   - Filter by L/D ratio range
   - Filter by preset status (detected/defaults)

3. **Visual Indicators:**
   - 💾 = Presets detected
   - ⚠️ = Warnings (high L/D, no presets, etc.)
   - Material tags show detected materials

4. **Sorting:**
   - By tool number (default)
   - By diameter (ascending/descending)
   - By L/D ratio
   - By preset count

**User Interactions:**

```typescript
interface ToolSelectionState {
  selectedToolIds: Set<string>;
  searchQuery: string;
  filters: {
    toolType: string | null;
    ldRatio: { min: number; max: number } | null;
    presetStatus: 'all' | 'detected' | 'defaults';
  };
  sortBy: 'number' | 'diameter' | 'ld_ratio' | 'preset_count';
  sortDirection: 'asc' | 'desc';
}

// Toggle individual tool
const toggleTool = (toolId: string) => {
  setSelectedToolIds(prev => {
    const next = new Set(prev);
    if (next.has(toolId)) {
      next.delete(toolId);
    } else {
      next.add(toolId);
    }
    return next;
  });
};

// Select all visible tools
const selectAll = () => {
  const visibleToolIds = getFilteredTools().map(t => t.id);
  setSelectedToolIds(new Set(visibleToolIds));
};

// Clear selection
const clearAll = () => {
  setSelectedToolIds(new Set());
};
```

---

### 4.4.3 Screen 3: Material Selection per Tool

**Purpose:** Assign materials to each selected tool

**Layout:**

```
┌──────────────────────────────────────────────────────────────┐
│ [← Back] Step 3 of 6: Select Materials per Tool              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ℹ️  Assign materials for each selected tool                │
│  Materials sorted by machining hardness (soft→hard)          │
│                                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  📌 T1 - Planfräser Ø30mm (3 flutes)                        │
│  💾 Auto-detected: 3 materials from existing presets         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                               │
│  [☑] Softwood (Weichholz)      ← From: WoodS_*              │
│       vc: 800-1200 m/min                                      │
│  [☑] Hardwood (Hartholz)       ← From: WoodH_*              │
│       vc: 600-900 m/min                                       │
│  [☑] Aluminium (6061, 7075)    ← From: Alu_*                │
│       vc: 200-400 m/min                                       │
│  [☐] Brass (Messing)                                         │
│       vc: 150-250 m/min                                       │
│  [☐] Acrylic (PMMA)                                          │
│       vc: 300-600 m/min                                       │
│  [☐] Steel Mild (Baustahl)                                   │
│       vc: 100-180 m/min                                       │
│  [☐] Steel Stainless (V2A)                                   │
│       vc: 80-140 m/min                                        │
│                                                               │
│  Summary: 3 materials selected                                │
│                                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  📌 T2 - End Mill Ø12mm (4 flutes)                          │
│  🎯 Default pre-selection: Aluminium                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                               │
│  [☐] Softwood (Weichholz)                                    │
│  [☐] Hardwood (Hartholz)                                     │
│  [☑] Aluminium (6061, 7075)    ← Default                    │
│  [☐] Brass (Messing)                                         │
│  [☐] Acrylic (PMMA)                                          │
│  [☐] Steel Mild (Baustahl)                                   │
│  [☐] Steel Stainless (V2A)                                   │
│                                                               │
│  Summary: 1 material selected                                 │
│                                                               │
│  [← Back] [Continue: 4 materials total →]                   │
└──────────────────────────────────────────────────────────────┘
```

**Material Sorting Order (ALWAYS):**

```python
MATERIALS_BY_HARDNESS = [
    'Softwood',         # 1 - Easiest to machine
    'Hardwood',         # 2
    'Aluminium',        # 3
    'Brass',            # 4
    'Acrylic',          # 5
    'Steel_Mild',       # 6
    'Steel_Stainless'   # 7 - Hardest to machine
]
```

**Key Features:**

1. **Pre-Selection from Detection:**
   - Auto-check detected materials
   - Visual indicator showing source (← From: Alu_*)
   - User can modify (add/remove)

2. **Material Properties Display:**
   - Typical vc range for each material
   - Hardness ranking
   - Common use cases

3. **Batch Operations:**
   - "Apply to all tools" button
   - "Copy from T1" button
   - "Clear all" button

4. **Validation:**
   - At least 1 material per tool required
   - Warning if tool unsuitable for material

**State Management:**

```typescript
interface MaterialSelectionState {
  materialsByTool: Record<string, Set<string>>;
  // Example:
  // {
  //   'T1': Set(['Softwood', 'Hardwood', 'Aluminium']),
  //   'T2': Set(['Aluminium'])
  // }
}

// Apply material to tool
const toggleMaterial = (toolId: string, material: string) => {
  setMaterialsByTool(prev => {
    const toolMaterials = new Set(prev[toolId] || []);
    if (toolMaterials.has(material)) {
      toolMaterials.delete(material);
    } else {
      toolMaterials.add(material);
    }
    return {
      ...prev,
      [toolId]: toolMaterials
    };
  });
};

// Copy materials from one tool to another
const copyMaterialsToAll = (sourceToolId: string) => {
  const sourceMaterials = materialsByTool[sourceToolId];
  const updates: Record<string, Set<string>> = {};

  selectedToolIds.forEach(toolId => {
    updates[toolId] = new Set(sourceMaterials);
  });

  setMaterialsByTool(prev => ({ ...prev, ...updates }));
};
```

---

### 4.4.4 Screen 4: Operation Matrix (Tabular Layout)

**Purpose:** Select operations for each tool-material combination

**Layout:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ [← Back] Step 4 of 6: Operations                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  📌 T1 - Planfräser Ø30mm (3 flutes)                                │
│  [SW] [HW] [Alu]                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  ┌───────────┬────────────────┬──────────────┬───────────────────┐  │
│  │   FACE    │     SLOT       │   GEOMETRY   │     SPECIAL       │  │
│  │ ▓▓▓▓▓▓▓▓  │                │              │                   │  │
│  ├─────┬─────┼────┬────┬──────┼────┬────┬────┼────┬────┬────────┤  │
│  │Rough│Finis│Roug│Fini│ Full │Troc│Cham│Radi│Ball│Adap│Plung│Dr│  │
│  │  h  │  h  │  h │  sh│      │hoid│ fer│ us │    │ tive│  e  │il│  │
│  ├─────┼─────┼────┼────┼──────┼────┼────┼────┼────┼────┼─────┼──┤  │
│  │ ☑   │ ☑   │ ☐  │ ☐  │  ☐   │ ☐  │ ☐  │ ☐  │ ☐  │ ☐  │  ☐  │☐ │  │
│  └─────┴─────┴────┴────┴──────┴────┴────┴────┴────┴────┴─────┴──┘  │
│                                                                       │
│  Summary: 2 operations × 3 materials = 6 presets                    │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  📌 T2 - End Mill Ø12mm (4 flutes)                                  │
│  [Alu]                                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  ┌───────────┬────────────────┬──────────────┬───────────────────┐  │
│  │   FACE    │     SLOT       │   GEOMETRY   │     SPECIAL       │  │
│  ├─────┬─────┼────┬────┬──────┼────┬────┬────┼────┬────┬────────┤  │
│  │Rough│Finis│Roug│Fini│ Full │Troc│Cham│Radi│Ball│Adap│Plung│Dr│  │
│  ├─────┼─────┼────┼────┼──────┼────┼────┼────┼────┼────┼─────┼──┤  │
│  │ ☐   │ ☑   │ ☐  │ ☑  │  ☐   │ ☐  │ ☐  │ ☐  │ ☐  │ ☐  │  ☐  │☐ │  │
│  └─────┴─────┴────┴────┴──────┴────┴────┴────┴────┴────┴─────┴──┘  │
│                                                                       │
│  Summary: 2 operations × 1 material = 2 presets                     │
│                                                                       │
│  [← Back] [Calculate 8 Presets →]                                   │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Features:**

1. **Group Toggle:**
   - Click on group header (FACE, SLOT, etc.) toggles all operations in group
   - Visual feedback: Green background when fully selected
   - Partial selection indicator (◐) when some selected

2. **Material Tags:**
   - Compact display: [SW] = Softwood, [HW] = Hardwood, [Alu] = Aluminium
   - Shows which materials will be calculated for this tool

3. **Operation Groups:**

```typescript
const OPERATION_GROUPS = [
  {
    id: 'FACE',
    name: 'FACE',
    color: '#fb923c', // Orange
    operations: ['FACE_ROUGH', 'FACE_FINISH']
  },
  {
    id: 'SLOT',
    name: 'SLOT',
    color: '#3b82f6', // Blue
    operations: ['SLOT_ROUGH', 'SLOT_FINISH', 'SLOT_FULL', 'SLOT_TROCHOIDAL']
  },
  {
    id: 'GEOMETRY',
    name: 'GEOMETRY',
    color: '#06b6d4', // Cyan
    operations: ['GEOMETRY_CHAMFER', 'GEOMETRY_RADIUS', 'GEOMETRY_BALL']
  },
  {
    id: 'SPECIAL',
    name: 'SPECIAL',
    color: '#a855f7', // Purple
    operations: ['SPECIAL_ADAPTIVE', 'SPECIAL_PLUNGE', 'SPECIAL_DRILL']
  }
];
```

4. **Preset Counter:**
   - Real-time calculation of total presets
   - Formula: (selected operations) × (selected materials) × (selected tools)

**User Interactions:**

```typescript
interface OperationSelectionState {
  operationsByTool: Record<string, Set<string>>;
  // Example:
  // {
  //   'T1': Set(['FACE_ROUGH', 'FACE_FINISH']),
  //   'T2': Set(['FACE_FINISH', 'SLOT_FINISH'])
  // }
}

// Toggle single operation
const toggleOperation = (toolId: string, operationId: string) => {
  setOperationsByTool(prev => {
    const toolOps = new Set(prev[toolId] || []);
    if (toolOps.has(operationId)) {
      toolOps.delete(operationId);
    } else {
      toolOps.add(operationId);
    }
    return {
      ...prev,
      [toolId]: toolOps
    };
  });
};

// Toggle entire group
const toggleGroup = (toolId: string, groupId: string) => {
  const group = OPERATION_GROUPS.find(g => g.id === groupId);
  if (!group) return;

  const toolOps = new Set(operationsByTool[toolId] || []);
  const groupOps = new Set(group.operations);

  // Check if all group operations are selected
  const allSelected = group.operations.every(op => toolOps.has(op));

  if (allSelected) {
    // Deselect all
    group.operations.forEach(op => toolOps.delete(op));
  } else {
    // Select all
    group.operations.forEach(op => toolOps.add(op));
  }

  setOperationsByTool(prev => ({
    ...prev,
    [toolId]: toolOps
  }));
};

// Calculate total presets
const getTotalPresets = (): number => {
  let total = 0;

  selectedToolIds.forEach(toolId => {
    const materials = materialsByTool[toolId]?.size || 0;
    const operations = operationsByTool[toolId]?.size || 0;
    total += materials * operations;
  });

  return total;
};
```

**Validation:**

- ⚠️ Warning if SLOT_FULL selected for high L/D ratio tools
- ⚠️ Warning if SLOT_TROCHOIDAL selected but no CAM support
- ⚠️ Warning if > 100 presets (long calculation time)

---

### 4.4.5 Screen 5: Coating + Surface Quality + Coolant

*(Already detailed in Section 2.4 - Coating System)*

---

### 4.4.6 Screen 6: Calculation Progress

**Purpose:** Show real-time calculation progress

**Layout:**

```
┌────────────────────────────────────────────────────────────────────┐
│ Calculating Presets...                                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ⏳ Running calculations...                                         │
│                                                                      │
│  Progress: 3 of 8 presets calculated (37%)                         │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 37%      │
│                                                                      │
│  ✅ T1 - Planfräser Ø30mm                                          │
│     • Softwood_Face_Rough  → SAFE ✓                                │
│     • Softwood_Face_Finish → SAFE ✓                                │
│     • Hardwood_Face_Rough  → WARNING ⚠️ (High chip temp)          │
│                                                                      │
│  🔄 T2 - End Mill Ø12mm                                            │
│     • Aluminium_Face_Finish → Calculating...                        │
│     • Aluminium_Slot_Finish → Queued                                │
│                                                                      │
│  Estimated time remaining: 2 seconds                                │
└────────────────────────────────────────────────────────────────────┘
```

**Implementation (WebSocket Updates):**

```typescript
interface CalculationProgress {
  status: 'queued' | 'running' | 'completed' | 'failed';
  completedPresets: number;
  totalPresets: number;
  currentPreset: string | null;
  results: PresetResult[];
  estimatedTimeRemaining: number; // seconds
}

// WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/calculation/{taskId}');

ws.onmessage = (event) => {
  const progress: CalculationProgress = JSON.parse(event.data);

  // Update UI
  setProgress(progress);

  // Auto-redirect when complete
  if (progress.status === 'completed') {
    setTimeout(() => {
      navigate('/results');
    }, 1000);
  }
};
```

**Features:**

1. **Real-time Updates:**
   - Progress bar updates as each preset completes
   - Live status per preset
   - Estimated time remaining

2. **Validation Status:**
   - ✅ SAFE (green)
   - ⚠️ WARNING (yellow)
   - ❌ UNSAFE (red)

3. **Error Handling:**
   - Individual preset failures don't stop batch
   - Error details shown per preset
   - Option to retry failed presets

---

### 4.4.7 Screen 7: Results Display with Filtering

*(Detailed specifications from DELTA_REQUEST, as shown earlier)*

**Key Features:**

- Bidirectional scrolling (horizontal + vertical)
- Sortable columns with custom preset name sorting
- Status filter toggle buttons
- Expandable rows for detailed view
- Export buttons

---

### 4.4.8 Screen 8: Expert Mode with Parameter Overrides

*(Detailed in Section 4.6 below)*

---

## 4.5 EXPERT MODE UI

### 4.5.1 Overview

**Purpose:** Allow advanced users to override calculated parameters with full control

**Access:** Available in two places:
1. During operation selection (per-tool overrides)
2. After results are calculated (global adjustments)

**Philosophy:** Progressive disclosure - hidden by default, powerful when needed

---

### 4.5.2 Expert Mode Panel - Detailed Layout

**Location:** Screen 4 (Operation Matrix) - Expandable per Tool

**Initial State (Collapsed):**

```
┌────────────────────────────────────────────────────────────────┐
│ 📌 T2 - End Mill Ø12mm Z4 • DC=12mm • LCF=30mm • L/D=2.5     │
│ [Alu]                                                          │
│                                                                 │
│ [⚙️  Show Expert Mode]  ← Toggle Button                       │
└────────────────────────────────────────────────────────────────┘
```

**Expanded State (Full Expert Mode):**

```
┌────────────────────────────────────────────────────────────────┐
│ 📌 T2 - End Mill Ø12mm Z4 • DC=12mm • LCF=30mm • L/D=2.5     │
│ [Alu]                                                          │
│                                                                 │
│ [⚙️  Hide Expert Mode]                                         │
│                                                                 │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ ⚙️  EXPERT MODE                                          │  │
│ │                                                           │  │
│ │ Selected Operation: FACE_FINISH                          │  │
│ │                                                           │  │
│ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│ │ GLOBAL ADJUSTMENT SLIDER                                 │  │
│ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│ │                                                           │  │
│ │  Conservative   ←────●───────────→   Aggressive          │  │
│ │      -50%           0%            +50%                    │  │
│ │                                                           │  │
│ │  Current: +15% (Moderate Aggressive)                     │  │
│ │                                                           │  │
│ │  Effect on all parameters:                               │  │
│ │  • vc: ×1.15 (faster cutting speed)                      │  │
│ │  • vf: ×1.15 (faster feed rate)                          │  │
│ │  • ae: ×1.15 (wider radial engagement)                   │  │
│ │  • ap: ×1.15 (deeper axial cut)                          │  │
│ │                                                           │  │
│ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│ │ AP REFERENCE OVERRIDE                                    │  │
│ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│ │                                                           │  │
│ │ ap Reference:                                            │  │
│ │ ● 🤖 Auto (Recommended)                                  │  │
│ │   System uses DC for FACE operations                     │  │
│ │                                                           │  │
│ │ ○ 📏 Manual Override:                                    │  │
│ │   [DC ▼] [LCF]                                           │  │
│ │                                                           │  │
│ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│ │ INDIVIDUAL PARAMETER OVERRIDES (Optional)                │  │
│ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│ │                                                           │  │
│ │ Radial Engagement (ae):                                  │  │
│ │ [ 9.0 ] mm ← Base: 7.5mm × Global(1.15) × Manual(1.04)  │  │
│ │ ├──────────────●────────────┤                            │  │
│ │ 3.75mm (50%)   7.5mm (100%)   15mm (200%)               │  │
│ │                                                           │  │
│ │ Axial Depth (ap):                                        │  │
│ │ [ 4.1 ] mm ← Base: 3.6mm × Global(1.15) × Manual(1.00)  │  │
│ │ ├──────────────●────────────┤                            │  │
│ │ 1.8mm (50%)    3.6mm (100%)   7.2mm (200%)              │  │
│ │                                                           │  │
│ │ Chip Load (fz):                                          │  │
│ │ [ 0.09 ] mm/tooth ← Base: 0.08mm × Global(1.15)         │  │
│ │ ├──────────────●────────────┤                            │  │
│ │ 0.04mm (50%)   0.08mm (100%)  0.16mm (200%)             │  │
│ │                                                           │  │
│ │ Cutting Speed (vc):                                      │  │
│ │ [ 138 ] m/min ← Base: 120 m/min × Global(1.15)          │  │
│ │ ├──────────────●────────────┤                            │  │
│ │ 60 m/min (50%) 120 m/min (100%) 240 m/min (200%)        │  │
│ │                                                           │  │
│ │ [Reset All] [Apply Overrides]                            │  │
│ └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

---

### 4.5.3 Global Adjustment Slider

**Concept:** Single slider affects ALL parameters proportionally

**Range:** -50% to +50%

**Default:** 0% (no adjustment)

**Use Cases:**
- **Conservative (-20% to -50%):** First time using tool, unknown material hardness, safety priority
- **Standard (0%):** Calculated safe values
- **Moderate (+10% to +25%):** Experienced user, proven setup, time optimization
- **Aggressive (+30% to +50%):** Production environment, tool wear acceptable, maximum MRR

**Implementation:**

```typescript
interface ExpertModeState {
  globalAdjustment: number; // -50 to +50
  apReferenceOverride: 'AUTO' | 'DC' | 'LCF';
  individualOverrides: {
    ae?: number;
    ap?: number;
    fz?: number;
    vc?: number;
  };
}

// Apply global adjustment
function applyGlobalAdjustment(baseValue: number, adjustment: number): number {
  const factor = 1 + (adjustment / 100);
  return baseValue * factor;
}

// Example
const vc_base = 120; // m/min
const global = 15; // +15%
const vc_adjusted = applyGlobalAdjustment(vc_base, global);
// Result: 120 × 1.15 = 138 m/min
```

**Visual Feedback:**

```tsx
<div className="global-slider">
  <label>Global Adjustment</label>
  <input
    type="range"
    min="-50"
    max="50"
    value={globalAdjustment}
    onChange={(e) => setGlobalAdjustment(parseInt(e.target.value))}
    className={`slider ${
      globalAdjustment < -20 ? 'conservative' :
      globalAdjustment > 20 ? 'aggressive' :
      'standard'
    }`}
  />
  <div className="slider-labels">
    <span className="conservative">Conservative</span>
    <span className="standard">0%</span>
    <span className="aggressive">Aggressive</span>
  </div>
  <div className="slider-value">
    Current: {globalAdjustment > 0 ? '+' : ''}{globalAdjustment}%
    {globalAdjustment < -20 && ' (Very Conservative)'}
    {globalAdjustment > 20 && ' (Very Aggressive)'}
  </div>
  <div className="slider-effects">
    Effect on all parameters:
    <ul>
      <li>vc: ×{(1 + globalAdjustment/100).toFixed(2)}</li>
      <li>vf: ×{(1 + globalAdjustment/100).toFixed(2)}</li>
      <li>ae: ×{(1 + globalAdjustment/100).toFixed(2)}</li>
      <li>ap: ×{(1 + globalAdjustment/100).toFixed(2)}</li>
    </ul>
  </div>
</div>
```

---

### 4.5.4 AP Reference Override

**Purpose:** Allow manual control of axial depth reference (DC vs LCF)

**Default Behavior (AUTO):**

```python
def get_ap_reference_auto(operation: OperationType, geometry: Geometry) -> str:
    """
    Automatic ap reference determination.
    """
    ld_ratio = geometry.LCF / geometry.DC

    # FACE operations always use DC
    if operation in ['FACE_ROUGH', 'FACE_FINISH']:
        return 'DC'

    # SLOT_FULL always uses DC
    if operation == 'SLOT_FULL':
        return 'DC'

    # SPECIAL_ADAPTIVE always uses LCF
    if operation == 'SPECIAL_ADAPTIVE':
        return 'LCF'

    # Dynamic based on L/D ratio
    if ld_ratio < 1.0:
        return 'DC'  # Short tool
    else:
        return 'LCF'  # Long tool
```

**Manual Override UI:**

```
ap Reference:
● 🤖 Auto (Recommended)
  System uses DC for FACE operations

○ 📏 Manual Override:
  [DC ▼] [LCF]
```

**When user selects Manual Override:**

```
ap Reference:
○ 🤖 Auto (Recommended)

● 📏 Manual Override:
  ● DC   ○ LCF

💡 Current selection: DC
   Base value: 30% of 12mm = 3.6mm
```

**With Warning (if conflicts with best practice):**

```
ap Reference:
○ 🤖 Auto (Recommended)

● 📏 Manual Override:
  ○ DC   ● LCF

⚠️  WARNING: Override conflicts with best practices

Recommended: DC (for FACE operations)
Your override: LCF

Impact:
• ap = 15mm (50% of 30mm LCF) instead of 3.6mm
• Risk: Excessive axial load in steel
• Risk: Tool deflection and chatter

[⚠️  Apply Override Anyway] [✓ Reset to Auto]
```

**Validation Function:**

```python
def validate_ap_reference_override(
    operation: OperationType,
    geometry: Geometry,
    override: str
) -> ValidationResult:
    """
    Validates manual ap reference override.
    """
    recommended = get_ap_reference_auto(operation, geometry)

    if override == recommended:
        return ValidationResult(
            valid=True,
            severity='INFO',
            message=f'Manual selection matches recommendation ({override})'
        )

    # Calculate impact
    if override == 'LCF':
        ap_value = geometry.LCF * 0.5  # Assuming 50% factor
    else:
        ap_value = geometry.DC * 0.5

    warnings = []

    # FACE operation with LCF is problematic
    if operation in ['FACE_ROUGH', 'FACE_FINISH'] and override == 'LCF':
        warnings.append({
            'severity': 'WARNING',
            'message': f'FACE operations should use DC reference. '
                      f'LCF override will result in ap={ap_value:.1f}mm, '
                      f'which may cause excessive tool deflection.',
            'recommendation': 'Use DC reference for FACE operations'
        })

    # Short tool with LCF
    ld_ratio = geometry.LCF / geometry.DC
    if ld_ratio < 1.0 and override == 'LCF':
        warnings.append({
            'severity': 'CAUTION',
            'message': f'Short tool (L/D={ld_ratio:.2f}) typically uses DC. '
                      f'LCF override may be unnecessarily conservative.',
            'recommendation': 'Consider using DC for short tools'
        })

    return ValidationResult(
        valid=True,  # Allow but warn
        severity='WARNING' if warnings else 'INFO',
        warnings=warnings
    )
```

---

### 4.5.5 Individual Parameter Overrides

**Purpose:** Fine-tune individual parameters beyond global adjustment

**Calculation Order:**

```
Final Value = Base Value × Global Factor × Individual Override
```

**Example:**

```
ae calculation:
1. Base: 7.5mm (from operation + material)
2. Global: ×1.15 (+15% aggressive)
   = 7.5 × 1.15 = 8.625mm
3. Individual: ×1.04 (+4% manual adjustment)
   = 8.625 × 1.04 = 8.97mm ≈ 9.0mm
```

**UI Components:**

```tsx
interface ParameterOverride {
  name: string;
  unit: string;
  baseValue: number;
  globalAdjusted: number;
  manualOverride: number;
  finalValue: number;
  min: number;
  max: number;
}

const ParameterSlider: React.FC<{ param: ParameterOverride }> = ({ param }) => {
  return (
    <div className="parameter-override">
      <label>{param.name} ({param.unit})</label>

      {/* Formula display */}
      <div className="formula">
        [{param.finalValue.toFixed(2)}] {param.unit} ←
        Base: {param.baseValue.toFixed(2)}{param.unit} ×
        Global({(globalAdjustment/100 + 1).toFixed(2)}) ×
        Manual({param.manualOverride.toFixed(2)})
      </div>

      {/* Slider */}
      <input
        type="range"
        min={param.min}
        max={param.max}
        step="0.01"
        value={param.manualOverride}
        onChange={(e) => handleManualOverride(param.name, parseFloat(e.target.value))}
        className="parameter-slider"
      />

      {/* Scale markers */}
      <div className="slider-markers">
        <span>{(param.baseValue * 0.5).toFixed(2)} (50%)</span>
        <span>{param.baseValue.toFixed(2)} (100%)</span>
        <span>{(param.baseValue * 2.0).toFixed(2)} (200%)</span>
      </div>
    </div>
  );
};
```

**Parameter Ranges:**

```typescript
const PARAMETER_RANGES = {
  ae: {
    min: 0.5,  // 50% of base
    max: 2.0,  // 200% of base
    step: 0.01,
    displayDecimals: 1
  },
  ap: {
    min: 0.5,
    max: 2.0,
    step: 0.01,
    displayDecimals: 1
  },
  fz: {
    min: 0.5,
    max: 2.0,
    step: 0.01,
    displayDecimals: 3  // More precision for small values
  },
  vc: {
    min: 0.5,
    max: 2.0,
    step: 0.01,
    displayDecimals: 0  // Whole numbers
  }
};
```

---

### 4.5.6 Warnings and Validation

**Real-time Validation:**

As user adjusts parameters, validate against safe ranges:

```typescript
interface ValidationResult {
  parameter: string;
  severity: 'INFO' | 'WARNING' | 'ERROR';
  message: string;
  recommendations: string[];
}

function validateOverride(
  parameter: string,
  value: number,
  baseValue: number,
  material: string,
  operation: string
): ValidationResult {
  const ratio = value / baseValue;

  // ae validation
  if (parameter === 'ae') {
    if (ratio > 1.5) {
      return {
        parameter: 'ae',
        severity: 'WARNING',
        message: `ae is ${(ratio * 100).toFixed(0)}% of recommended. High radial forces expected.`,
        recommendations: [
          'Monitor tool deflection',
          'Watch for chatter',
          'Consider reducing if vibrations occur'
        ]
      };
    }
  }

  // ap validation
  if (parameter === 'ap') {
    if (ratio > 1.8) {
      return {
        parameter: 'ap',
        severity: 'ERROR',
        message: `ap is ${(ratio * 100).toFixed(0)}% of recommended. Tool breakage risk!`,
        recommendations: [
          'REDUCE ap immediately',
          'Maximum safe ap is 150-180% of base',
          'Consider multiple passes instead'
        ]
      };
    }
  }

  // vc validation (material-specific)
  if (parameter === 'vc') {
    const vcLimits = VC_LIMITS[material];
    if (value > vcLimits.max) {
      return {
        parameter: 'vc',
        severity: 'WARNING',
        message: `vc exceeds material limit (${vcLimits.max} m/min for ${material})`,
        recommendations: [
          `Reduce vc to < ${vcLimits.max} m/min`,
          'Risk: Excessive heat and tool wear'
        ]
      };
    }
  }

  return {
    parameter,
    severity: 'INFO',
    message: 'Parameter within safe range',
    recommendations: []
  };
}
```

**Display Warnings in UI:**

```tsx
const WarningBanner: React.FC<{ validation: ValidationResult }> = ({ validation }) => {
  if (validation.severity === 'INFO') return null;

  const severityClasses = {
    WARNING: 'warning-banner warning',
    ERROR: 'warning-banner error'
  };

  return (
    <div className={severityClasses[validation.severity]}>
      <div className="warning-icon">
        {validation.severity === 'ERROR' ? '🔴' : '⚠️'}
      </div>
      <div className="warning-content">
        <h4>{validation.message}</h4>
        {validation.recommendations.length > 0 && (
          <ul>
            {validation.recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};
```

---

### 4.5.7 Reset and Apply Actions

**Reset Buttons:**

```tsx
// Reset all to defaults
<button onClick={handleResetAll} className="btn btn-secondary">
  Reset All to Defaults
</button>

// Reset only global
<button onClick={() => setGlobalAdjustment(0)} className="btn btn-outline">
  Reset Global Slider
</button>

// Reset only individual overrides
<button onClick={handleResetIndividual} className="btn btn-outline">
  Reset Individual Overrides
</button>
```

**Apply Logic:**

```typescript
function handleApplyOverrides() {
  // Validate all parameters
  const validations = validateAllParameters();

  // Check for errors
  const errors = validations.filter(v => v.severity === 'ERROR');
  if (errors.length > 0) {
    showError('Cannot apply overrides with errors. Please fix highlighted parameters.');
    return;
  }

  // Check for warnings
  const warnings = validations.filter(v => v.severity === 'WARNING');
  if (warnings.length > 0) {
    // Show confirmation dialog
    showConfirmDialog({
      title: 'Warning: Aggressive Parameters',
      message: `${warnings.length} parameters have warnings. Apply anyway?`,
      warnings: warnings,
      onConfirm: () => applyOverrides(),
      onCancel: () => {}
    });
    return;
  }

  // No issues - apply directly
  applyOverrides();
}

function applyOverrides() {
  // Save to state
  saveExpertModeSettings({
    globalAdjustment,
    apReferenceOverride,
    individualOverrides
  });

  // Show success message
  showSuccess('Expert mode settings applied. Calculations will use your overrides.');

  // Close expert mode panel (optional)
  setExpertModeOpen(false);
}
```

---

### 4.5.8 Persistence and State Management

**State Structure:**

```typescript
interface ExpertModeSettings {
  enabled: boolean;
  perToolSettings: Record<string, ToolExpertSettings>;
}

interface ToolExpertSettings {
  globalAdjustment: number;
  apReferenceOverride: 'AUTO' | 'DC' | 'LCF';
  parameterOverrides: {
    ae?: number;
    ap?: number;
    fz?: number;
    vc?: number;
  };
  appliedAt: Date;
}

// Zustand store
interface ExpertModeStore {
  settings: ExpertModeSettings;
  setGlobalAdjustment: (toolId: string, value: number) => void;
  setApReference: (toolId: string, ref: 'AUTO' | 'DC' | 'LCF') => void;
  setParameterOverride: (toolId: string, param: string, value: number) => void;
  resetTool: (toolId: string) => void;
  resetAll: () => void;
}

export const useExpertModeStore = create<ExpertModeStore>((set) => ({
  settings: {
    enabled: false,
    perToolSettings: {}
  },

  setGlobalAdjustment: (toolId, value) => set((state) => ({
    settings: {
      ...state.settings,
      perToolSettings: {
        ...state.settings.perToolSettings,
        [toolId]: {
          ...state.settings.perToolSettings[toolId],
          globalAdjustment: value
        }
      }
    }
  })),

  // ... other actions
}));
```

**Persistence:**

```typescript
// Save to localStorage on change
useEffect(() => {
  localStorage.setItem('expertMode', JSON.stringify(expertModeSettings));
}, [expertModeSettings]);

// Load on mount
useEffect(() => {
  const saved = localStorage.getItem('expertMode');
  if (saved) {
    const parsed = JSON.parse(saved);
    setExpertModeSettings(parsed);
  }
}, []);
```

---

### 4.5.9 Expert Mode in Results Display

**Show Expert Mode Indicators in Results Table:**

```
┌────────────────────────────────────────────────────────────────┐
│ 📊 Results (8 presets)                                         │
│ ⚙️  Expert Mode Active: +15% Global Adjustment                │
├────────────────────────────────────────────────────────────────┤
│ Preset          │St│vc │  n  │fz │ vf  │ae  │ap  │MRR │Expert│
│                 │  │m/m│ rpm │mm │mm/mn│% DC│% DC│cm³ │      │
├─────────────────┼──┼───┼─────┼───┼─────┼────┼────┼────┼──────┤
│Steel_F_Fin ✓    │✓ │138│3661 │.09│ 988 │75  │30  │24  │ ⚙️   │
│                 │  │   │     │   │     │    │    │    │+15%  │
└────────────────────────────────────────────────────────────────┘
```

**Expandable Details:**

```
[Click on ⚙️ icon to show details]

┌────────────────────────────────────────────────────────────────┐
│ Expert Mode Settings for Steel_Face_Finish                    │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Global Adjustment: +15%                                        │
│ ap Reference: DC (Auto)                                        │
│                                                                 │
│ Parameter Adjustments:                                         │
│ ───────────────────────────────────────────────────────────── │
│ Parameter │ Base  │ Global│ Manual│ Final │ Change            │
│ ──────────┼───────┼───────┼───────┼───────┼──────────────     │
│ vc        │ 120   │ ×1.15 │ ×1.00 │ 138   │ +18 m/min (+15%) │
│ n         │ 3183  │ ×1.15 │ ×1.00 │ 3661  │ +478 rpm (+15%)  │
│ fz        │ 0.08  │ ×1.15 │ ×1.00 │ 0.09  │ +0.01 mm (+15%)  │
│ vf        │ 859   │ ×1.15 │ ×1.00 │ 988   │ +129 mm/min      │
│ ae        │ 9.0   │ ×1.15 │ ×1.00 │ 10.4  │ +1.4 mm (+15%)   │
│ ap        │ 3.6   │ ×1.15 │ ×1.00 │ 4.1   │ +0.5 mm (+15%)   │
│                                                                 │
│ [Edit Expert Mode] [Reset to Defaults]                        │
└────────────────────────────────────────────────────────────────┘
```

---

## 4.6 MATHEMATICAL WORKBOOK

### 4.6.1 Overview

**Purpose:** Show complete calculation breakdown with all intermediate steps

**Access:** Click "📊 Workbook" button in results screen

**Philosophy:** Educational + transparency - show how every number is calculated

---

### 4.6.2 Workbook Layout

**Full Screen Modal:**

```
┌──────────────────────────────────────────────────────────────────────┐
│ [← Back to Results] Mathematical Workbook: Steel_Face_Finish         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│ 📊 COMPLETE CALCULATION BREAKDOWN                                    │
│                                                                        │
│ Tool: T2 - End Mill Ø12mm Z4                                         │
│ Material: Steel Mild (C45)                                           │
│ Operation: FACE_FINISH                                                │
│ Coating: TiAlN (+60%)                                                │
│ Surface Quality: FINISHING (-20% ae/ap)                             │
│ Coolant: Flood                                                        │
│                                                                        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│ PHASE 1: Material Base Values                                        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                        │
│ vc_base (Cutting Speed - Material):                                  │
│   Material: Steel_Mild                                               │
│   Base vc: 120 m/min                                                 │
│   Source: MATERIAL_DATABASE['Steel_Mild']['vc_base']                 │
│                                                                        │
│ fz_base (Chip Load - Material):                                      │
│   Material: Steel_Mild                                               │
│   DC: 12 mm                                                          │
│   Formula: fz = 0.05 + (DC - 6) × 0.002                             │
│   fz_base = 0.05 + (12 - 6) × 0.002                                 │
│   fz_base = 0.05 + 0.012 = 0.062 mm/tooth                           │
│                                                                        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│ PHASE 2: Coating Factor Application                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                        │
│ Coating: TiAlN                                                       │
│ Factor: 1.6× (+60%)                                                  │
│                                                                        │
│ vc_coated = vc_base × coating_factor                                │
│ vc_coated = 120 m/min × 1.6                                          │
│ vc_coated = 192 m/min                                                │
│                                                                        │
│ 💡 TiAlN is excellent for steel - high temperature resistance        │
│                                                                        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│ PHASE 3: Operation-Specific Adjustments                              │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                        │
│ Operation: FACE_FINISH                                                │
│                                                                        │
│ ae (Radial Engagement):                                              │
│   ae_factor: 0.25 (25% of DC for face milling)                      │
│   ae_base = DC × 0.25 = 12mm × 0.25 = 3.0 mm                        │
│                                                                        │
│ ap (Axial Depth):                                                    │
│   ap_reference: DC (correct for FACE operations)                     │
│   ap_factor: 0.15 (15% of DC for finishing)                         │
│   ap_base = DC × 0.15 = 12mm × 0.15 = 1.8 mm                        │
│                                                                        │
│ fz Adjustment for Finishing:                                         │
│   fz_operation_factor: 0.8 (20% reduction for better surface)       │
│   fz_adjusted = fz_base × 0.8                                        │
│   fz_adjusted = 0.062 mm/tooth × 0.8 = 0.0496 mm/tooth              │
│                                                                        │
│ vc Adjustment for Finishing:                                         │
│   vc_operation_factor: 1.2 (20% increase for better surface)        │
│   vc_adjusted = vc_coated × 1.2                                      │
│   vc_adjusted = 192 m/min × 1.2 = 230.4 m/min                       │
│                                                                        │
│ [Continue to Phase 4 →]                                              │
│                                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

**Phase 4-10 screens continue similarly...**

---

### 4.6.3 Reference Values Comparison

**When Fusion 360 presets were detected:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REFERENCE COMPARISON (from imported Fusion preset)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Parameter │ Calculated │ Fusion Ref │ Deviation │ Status
──────────┼────────────┼────────────┼───────────┼─────────────────
vc        │ 192 m/min  │ 180 m/min  │ +6.7%     │ ✓ Acceptable
n         │ 5093 rpm   │ 4775 rpm   │ +6.7%     │ ✓ Acceptable
fz        │ 0.050 mm   │ 0.055 mm   │ -9.1%     │ ✓ Acceptable
vf        │ 1018 mm/mn │ 1050 mm/mn │ -3.0%     │ ✓ Acceptable
ae        │ 3.0 mm     │ 3.0 mm     │ 0.0%      │ ✓ Match
ap        │ 1.8 mm     │ 2.0 mm     │ -10.0%    │ ⚠️ More conservative

💡 Interpretation:
Our calculations are slightly more conservative than Fusion 360 values.
This is intentional for hobby CNC safety.

Deviations < 15% are normal and acceptable.
Our values prioritize tool life over maximum MRR.
```

---

### 4.7 State Management

**Zustand Stores:**
- `useWorkflowStore` - Current Step, Navigation, Completed Steps
- `useToolStore` - Tools, Selected Tools, Coating
- `useMaterialStore` - Materials by Tool
- `useOperationStore` - Selected Operations
- `useResultsStore` - Calculation Results

**React Query:** Server State (API Calls, Caching)

---

## TEIL 5: EXPORT-MODUL (Zusammenfassung)

### Fusion 360 Parametric Export

**Kritisch:** 13 Expressions PRO Preset (MANDATORY!)

```
1. tool_surfaceSpeed = "527.8 mpm"
2. tool_feedPerTooth = "0.09 mm"
3. tool_feedEntry = "tool_feedCutting*0.5"
4. tool_feedExit = "tool_feedCutting*1.0"
5. tool_feedPlunge = "tool_feedCutting*0.25"
6. tool_feedRamp = "tool_feedCutting*0.5"
7. tool_feedTransition = "tool_feedCutting*1.0"
8. tool_rampSpindleSpeed = "tool_spindleSpeed*1.0"
9. tool_stepdown = "tool_fluteLength*0.1875"  (ap-Referenz: DC oder LCF!)
10. tool_stepover = "tool_diameter*0.25"
11. tool_coolant = "'disabled'"
12. use_tool_stepdown = "true"
13. use_tool_stepover = "true"
```

**Weitere Exports:**
- CSV (simple, for Excel)
- JSON (für andere Tools)
- PDF (Report mit Tabellen + Warnings)

---

## TEIL 6: USER STORIES & EPICS (Zusammenfassung)

### Epic E1: Tool Import & Selection

**US1.1:** Als User möchte ich .tools Files importieren
**US1.2:** Als User möchte ich Tools auswählen (Multi-Select)
**US1.3:** Als User möchte ich Coating wählen (Dropdown)

### Epic E2: Material & Operation Selection

**US2.1:** Als User möchte ich Materialien PRO TOOL wählen (NICHT global!)
**US2.2:** Als User möchte ich Materialien nach Härte sortiert sehen
**US2.3:** Als User möchte ich Surface Quality wählen
**US2.4:** Als User möchte ich Operationen aus 13 Ops wählen (inkl. SLOT_TROCHOIDAL)
**US2.5:** Als User möchte ich Operationen nach Kategorie gruppiert sehen (4 Farben)

### Epic E3: Calculation & Results

**US3.1:** Als User möchte ich Berechnungen starten (max 2s für 100 Presets)
**US3.2:** Als User möchte ich Progress sehen (bei > 100 Presets)
**US3.3:** Als User möchte ich Results filtern (OK/Warning/Error)
**US3.4:** Als User möchte ich Results nach Tool gruppiert sehen
**US3.5:** Als User möchte ich Warnings/Errors verstehen (klare Messages)

### Epic E4: Export

**US4.1:** Als User möchte ich zu Fusion 360 exportieren (parametric!)
**US4.2:** Als User möchte ich zu CSV/Excel exportieren
**US4.3:** Als User möchte ich Export-Validation sehen (KEINE Fusion-Warnings!)

### Epic E5: Expert Mode & Workbook

**US5.1:** Als Expert möchte ich Global Slider (-50% bis +50%)
**US5.2:** Als Expert möchte ich Individual Parameters überschreiben (ae/ap/fz)
**US5.3:** Als Expert möchte ich Entry Parameters ändern (vf_ramp, ramp_angle)
**US5.4:** Als Expert möchte ich Mathematical Workbook sehen (10 Phasen detailliert)

---

## TEIL 7: IMPLEMENTIERUNGS-STRATEGIE (Zusammenfassung)

### 3-Phasen-Plan

**Phase 1: Foundation (Woche 1-2)**
```
Sprint 1: Design System Setup
  - Design Tokens CSS (v0.3_production)
  - Inter/Work Sans/Fira Code Fonts
  - Core Layout Components

Sprint 2: API Scaffolding
  - FastAPI Setup + OpenAPI
  - Pydantic Models (Tool, Preset, etc.)
  - V2.0 Engine Wrapper (NO-TOUCH!)
  - Database Models (SQLAlchemy)
```

**Phase 2: Core Features (Woche 3-5)**
```
Sprint 3: Basis-Workflow (Screens 1-4)
  - Import Screen + .tools Parser
  - Tool Selection + Coating
  - Material Selection (PER TOOL!)
  - Operation Matrix (13 Ops)

Sprint 4: Calculation + Results (Screens 5-6)
  - 10-Phasen Calculation
  - 8-Checks Validation
  - Results Table + Filtering
  - Status Badges (OK/Warning/Error)

Sprint 5: Export (Screen 7)
  - Fusion Parametric Export (13 Expressions!)
  - CSV/JSON Export
  - Export Validation
```

**Phase 3: Advanced Features (Woche 6-8)**
```
Sprint 6: Expert Mode (Screen 8)
  - Global Slider Component
  - CompactSliders für ae/ap/fz
  - Entry Parameters Override
  - Validation & Warnings

Sprint 7: Mathematical Workbook
  - 10-Phasen Detail-View
  - Formeln anzeigen
  - Intermediate Values
  - Educational Mode

Sprint 8: Polish & Optimization
  - Performance (< 2s für 100 Presets)
  - Celery für > 100 Presets
  - Error Handling
  - Testing (85% Coverage)
```

### Migration vom Prototyp

**Option A: Prototyp als Basis (EMPFOHLEN)**
1. Prototyp-Code als Startpunkt
2. Design System bereits vorhanden
3. Komponenten (Slider, Table) fertig
4. Nur Business-Logic hinzufügen

**Option B: Greenfield**
1. Neues Projekt von Grund auf
2. Prototyp als Referenz
3. Mehr Kontrolle, aber mehr Aufwand

**Empfehlung:** Option A - spart ~30-40% Zeit

---

### 7.4 Testing Strategy (COMPLETE)

**Testing Pyramid:**

```
                    ▲
                   ╱ ╲
                  ╱   ╲
                 ╱ E2E ╲              5-10 Tests
                ╱───────╲
               ╱         ╲
              ╱Integration╲           20-30 Tests
             ╱─────────────╲
            ╱               ╲
           ╱   Unit Tests    ╲       100-150 Tests
          ╱───────────────────╲
         ╱                     ╲
        ╱_______________________╲
```

**Coverage Target:** 85% overall
- Backend: 90%+ (calculation logic critical)
- Frontend: 75%+ (UI logic)
- Integration: 80%+ (API contracts)

---

#### 7.4.1 Unit Tests

**Backend Unit Tests (pytest):**

```python
# tests/test_calculations.py
import pytest
from core.v2_engine import calculate_preset
from models.domain import Tool, Material, Operation

class TestCalculationEngine:
    """Test core calculation logic."""

    def test_face_rough_aluminium_basic(self):
        """Test basic FACE_ROUGH calculation for aluminium."""
        tool = Tool(
            id="T1",
            DC=12,
            LCF=30,
            NOF=4,
            tool_type="END_MILL"
        )

        material = Material.ALUMINIUM
        operation = Operation.FACE_ROUGH

        result = calculate_preset(
            tool=tool,
            material=material,
            operation=operation,
            coating="NONE",
            surface_quality="STANDARD",
            coolant="FLOOD"
        )

        # Assertions
        assert result.vc > 0, "vc must be positive"
        assert result.n > 0, "n must be positive"
        assert result.fz > 0, "fz must be positive"
        assert result.vf > 0, "vf must be positive"
        assert result.ae > 0, "ae must be positive"
        assert result.ap > 0, "ap must be positive"

        # Aluminium typical ranges
        assert 200 <= result.vc <= 600, f"vc={result.vc} outside aluminium range"
        assert 0.05 <= result.fz <= 0.20, f"fz={result.fz} outside typical range"

    def test_coating_factor_application(self):
        """Test coating factors are applied correctly."""
        tool = Tool(id="T1", DC=12, LCF=30, NOF=4)

        # Uncoated
        result_uncoated = calculate_preset(
            tool=tool,
            material=Material.STEEL_MILD,
            operation=Operation.FACE_FINISH,
            coating="NONE"
        )

        # TiAlN coated (+60%)
        result_coated = calculate_preset(
            tool=tool,
            material=Material.STEEL_MILD,
            operation=Operation.FACE_FINISH,
            coating="TIALN"
        )

        # vc should be ~60% higher with TiAlN
        expected_vc_coated = result_uncoated.vc * 1.6
        assert abs(result_coated.vc - expected_vc_coated) < 5, \
            f"Coating factor not applied correctly: {result_coated.vc} vs {expected_vc_coated}"

    def test_surface_quality_adjustments(self):
        """Test surface quality factors."""
        tool = Tool(id="T1", DC=12, LCF=30, NOF=4)

        # Standard
        result_standard = calculate_preset(
            tool=tool,
            material=Material.ALUMINIUM,
            operation=Operation.FACE_FINISH,
            surface_quality="STANDARD"
        )

        # Finishing (-20% ae/ap)
        result_finishing = calculate_preset(
            tool=tool,
            material=Material.ALUMINIUM,
            operation=Operation.FACE_FINISH,
            surface_quality="FINISHING"
        )

        # ae and ap should be reduced
        assert result_finishing.ae < result_standard.ae, \
            "Finishing should reduce ae"
        assert result_finishing.ap < result_standard.ap, \
            "Finishing should reduce ap"

    def test_ap_reference_logic(self):
        """Test ap reference selection (DC vs LCF)."""
        from core.operations import get_ap_reference

        # Short tool (L/D < 1.0)
        tool_short = Tool(id="T1", DC=30, LCF=8, NOF=3)  # L/D = 0.27
        ref = get_ap_reference(Operation.FACE_FINISH, tool_short)
        assert ref == "DC", "FACE operations should always use DC"

        ref = get_ap_reference(Operation.SLOT_ROUGH, tool_short)
        assert ref == "DC", "Short tools should use DC"

        # Long tool (L/D >= 1.0)
        tool_long = Tool(id="T2", DC=12, LCF=30, NOF=4)  # L/D = 2.5
        ref = get_ap_reference(Operation.SLOT_ROUGH, tool_long)
        assert ref == "LCF", "Long tools should use LCF for slots"

    def test_validation_8_checks(self):
        """Test all 8 validation checks."""
        from services.validation import ValidationService

        validator = ValidationService()

        tool = Tool(id="T1", DC=12, LCF=30, NOF=4)
        result = calculate_preset(
            tool=tool,
            material=Material.STEEL_STAINLESS,
            operation=Operation.FACE_ROUGH
        )

        validation = validator.validate_result(result)

        assert validation.checks_performed == 8, "Should perform all 8 checks"
        assert validation.status in ["SAFE", "WARNING", "UNSAFE"]

    def test_expert_mode_global_adjustment(self):
        """Test expert mode global adjustment slider."""
        from services.expert_mode import ExpertModeService

        expert = ExpertModeService()

        tool = Tool(id="T1", DC=12, LCF=30, NOF=4)
        base_result = calculate_preset(
            tool=tool,
            material=Material.ALUMINIUM,
            operation=Operation.FACE_FINISH
        )

        # Apply +15% global adjustment
        adjusted_result = expert.apply_global_adjustment(
            base_result,
            adjustment=15
        )

        # All parameters should be ~15% higher
        assert abs(adjusted_result.vc - base_result.vc * 1.15) < 1
        assert abs(adjusted_result.vf - base_result.vf * 1.15) < 10
        assert abs(adjusted_result.ae - base_result.ae * 1.15) < 0.1
        assert abs(adjusted_result.ap - base_result.ap * 1.15) < 0.1

    @pytest.mark.parametrize("material,operation,expected_range", [
        (Material.SOFTWOOD, Operation.FACE_ROUGH, (800, 1200)),
        (Material.ALUMINIUM, Operation.FACE_ROUGH, (200, 400)),
        (Material.STEEL_MILD, Operation.FACE_ROUGH, (100, 180)),
        (Material.STEEL_STAINLESS, Operation.FACE_FINISH, (80, 140)),
    ])
    def test_material_vc_ranges(self, material, operation, expected_range):
        """Test vc values are within expected ranges for materials."""
        tool = Tool(id="T1", DC=12, LCF=30, NOF=4)

        result = calculate_preset(
            tool=tool,
            material=material,
            operation=operation
        )

        min_vc, max_vc = expected_range
        assert min_vc <= result.vc <= max_vc, \
            f"{material.value} vc={result.vc} outside range [{min_vc}, {max_vc}]"


# tests/test_tool_parser.py
class TestToolParser:
    """Test .tools file parsing."""

    def test_parse_valid_tools_file(self, sample_tools_file):
        """Test parsing valid .tools file."""
        from services.tool_parser import ToolParserService

        parser = ToolParserService()
        result = parser.parse_tools_file(sample_tools_file)

        assert result.success == True
        assert len(result.tools) > 0
        assert all(tool.DC > 0 for tool in result.tools)
        assert all(tool.LCF > 0 for tool in result.tools)

    def test_smart_preset_detection(self, tools_file_with_presets):
        """Test smart preset detection from Fusion names."""
        from services.tool_parser import ToolParserService

        parser = ToolParserService()
        result = parser.parse_tools_file(tools_file_with_presets)

        tool_with_presets = next(
            t for t in result.tools if len(t.detected_presets) > 0
        )

        # Should detect materials and operations
        assert len(tool_with_presets.detected_materials) > 0
        assert len(tool_with_presets.detected_operations) > 0

    def test_ld_ratio_calculation(self):
        """Test L/D ratio calculation."""
        from services.tool_parser import ToolParserService

        parser = ToolParserService()

        tool_data = {
            "DC": 12.0,
            "LCF": 30.0,
            "NOF": 4
        }

        ld_ratio = parser.calculate_ld_ratio(tool_data)
        assert abs(ld_ratio - 2.5) < 0.01


# tests/test_export.py
class TestExport:
    """Test export functionality."""

    def test_fusion_export_structure(self, calculation_results):
        """Test Fusion .tools export structure."""
        from services.export import ExportService

        exporter = ExportService()
        tools_file = exporter.create_fusion_export(calculation_results)

        # Should be valid ZIP
        import zipfile
        with zipfile.ZipFile(io.BytesIO(tools_file)) as zf:
            assert 'tools.json' in zf.namelist()

            # Parse tools.json
            tools_json = json.loads(zf.read('tools.json'))
            assert 'data' in tools_json
            assert 'tools' in tools_json['data']

    def test_fusion_preset_expressions(self, single_preset_result):
        """Test preset has all 13 expressions."""
        from services.export import ExportService

        exporter = ExportService()
        preset_json = exporter.create_preset_json(single_preset_result)

        assert 'expressions' in preset_json
        expressions = preset_json['expressions']

        # Must have exactly 13 expressions
        assert len(expressions) == 13

        # Check required expression names
        required = [
            'tool_spindleSpeed', 'tool_feedCutting', 'tool_feedPlunge',
            'tool_rampSpindleSpeed', 'tool_rampFeedCutting',
            'tool_surfaceSpeed', 'tool_stepover', 'tool_stepdown',
            # ... etc
        ]
        for exp in required:
            assert exp in [e['name'] for e in expressions]
```

---

#### 7.4.2 Integration Tests

**API Integration Tests (pytest + httpx):**

```python
# tests/test_api_integration.py
import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
class TestCalculationAPI:
    """Test calculation API endpoints."""

    async def test_calculate_single_preset(self, client: AsyncClient):
        """Test /api/v1/calculate with single preset."""
        request_data = {
            "tool_ids": ["T1"],
            "materials": ["Aluminium"],
            "operations": ["FACE_FINISH"],
            "coating": "TIN",
            "surface_quality": "STANDARD",
            "coolant": "FLOOD"
        }

        response = await client.post("/api/v1/calculate", json=request_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] == True
        assert data["total_presets"] == 1
        assert len(data["results"]) == 1

        result = data["results"][0]
        assert "vc" in result
        assert "n" in result
        assert "fz" in result
        assert "vf" in result
        assert "ae" in result
        assert "ap" in result

    async def test_calculate_batch(self, client: AsyncClient):
        """Test batch calculation with multiple presets."""
        request_data = {
            "tool_ids": ["T1", "T2"],
            "materials": ["Aluminium", "Steel_Mild"],
            "operations": ["FACE_ROUGH", "FACE_FINISH"],
            "coating": "TIALN",
            "surface_quality": "STANDARD",
            "coolant": "FLOOD"
        }

        # 2 tools × 2 materials × 2 operations = 8 presets
        response = await client.post("/api/v1/calculate", json=request_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["total_presets"] == 8
        assert len(data["results"]) == 8

    async def test_async_calculation(self, client: AsyncClient):
        """Test async calculation endpoint."""
        request_data = {
            "tool_ids": ["T1", "T2", "T3"],
            "materials": ["Aluminium", "Steel_Mild", "Brass"],
            "operations": ["FACE_ROUGH", "FACE_FINISH", "SLOT_ROUGH", "SLOT_FINISH"],
            "coating": "TIALN",
            "surface_quality": "STANDARD",
            "coolant": "FLOOD"
        }

        # 3 × 3 × 4 = 36 presets (should trigger async)
        response = await client.post("/api/v1/calculate/async", json=request_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "task_id" in data
        assert data["status"] == "PENDING"

        # Poll status
        task_id = data["task_id"]
        for _ in range(10):  # Max 10 attempts
            await asyncio.sleep(1)
            status_response = await client.get(f"/api/v1/calculate/status/{task_id}")
            status_data = status_response.json()

            if status_data["state"] == "SUCCESS":
                assert status_data["progress"] == 100
                assert "result" in status_data
                break

    async def test_expert_mode_calculation(self, client: AsyncClient):
        """Test expert mode endpoint."""
        request_data = {
            "tool_id": "T1",
            "material": "Steel_Mild",
            "operation": "FACE_FINISH",
            "coating": "TIALN",
            "overrides": {
                "global_adjustment": 15,
                "ap_reference": "AUTO",
                "individual_overrides": {
                    "ae": 1.10,
                    "ap": 1.00
                }
            }
        }

        response = await client.post("/api/v1/expert/calculate", json=request_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] == True
        assert "result" in data
        assert "validation" in data

    async def test_tools_file_upload(self, client: AsyncClient, sample_tools_file):
        """Test .tools file upload and parsing."""
        files = {"file": ("test.tools", sample_tools_file, "application/zip")}

        response = await client.post("/api/v1/tools/parse", files=files)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] == True
        assert len(data["tools"]) > 0

        tool = data["tools"][0]
        assert "id" in tool
        assert "DC" in tool
        assert "LCF" in tool
        assert "NOF" in tool

    async def test_export_fusion(self, client: AsyncClient, calculation_results):
        """Test Fusion .tools export."""
        export_request = {
            "results": calculation_results,
            "batch_id": "test_batch_123"
        }

        response = await client.post("/api/v1/export/fusion", json=export_request)

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/zip"

        # Verify it's a valid ZIP
        import zipfile
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            assert 'tools.json' in zf.namelist()

    async def test_validation_errors(self, client: AsyncClient):
        """Test API validation errors."""
        # Missing required field
        invalid_request = {
            "tool_ids": ["T1"],
            # Missing materials
            "operations": ["FACE_FINISH"]
        }

        response = await client.post("/api/v1/calculate", json=invalid_request)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data

    async def test_rate_limiting(self, client: AsyncClient):
        """Test API rate limiting."""
        # Make multiple rapid requests
        for _ in range(100):
            response = await client.get("/health")
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                break
        # Should hit rate limit eventually
```

---

#### 7.4.3 E2E Tests (Playwright)

**End-to-End Tests:**

```typescript
// tests/e2e/workflow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Complete 6-Screen Workflow', () => {
  test('should complete full workflow from import to export', async ({ page }) => {
    // Screen 1: Import .tools file
    await page.goto('/');
    await page.click('text=Import Tools');

    // Upload file
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles('tests/fixtures/sample.tools');

    // Wait for parsing
    await expect(page.locator('text=✓ 13 tools imported')).toBeVisible();
    await page.click('text=Continue to Tool Selection');

    // Screen 2: Tool Selection
    await expect(page).toHaveURL(/\/tools/);

    // Select tools
    await page.click('text=Select All');
    await expect(page.locator('text=13 of 13 tools selected')).toBeVisible();
    await page.click('text=Continue with 13 tools');

    // Screen 3: Material Selection
    await expect(page).toHaveURL(/\/materials/);

    // Select materials for first tool
    await page.click('label:has-text("Aluminium")');
    await page.click('label:has-text("Steel Mild")');

    // Apply to all tools
    await page.click('text=Apply to all tools');
    await page.click('text=Continue: 26 materials total');

    // Screen 4: Operation Matrix
    await expect(page).toHaveURL(/\/operations/);

    // Click FACE group header (select all FACE operations)
    await page.click('[data-group="FACE"]');

    // Verify summary
    await expect(page.locator('text=26 presets')).toBeVisible();
    await page.click('text=Calculate 26 Presets');

    // Screen 5: Calculation Progress
    await expect(page).toHaveURL(/\/calculating/);
    await expect(page.locator('text=Calculating...')).toBeVisible();

    // Wait for completion (max 30s)
    await expect(page.locator('text=Calculation completed')).toBeVisible({
      timeout: 30000
    });

    // Auto-redirect to results
    await expect(page).toHaveURL(/\/results/);

    // Screen 6: Results
    // Verify table
    await expect(page.locator('table')).toBeVisible();
    await expect(page.locator('tbody tr')).toHaveCount(26);

    // Verify columns
    await expect(page.locator('th:has-text("vc")')).toBeVisible();
    await expect(page.locator('th:has-text("n")')).toBeVisible();
    await expect(page.locator('th:has-text("fz")')).toBeVisible();

    // Filter results
    await page.click('button:has-text("SAFE")');
    const safeRows = page.locator('tbody tr:has([data-status="SAFE"])');
    expect(await safeRows.count()).toBeGreaterThan(0);

    // Screen 7: Export
    await page.click('text=Export to Fusion 360');

    // Wait for download
    const downloadPromise = page.waitForEvent('download');
    await page.click('text=Download .tools file');
    const download = await downloadPromise;

    expect(download.suggestedFilename()).toContain('.tools');
  });

  test('should handle expert mode adjustments', async ({ page }) => {
    // Navigate to operations screen
    await page.goto('/operations');

    // Enable expert mode
    await page.click('text=Show Expert Mode');

    // Adjust global slider
    const slider = page.locator('[data-testid="global-adjustment-slider"]');
    await slider.fill('15');

    // Verify effect display
    await expect(page.locator('text=vc: ×1.15')).toBeVisible();

    // Apply overrides
    await page.click('text=Apply Overrides');

    // Continue to calculation
    await page.click('text=Calculate');

    // Verify expert mode indicator in results
    await expect(page).toHaveURL(/\/results/);
    await expect(page.locator('text=⚙️ Expert Mode Active: +15%')).toBeVisible();
  });

  test('should show mathematical workbook', async ({ page }) => {
    // Navigate to results
    await page.goto('/results/test-batch-123');

    // Click workbook button
    await page.click('button:has-text("📊 Workbook")');

    // Verify modal
    await expect(page.locator('text=Mathematical Workbook')).toBeVisible();
    await expect(page.locator('text=PHASE 1: Material Base Values')).toBeVisible();
    await expect(page.locator('text=PHASE 2: Coating Factor')).toBeVisible();

    // Navigate phases
    await page.click('text=Continue to Phase 4');
    await expect(page.locator('text=PHASE 4:')).toBeVisible();
  });
});


test.describe('Error Handling', () => {
  test('should handle invalid .tools file', async ({ page }) => {
    await page.goto('/');

    // Upload invalid file
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles('tests/fixtures/invalid.txt');

    // Verify error message
    await expect(page.locator('text=Invalid file format')).toBeVisible();
    await expect(page.locator('text=Expected .tools file')).toBeVisible();
  });

  test('should handle calculation errors', async ({ page }) => {
    // ... trigger calculation error scenario ...

    await expect(page.locator('text=Calculation failed')).toBeVisible();
    await expect(page.locator('button:has-text("Retry")')).toBeVisible();
  });
});
```

---

#### 7.4.4 Performance Tests

**Load Testing (locust):**

```python
# tests/performance/locustfile.py
from locust import HttpUser, task, between

class CNCCalculatorUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def calculate_single_preset(self):
        """Most common operation - single preset calculation."""
        self.client.post("/api/v1/calculate", json={
            "tool_ids": ["T1"],
            "materials": ["Aluminium"],
            "operations": ["FACE_FINISH"],
            "coating": "TIN",
            "surface_quality": "STANDARD",
            "coolant": "FLOOD"
        })

    @task(2)
    def calculate_batch(self):
        """Batch calculation - 10 presets."""
        self.client.post("/api/v1/calculate", json={
            "tool_ids": ["T1", "T2"],
            "materials": ["Aluminium", "Steel_Mild"],
            "operations": ["FACE_ROUGH", "FACE_FINISH", "SLOT_FINISH"],
            "coating": "TIALN"
        })

    @task(1)
    def parse_tools_file(self):
        """File upload and parsing."""
        with open("tests/fixtures/sample.tools", "rb") as f:
            self.client.post("/api/v1/tools/parse", files={"file": f})

    def on_start(self):
        """Called when user starts."""
        # Health check
        self.client.get("/health")
```

**Run:** `locust -f tests/performance/locustfile.py --host=http://localhost:8000`

**Performance Targets:**
- Single preset calculation: < 100ms
- Batch (10 presets): < 500ms
- Batch (100 presets): < 2s
- Tool parsing: < 200ms
- API p95 latency: < 300ms

---

### 7.5 Deployment Strategy

#### 7.5.1 Docker Configuration

**Dockerfile (Backend):**

```dockerfile
# Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile (Frontend):**

```dockerfile
# Dockerfile.frontend
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source
COPY . .

# Build
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/cnc_calculator
      - REDIS_HOST=redis
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
      - uploads:/app/uploads
    networks:
      - cnc-network

  # Celery Worker
  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A workers.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/cnc_calculator
      - REDIS_HOST=redis
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
    networks:
      - cnc-network

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - cnc-network

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=cnc_calculator
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - cnc-network

  # Redis (Celery broker)
  redis:
    image: redis:7-alpine
    networks:
      - cnc-network

volumes:
  postgres-data:
  uploads:

networks:
  cnc-network:
    driver: bridge
```

---

#### 7.5.2 CI/CD Pipeline (GitHub Actions)

**.github/workflows/ci.yml:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Backend tests
  backend-test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        working-directory: ./backend
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio

      - name: Run tests
        working-directory: ./backend
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          REDIS_HOST: localhost
        run: |
          pytest --cov=. --cov-report=xml --cov-report=term

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  # Frontend tests
  frontend-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Run linter
        working-directory: ./frontend
        run: npm run lint

      - name: Run tests
        working-directory: ./frontend
        run: npm test -- --coverage

      - name: Build
        working-directory: ./frontend
        run: npm run build

  # E2E tests
  e2e-test:
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-test]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Start services
        run: docker-compose up -d

      - name: Wait for services
        run: |
          timeout 60 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done'
          timeout 60 bash -c 'until curl -f http://localhost:3000; do sleep 2; done'

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/

  # Build and push Docker images
  build-deploy:
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-test, e2e-test]
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push backend
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/cnc-calculator-backend:latest

      - name: Build and push frontend
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/cnc-calculator-frontend:latest

  # Deploy to production
  deploy:
    runs-on: ubuntu-latest
    needs: build-deploy
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            cd /opt/cnc-calculator
            docker-compose pull
            docker-compose up -d
            docker-compose exec -T backend python manage.py migrate
```

---

## TEIL 8: ANHÄNGE

### Glossar

**CNC:** Computer Numerical Control
**vc:** Cutting Speed [m/min]
**n:** Spindle Speed [RPM]
**fz:** Feed per Tooth [mm]
**vf:** Feed Rate [mm/min]
**ae:** Radial Width of Cut [mm]
**ap:** Axial Depth of Cut [mm]
**DC:** Cutting Diameter [mm]
**LCF:** Length of Cut [mm]
**NOF:** Number of Flutes
**L/D:** Length-to-Diameter Ratio
**MRR:** Material Removal Rate [cm³/min]
**kc:** Specific Cutting Force [N/mm²]

### Change Request Template

```markdown
# Change Request: [Title]

**Date:** YYYY-MM-DD
**Author:** [Name]
**Type:** Feature / Bugfix / Enhancement
**Priority:** Critical / High / Medium / Low

## Description
[What needs to change and why?]

## Current Behavior
[How does it work now?]

## Proposed Behavior
[How should it work?]

## Impact Analysis
- Affected Modules: [...]
- Breaking Changes: Yes/No
- Performance Impact: [...]

## Implementation Plan
1. Step 1
2. Step 2
3. ...

## Testing Requirements
- Unit Tests: [...]
- Integration Tests: [...]
- Manual Testing: [...]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

---

### 8.1 Pydantic Schema Examples

**Complete schema definitions for type safety:**

```python
# models/schemas.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class ToolType(str, Enum):
    END_MILL = "end_mill"
    BALL_NOSE = "ball_nose"
    FACE_MILL = "face_mill"
    CHAMFER = "chamfer"
    DRILL = "drill"


class MaterialType(str, Enum):
    SOFTWOOD = "Softwood"
    HARDWOOD = "Hardwood"
    ALUMINIUM = "Aluminium"
    BRASS = "Brass"
    ACRYLIC = "Acrylic"
    STEEL_MILD = "Steel_Mild"
    STEEL_STAINLESS = "Steel_Stainless"


class OperationType(str, Enum):
    FACE_ROUGH = "FACE_ROUGH"
    FACE_FINISH = "FACE_FINISH"
    SLOT_ROUGH = "SLOT_ROUGH"
    SLOT_FINISH = "SLOT_FINISH"
    SLOT_FULL = "SLOT_FULL"
    SLOT_TROCHOIDAL = "SLOT_TROCHOIDAL"
    GEOMETRY_CHAMFER = "GEOMETRY_CHAMFER"
    GEOMETRY_RADIUS = "GEOMETRY_RADIUS"
    GEOMETRY_BALL = "GEOMETRY_BALL"
    SPECIAL_ADAPTIVE = "SPECIAL_ADAPTIVE"
    SPECIAL_PLUNGE = "SPECIAL_PLUNGE"
    SPECIAL_DRILL = "SPECIAL_DRILL"


class CoatingType(str, Enum):
    NONE = "NONE"
    TIN = "TIN"
    TIALN = "TIALN"
    ALTIN = "ALTIN"
    DIAMOND = "DIAMOND"
    CARBIDE = "CARBIDE"


class SurfaceQuality(str, Enum):
    ROUGHING = "ROUGHING"
    STANDARD = "STANDARD"
    FINISHING = "FINISHING"
    HIGH_FINISH = "HIGH_FINISH"


class CoolantType(str, Enum):
    FLOOD = "FLOOD"
    DRY = "DRY"
    MQL = "MQL"


class Geometry(BaseModel):
    DC: float = Field(..., gt=0, description="Cutting diameter in mm")
    LCF: float = Field(..., gt=0, description="Length of cut in mm")
    NOF: int = Field(..., ge=1, le=12, description="Number of flutes")
    SHAFT_DIAMETER: Optional[float] = Field(None, gt=0)
    OVERALL_LENGTH: Optional[float] = Field(None, gt=0)

    @property
    def ld_ratio(self) -> float:
        """Calculate L/D ratio."""
        return self.LCF / self.DC


class Tool(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    tool_type: ToolType
    geometry: Geometry
    vendor: Optional[str] = None
    part_number: Optional[str] = None


class PresetDetection(BaseModel):
    has_presets: bool
    detected_materials: List[MaterialType] = []
    detected_operations: List[OperationType] = []
    reference_values: Dict[str, Any] = {}


class ToolParseResponse(BaseModel):
    success: bool
    tools: List[Tool]
    total_tools: int
    detections: Dict[str, PresetDetection] = {}
    errors: List[str] = []


class CalculationRequest(BaseModel):
    tool_ids: List[str] = Field(..., min_items=1)
    materials: List[MaterialType] = Field(..., min_items=1)
    operations: List[OperationType] = Field(..., min_items=1)
    coating: CoatingType = CoatingType.NONE
    surface_quality: SurfaceQuality = SurfaceQuality.STANDARD
    coolant: CoolantType = CoolantType.FLOOD

    @validator('tool_ids')
    def validate_tool_ids(cls, v):
        if len(v) > 50:
            raise ValueError('Maximum 50 tools per batch')
        return v

    @property
    def total_presets(self) -> int:
        return len(self.tool_ids) * len(self.materials) * len(self.operations)


class ValidationStatus(str, Enum):
    SAFE = "SAFE"
    WARNING = "WARNING"
    UNSAFE = "UNSAFE"


class ValidationCheck(BaseModel):
    check_id: str
    name: str
    status: ValidationStatus
    message: str
    value: Optional[float] = None
    threshold: Optional[float] = None


class PresetResult(BaseModel):
    preset_id: str
    preset_name: str
    tool_id: str
    material: MaterialType
    operation: OperationType

    # Calculated parameters
    vc: float = Field(..., description="Cutting speed in m/min")
    n: float = Field(..., description="Spindle speed in RPM")
    fz: float = Field(..., description="Chip load in mm/tooth")
    vf: float = Field(..., description="Feed rate in mm/min")
    ae: float = Field(..., description="Radial engagement in mm")
    ap: float = Field(..., description="Axial depth in mm")
    mrr: float = Field(..., description="Material removal rate in cm³/min")

    # Percentages
    ae_percent: float = Field(..., description="ae as % of reference")
    ap_percent: float = Field(..., description="ap as % of reference")

    # Validation
    validation_status: ValidationStatus
    validation_checks: List[ValidationCheck] = []

    # Metadata
    ap_reference: str = Field(..., description="DC or LCF")
    coating_factor: float = 1.0
    surface_quality_factor: Dict[str, float] = {}
    expert_mode_applied: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)


class CalculationResponse(BaseModel):
    success: bool
    total_presets: int
    results: List[PresetResult]
    warnings: List[str] = []
    calculation_time_ms: Optional[float] = None


class ExpertModeOverrides(BaseModel):
    global_adjustment: Optional[int] = Field(None, ge=-50, le=50)
    ap_reference: Optional[str] = Field(None, pattern="^(AUTO|DC|LCF)$")
    individual_overrides: Optional[Dict[str, float]] = None

    @validator('individual_overrides')
    def validate_individual_overrides(cls, v):
        if v is not None:
            allowed_keys = {'ae', 'ap', 'fz', 'vc'}
            for key in v.keys():
                if key not in allowed_keys:
                    raise ValueError(f'Invalid override key: {key}')
                if not (0.5 <= v[key] <= 2.0):
                    raise ValueError(f'Override value for {key} must be between 0.5 and 2.0')
        return v


class ExpertModeRequest(BaseModel):
    tool_id: str
    material: MaterialType
    operation: OperationType
    coating: CoatingType = CoatingType.NONE
    overrides: ExpertModeOverrides


class ExpertModeValidation(BaseModel):
    valid: bool
    warnings: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0


class ExpertModeResponse(BaseModel):
    success: bool
    result: PresetResult
    validation: ExpertModeValidation


class AsyncTaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


class TaskStatus(BaseModel):
    task_id: str
    state: str
    status: str
    progress: int = 0
    current_preset: Optional[str] = None
    total_presets: Optional[int] = None
    result: Optional[Any] = None
    error: Optional[str] = None


class ExportFormat(str, Enum):
    FUSION = "fusion"
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"


class ExportRequest(BaseModel):
    results: List[PresetResult]
    format: ExportFormat = ExportFormat.FUSION
    batch_id: str
    include_metadata: bool = True
```

---

### 8.2 Database Schema (PostgreSQL)

**Complete database schema for data persistence:**

```sql
-- migrations/001_initial_schema.sql

-- Tools table
CREATE TABLE tools (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    tool_type VARCHAR(50) NOT NULL,
    vendor VARCHAR(100),
    part_number VARCHAR(100),

    -- Geometry
    dc DECIMAL(10, 2) NOT NULL CHECK (dc > 0),
    lcf DECIMAL(10, 2) NOT NULL CHECK (lcf > 0),
    nof INTEGER NOT NULL CHECK (nof >= 1 AND nof <= 12),
    shaft_diameter DECIMAL(10, 2),
    overall_length DECIMAL(10, 2),

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_ld_ratio CHECK (lcf / dc < 10)
);

CREATE INDEX idx_tools_type ON tools(tool_type);
CREATE INDEX idx_tools_created_at ON tools(created_at);


-- Calculation jobs table
CREATE TABLE calculation_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id VARCHAR(100) UNIQUE NOT NULL,

    -- Request parameters
    tool_ids TEXT[] NOT NULL,
    materials TEXT[] NOT NULL,
    operations TEXT[] NOT NULL,
    coating VARCHAR(50) NOT NULL DEFAULT 'NONE',
    surface_quality VARCHAR(50) NOT NULL DEFAULT 'STANDARD',
    coolant VARCHAR(50) NOT NULL DEFAULT 'FLOOD',

    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    total_presets INTEGER NOT NULL,
    completed_presets INTEGER DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    -- Metadata
    error_message TEXT,
    calculation_time_ms INTEGER,

    CHECK (status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED'))
);

CREATE INDEX idx_jobs_batch_id ON calculation_jobs(batch_id);
CREATE INDEX idx_jobs_status ON calculation_jobs(status);
CREATE INDEX idx_jobs_created_at ON calculation_jobs(created_at);


-- Preset results table
CREATE TABLE preset_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES calculation_jobs(id) ON DELETE CASCADE,

    preset_id VARCHAR(200) UNIQUE NOT NULL,
    preset_name VARCHAR(200) NOT NULL,

    -- References
    tool_id VARCHAR(50) NOT NULL REFERENCES tools(id),
    material VARCHAR(50) NOT NULL,
    operation VARCHAR(50) NOT NULL,

    -- Calculated parameters
    vc DECIMAL(10, 2) NOT NULL CHECK (vc > 0),
    n DECIMAL(10, 2) NOT NULL CHECK (n > 0),
    fz DECIMAL(10, 4) NOT NULL CHECK (fz > 0),
    vf DECIMAL(10, 2) NOT NULL CHECK (vf > 0),
    ae DECIMAL(10, 2) NOT NULL CHECK (ae > 0),
    ap DECIMAL(10, 2) NOT NULL CHECK (ap > 0),
    mrr DECIMAL(10, 2) NOT NULL,

    -- Percentages
    ae_percent DECIMAL(5, 1) NOT NULL,
    ap_percent DECIMAL(5, 1) NOT NULL,

    -- Validation
    validation_status VARCHAR(50) NOT NULL,
    validation_checks JSONB,

    -- Metadata
    ap_reference VARCHAR(10) NOT NULL CHECK (ap_reference IN ('DC', 'LCF')),
    coating_factor DECIMAL(5, 2) NOT NULL DEFAULT 1.0,
    surface_quality_factor JSONB,
    expert_mode_applied BOOLEAN DEFAULT FALSE,
    expert_mode_overrides JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (validation_status IN ('SAFE', 'WARNING', 'UNSAFE'))
);

CREATE INDEX idx_results_job_id ON preset_results(job_id);
CREATE INDEX idx_results_preset_id ON preset_results(preset_id);
CREATE INDEX idx_results_tool_id ON preset_results(tool_id);
CREATE INDEX idx_results_validation_status ON preset_results(validation_status);
CREATE INDEX idx_results_created_at ON preset_results(created_at);


-- Audit log table
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,

    -- Event info
    event_type VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id VARCHAR(200),

    -- User/System info
    user_id VARCHAR(100),
    ip_address VARCHAR(50),
    user_agent TEXT,

    -- Changes
    old_value JSONB,
    new_value JSONB,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_data JSONB
);

CREATE INDEX idx_audit_event_type ON audit_log(event_type);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_created_at ON audit_log(created_at);


-- User preferences table (future feature)
CREATE TABLE user_preferences (
    user_id VARCHAR(100) PRIMARY KEY,

    -- UI preferences
    theme VARCHAR(50) DEFAULT 'dark',
    contrast_mode VARCHAR(50) DEFAULT 'balanced',

    -- Default settings
    default_coating VARCHAR(50) DEFAULT 'NONE',
    default_surface_quality VARCHAR(50) DEFAULT 'STANDARD',
    default_coolant VARCHAR(50) DEFAULT 'FLOOD',

    -- Expert mode defaults
    expert_mode_enabled BOOLEAN DEFAULT FALSE,
    expert_global_adjustment INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    preferences JSONB
);


-- Views for reporting

CREATE VIEW calculation_stats AS
SELECT
    DATE(created_at) as date,
    COUNT(*) as total_jobs,
    SUM(total_presets) as total_presets_calculated,
    AVG(calculation_time_ms) as avg_calculation_time_ms,
    COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as successful_jobs,
    COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as failed_jobs
FROM calculation_jobs
GROUP BY DATE(created_at)
ORDER BY date DESC;


CREATE VIEW tool_usage_stats AS
SELECT
    t.id as tool_id,
    t.name as tool_name,
    t.tool_type,
    COUNT(DISTINCT pr.job_id) as times_used,
    COUNT(pr.id) as total_presets,
    AVG(pr.vc) as avg_vc,
    AVG(pr.n) as avg_n,
    MAX(pr.created_at) as last_used
FROM tools t
LEFT JOIN preset_results pr ON t.id = pr.tool_id
GROUP BY t.id, t.name, t.tool_type
ORDER BY times_used DESC;


CREATE VIEW validation_summary AS
SELECT
    validation_status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM preset_results
GROUP BY validation_status
ORDER BY count DESC;
```

---

### 8.3 Monitoring and Observability

**Prometheus metrics configuration:**

```python
# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from functools import wraps
import time

# Metrics definitions
calculation_requests_total = Counter(
    'cnc_calculator_calculation_requests_total',
    'Total number of calculation requests',
    ['status', 'async']
)

calculation_duration_seconds = Histogram(
    'cnc_calculator_calculation_duration_seconds',
    'Time spent calculating presets',
    ['preset_count_bucket'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

active_calculations = Gauge(
    'cnc_calculator_active_calculations',
    'Number of currently active calculations'
)

preset_calculations_total = Counter(
    'cnc_calculator_preset_calculations_total',
    'Total number of presets calculated',
    ['material', 'operation', 'validation_status']
)

api_request_duration_seconds = Histogram(
    'cnc_calculator_api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint', 'status']
)

file_upload_size_bytes = Histogram(
    'cnc_calculator_file_upload_size_bytes',
    'Size of uploaded .tools files',
    buckets=[1024, 10240, 102400, 1024000, 10240000]  # 1KB to 10MB
)

celery_task_duration_seconds = Histogram(
    'cnc_calculator_celery_task_duration_seconds',
    'Celery task execution time',
    ['task_name', 'status']
)

database_query_duration_seconds = Histogram(
    'cnc_calculator_database_query_duration_seconds',
    'Database query execution time',
    ['operation']
)


def track_calculation_time(preset_count: int):
    """Decorator to track calculation timing."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Determine bucket
            if preset_count <= 5:
                bucket = "1-5"
            elif preset_count <= 20:
                bucket = "6-20"
            elif preset_count <= 100:
                bucket = "21-100"
            else:
                bucket = "100+"

            start_time = time.time()
            active_calculations.inc()

            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                calculation_duration_seconds.labels(preset_count_bucket=bucket).observe(duration)
                calculation_requests_total.labels(status="success", async=False).inc()
                return result
            except Exception as e:
                calculation_requests_total.labels(status="error", async=False).inc()
                raise
            finally:
                active_calculations.dec()

        return wrapper
    return decorator


# FastAPI endpoint
from fastapi import Response

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
```

**Grafana Dashboard JSON:**

```json
{
  "dashboard": {
    "title": "CNC Calculator Monitoring",
    "panels": [
      {
        "title": "Calculation Requests (Rate)",
        "targets": [
          {
            "expr": "rate(cnc_calculator_calculation_requests_total[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Average Calculation Duration",
        "targets": [
          {
            "expr": "rate(cnc_calculator_calculation_duration_seconds_sum[5m]) / rate(cnc_calculator_calculation_duration_seconds_count[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Active Calculations",
        "targets": [
          {
            "expr": "cnc_calculator_active_calculations"
          }
        ],
        "type": "gauge"
      },
      {
        "title": "Presets by Validation Status",
        "targets": [
          {
            "expr": "sum by (validation_status) (cnc_calculator_preset_calculations_total)"
          }
        ],
        "type": "piechart"
      },
      {
        "title": "API Request p95 Latency",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(cnc_calculator_api_request_duration_seconds_bucket[5m]))"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

---

### 8.4 Security Considerations

**Security best practices:**

```python
# security/middleware.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
import hashlib
import hmac
import time

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/calculate")
@limiter.limit("10/minute")
async def calculate_with_rate_limit(request: Request, calc_request: CalculationRequest):
    # ... implementation ...
    pass


# Input validation and sanitization
from bleach import clean

def sanitize_string(value: str) -> str:
    """Remove potentially dangerous characters."""
    return clean(value, tags=[], strip=True)


# File upload security
ALLOWED_MIME_TYPES = {
    'application/zip',
    'application/x-zip-compressed'
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def validate_file_upload(file: UploadFile) -> bytes:
    """Validate uploaded file."""
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024} MB"
        )

    # Check MIME type
    import magic
    mime_type = magic.from_buffer(contents, mime=True)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {mime_type}"
        )

    # Check if it's actually a ZIP
    import zipfile
    try:
        with zipfile.ZipFile(io.BytesIO(contents)) as zf:
            # Check for zip bombs
            total_size = sum(info.file_size for info in zf.infolist())
            if total_size > MAX_FILE_SIZE * 10:
                raise HTTPException(
                    status_code=400,
                    detail="Suspicious file: compressed size exceeds limits"
                )
    except zipfile.BadZipFile:
        raise HTTPException(
            status_code=400,
            detail="Invalid ZIP file"
        )

    return contents


# API authentication (future feature)
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    token = credentials.credentials
    try:
        # Verify JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
```

---

# DOKUMENT ENDE

**Total Seiten:** ~150 Seiten (komprimiert)
**Total Zeilen:** ~3500 Zeilen
**Status:** ✅ VOLLSTÄNDIG - Bereit für Implementierung

---

## NÄCHSTE SCHRITTE: OPERATIONALISIERUNG

→ **Siehe separates Dokument:** `OPERATIONALIZATION_STRATEGY.md`

**Fragen zu klären:**
1. Einzelner Claude Agent vs. Multi-Agent-Orchestration?
2. Kontext-Management-Strategie?
3. Greenfield vs. Prototyp-Migration?
4. Team-Setup (UI/Frontend/Backend)?

**Empfehlung:** Multi-Agent mit Governance (Details im Operationalisierungs-Dokument)

---

**Version:** 4.0 Final Consolidated
**Datum:** 2025-11-10
**Autoren:** Volker + Claude + Prof. Dr.-Ing.
**Status:** ✅ PRODUCTION READY - Bereit für Operationalisierungs-Planung

