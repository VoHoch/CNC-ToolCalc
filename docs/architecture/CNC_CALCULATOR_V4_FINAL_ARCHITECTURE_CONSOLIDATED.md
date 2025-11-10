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

## TEIL 3: BACKEND-ARCHITEKTUR (Zusammenfassung)

### 3.1 System-Architektur

**Pattern:** API-First + Clean Architecture
- **Frontend** (React) → REST API → **Backend** (FastAPI) → **V2.0 Engine** (NO-TOUCH)
- **Async Processing:** Celery + Redis für große Berechnungen
- **Database:** SQLite (Dev) / PostgreSQL (Prod)

### 3.2 REST API Endpoints

```
POST   /api/v1/tools/parse              # Parse .tools file
POST   /api/v1/calculate                # Calculate presets
POST   /api/v1/calculate/async          # Async calculation
POST   /api/v1/export/fusion            # Export to Fusion .tools
POST   /api/v1/expert/calculate         # Expert Mode calculation
```

### 3.3 Key Services

1. **CalculationEngine** - Wrapper um V2.0 (10-Phasen-Workflow)
2. **ExpertModeService** - Global Slider + Individual Overrides
3. **ValidationService** - 8-Checks-System
4. **ExportService** - Fusion Parametric Export

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

### 4.4 State Management

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

