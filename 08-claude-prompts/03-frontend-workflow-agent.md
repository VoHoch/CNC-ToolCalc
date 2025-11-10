# CNC-ToolCalc Frontend/Workflow Agent Prompt

**VERSION:** 1.0
**DATE:** 2025-11-10
**STATUS:** PRODUCTION

---

## MODE: FULL EXECUTION

Build 6-screen workflow autonomously. Integrate with Backend API. Manage state & progressive disclosure.

---

## ROLE & RESPONSIBILITIES

You are the **Frontend/Workflow Agent** – Application Architect and UX Flow Builder.

### Core Responsibilities

1. **6-Screen Workflow Implementation**
   - Screen 1: Tool Selection (DC, length)
   - Screen 2: Material Selection **PER TOOL** (CRITICAL!)
   - Screen 3: Operation Selection (13 operations)
   - Screen 4: Coating + Surface Quality + Coolant
   - Screen 5: Parameter Configuration + Results + Expert Mode
   - Screen 6: Export (Fusion, Underscott)

2. **State Management**
   - Tool Selection Store (which tools picked)
   - Material Store (per-tool material selection)
   - Calculation Store (API results, phase progress)
   - Expert Mode Store (global slider + individual overrides)
   - Export Store (what to export, format)

3. **Backend Integration**
   - API Client (OpenAPI generated from `/docs/contracts/API_CONTRACT.md`)
   - Handle async calculation (show progress phases)
   - Validation error handling
   - Response mapping to UI

4. **Progressive Disclosure**
   - Basic Mode: Show only essential parameters
   - Expert Mode: Global slider (-50 to +50) + parameter overrides
   - Smooth transition between modes

5. **Form Validation**
   - Client-side validation before API call
   - Server-side validation handling
   - Clear error messages
   - Field-level feedback

---

## CONTEXT: WORKFLOW & STATE

### The 6-Screen Flow

**Screen 1: Tool Selection**
```
┌────────────────────────────────────┐
│ Select Tools to Work With          │
├────────────────────────────────────┤
│ [Card: T1 Planfräser Ø30]          │
│         DC: 30mm, LCF: 8mm         │
│         [SELECT] [INFO]            │
│                                    │
│ [Card: T2 Schaftfräser Ø6]         │
│         DC: 6mm, LCF: 15mm         │
│         [SELECT] [INFO]            │
└────────────────────────────────────┘
Next: Material Selection (per Tool)
```

**State:** `selectedToolIds: string[]`

**Screen 2: Material Selection (PER TOOL!)**
```
For Tool T1 (Planfräser Ø30):
┌────────────────────────────────────┐
│ Select Materials                   │
├────────────────────────────────────┤
│ [Card: Softwood (Weichholz)]       │
│         Hardness: 1 (softest)      │
│         [SELECT]                   │
│                                    │
│ [Card: Aluminium 6061/7075]        │
│         Hardness: 3                │
│         [SELECT]                   │
│                                    │
│ [Card: Steel (Stahl)]              │
│         Hardness: 6                │
│         [SELECT]                   │
└────────────────────────────────────┘
[< Back] [Next: Operations >]

Show selected materials for T1 in sidebar:
"T1: Softwood, Aluminium"
```

**State:** `materialsByTool: Record<string, string[]>`

**Screen 3: Operation Selection**
```
┌────────────────────────────────────┐
│ Select Operations (13 total)       │
├────────────────────────────────────┤
│ ▼ FACE (Planfräsen)           [2/2]│
│   [☑] Face Roughing (Schruppen)   │
│   [☑] Face Finishing (Schlichten)  │
│                                    │
│ ► SLOT (Nuten/Taschen)        [0/4]│
│                                    │
│ ▼ GEOMETRY (Konturbearbeitung) [1/3]
│   [☑] 3D Surface                  │
│                                    │
│ ► SPECIAL (Sonderfunktionen)   [0/2]
└────────────────────────────────────┘
```

**State:** `selectedOperations: string[]`

**Screen 4: Coating + Surface Quality**
```
┌────────────────────────────────────┐
│ Tool Coatings & Surface Quality    │
├────────────────────────────────────┤
│ Coating Type:                      │
│  [NONE] [TIN: +40%] [TIALN: +60%]  │
│  [ALTIN: +80%] [DIAMOND: +120%]    │
│  [CARBIDE: +50%]                   │
│                                    │
│ Surface Quality:                   │
│  [ROUGHING] [STANDARD] [FINISHING] │
│  [HIGH_FINISH]                     │
│                                    │
│ Coolant Type:                      │
│  [WET (normal)] [DRY: -30% fz]     │
│  [MQL: -15% fz]                    │
└────────────────────────────────────┘
```

**State:** `coatingType, surfaceQuality, coolantType`

**Screen 5: Results + Parameter Configuration**
```
┌────────────────────────────────────┐
│ Calculation Results                │
│                                    │
│ BASIC MODE:                        │
│ ┌──────────────────────────────┐   │
│ │ Tool T1, Material ALU,       │   │
│ │ Operation FACE_FINISH        │   │
│ │                              │   │
│ │ vc: 168 m/min                │   │
│ │ n: 18000 RPM                 │   │
│ │ fz: 0.05 mm/tooth            │   │
│ │ vf: 2700 mm/min              │   │
│ │                              │   │
│ │ Status: ✓ OK                 │   │
│ └──────────────────────────────┘   │
│                                    │
│ [☐ Enable Expert Mode]             │
└────────────────────────────────────┘
```

**Screen 5 (Expert Mode):**
```
┌────────────────────────────────────┐
│ EXPERT MODE: Global Adjustment     │
├────────────────────────────────────┤
│ Global Slider: -50 to +50          │
│ ◄──────────●──────────► [+15%]     │
│                                    │
│ Individual Parameter Overrides:    │
│ ┌──────────────────────────────┐   │
│ │ ae (Radial Engagement)       │   │
│ │ ◄──────────●──────────► [-5%] │   │
│ │                              │   │
│ │ ap (Axial Depth)             │   │
│ │ ◄──────────────●──────► [+10%]│   │
│ │                              │   │
│ │ fz (Chip Load)               │   │
│ │ ◄──────────●──────────► [0%]  │   │
│ └──────────────────────────────┘   │
│                                    │
│ Calculated Results (updated live): │
│ vc: 182 m/min (was 168)            │
│ n: 19500 RPM (was 18000)           │
│ Power: 0.71 kW (was 0.65)          │
└────────────────────────────────────┘
```

**State:** `expertModeEnabled, globalSlider, parameterOverrides`

**Screen 6: Export**
```
┌────────────────────────────────────┐
│ Export Calculation Results         │
├────────────────────────────────────┤
│ Export Format:                     │
│ [✓] Fusion 360 (.tools ZIP)        │
│ [ ] Underscott CSV                 │
│ [ ] JSON                           │
│ [ ] PDF Report                     │
│                                    │
│ Select Results to Export:          │
│ [☑] T1 + ALU + FACE_FINISH        │
│ [☑] T1 + ALU + SLOT_ROUGH         │
│ [☑] T2 + STEEL + FACE_ROUGH       │
│                                    │
│ [PREVIEW] [EXPORT] [SAVE PRESET]   │
└────────────────────────────────────┘
```

**State:** `exportFormat, selectedResults, presetName`

---

## ARCHITECTURE: STATE MANAGEMENT

### Store 1: Tool Selection Store

```typescript
// src/state/toolStore.ts (using Zustand or Redux)
interface ToolStore {
  // State
  selectedToolIds: string[];
  allTools: Tool[];

  // Actions
  loadTools: (tools: Tool[]) => void;
  selectTool: (toolId: string) => void;
  deselectTool: (toolId: string) => void;
  getSelectedTools: () => Tool[];
}

// Usage:
const {selectedToolIds, selectTool} = useToolStore();
```

### Store 2: Material Selection Store (PER TOOL)

```typescript
// src/state/materialStore.ts
interface MaterialStore {
  // State: materials are per-tool!
  materialsByTool: Record<string, string[]>;  // {T1: ["ALU", "STEEL"], T2: ["ALU"]}
  allMaterials: Material[];

  // Actions
  loadMaterials: (materials: Material[]) => void;
  selectMaterialForTool: (toolId: string, materialId: string) => void;
  deselectMaterialForTool: (toolId: string, materialId: string) => void;
  getMaterialsForTool: (toolId: string) => Material[];
  getAllSelectedMaterials: () => Array<{toolId: string, materialId: string}>;
}

// CRITICAL: Don't use global materialSelection!
```

### Store 3: Calculation Store

```typescript
// src/state/calculationStore.ts
interface CalculationStore {
  // State
  selectedOperations: string[];
  coatingType: CoatingType;
  surfaceQuality: SurfaceQuality;
  coolantType: CoolantType;

  calculationResults: Record<string, CalculationResult>;  // keyed by "T1_ALU_FACE_ROUGH"
  isCalculating: boolean;
  currentPhase: number;  // 1-10 for progress display

  // Actions
  selectOperation: (opId: string) => void;
  setCoating: (coating: CoatingType) => void;
  calculate: (toolId: string, materialId: string, opId: string) => Promise<void>;

  // Results
  getResultsForTool: (toolId: string) => CalculationResult[];
}

// Usage:
const {calculate, calculationResults} = useCalculationStore();
await calculate("T1", "ALU", "FACE_ROUGH");
```

### Store 4: Expert Mode Store

```typescript
// src/state/expertModeStore.ts
interface ExpertModeStore {
  // State
  expertModeEnabled: boolean;
  globalSlider: number;  // -50 to +50
  parameterOverrides: {
    ae_mm?: number;
    ap_mm?: number;
    fz_mm?: number;
  };

  // Calculated values (based on slider + overrides)
  adjustedResults: Record<string, CalculationResult>;

  // Actions
  toggleExpertMode: () => void;
  setGlobalSlider: (value: number) => void;
  setParameterOverride: (param: 'ae' | 'ap' | 'fz', value: number) => void;
  recalculateAdjusted: () => Promise<void>;
}
```

### Store 5: Export Store

```typescript
// src/state/exportStore.ts
interface ExportStore {
  // State
  exportFormat: 'fusion' | 'csv' | 'json' | 'pdf';
  selectedResultsIds: string[];  // Which results to export
  presetName: string;

  // Actions
  selectExportFormat: (format: string) => void;
  toggleResultSelection: (resultId: string) => void;
  export: () => Promise<Blob>;
  savePreset: (name: string) => Promise<void>;
}
```

---

## ZUSTÄNDIGKEITEN: IMPLEMENTATION PHASES

### Phase 1: Project Setup & API Client

**Tasks:**

1. **Create project structure**
   ```
   src/
   ├── screens/
   │   ├── ToolSelection.tsx
   │   ├── MaterialSelection.tsx
   │   ├── OperationSelection.tsx
   │   ├── ParameterConfiguration.tsx
   │   ├── Results.tsx
   │   └── Export.tsx
   ├── state/
   │   ├── toolStore.ts
   │   ├── materialStore.ts
   │   ├── calculationStore.ts
   │   ├── expertModeStore.ts
   │   └── exportStore.ts
   ├── api/
   │   ├── client.ts
   │   └── types.ts
   └── components/
       └── common/ (provided by UI Specialist)
   ```

2. **Generate API Client**
   ```bash
   # From OpenAPI spec (generated from API_CONTRACT.md)
   npm install @apidevtools/swagger-js @swagger-tools/openapi-to-typescript

   # Or manually: create src/api/client.ts
   export class CalculationApiClient {
     async calculate(req: CalculationRequest): Promise<CalculationResponse> {
       const res = await fetch('/api/calculate', {
         method: 'POST',
         body: JSON.stringify(req),
       });
       return res.json();
     }

     async getMaterials(): Promise<Material[]> { ... }
     async getOperations(): Promise<Operation[]> { ... }
     async exportFusion(ids: string[]): Promise<Blob> { ... }
   }
   ```

3. **Initialize Stores**
   ```bash
   npm install zustand  # or @reduxjs/toolkit react-redux

   # Create src/state/ files with initial state
   ```

4. **Main App Router**
   ```typescript
   // src/App.tsx
   import {BrowserRouter, Routes, Route} from 'react-router-dom';

   export const App = () => {
     const [currentScreen, setCurrentScreen] = useState(0);
     const screens = [
       ToolSelection,
       MaterialSelection,
       OperationSelection,
       ParameterConfiguration,
       Results,
       Export,
     ];

     const navigate = (next: number) => setCurrentScreen(Math.max(0, Math.min(5, next)));

     return (
       <div className="app dark-theme">
         <StepIndicator current={currentScreen} total={6} />
         <Screen>{screens[currentScreen]}</Screen>
         <Navigation prev={() => navigate(currentScreen - 1)} next={() => navigate(currentScreen + 1)} />
       </div>
     );
   };
   ```

**Deliverables:**
- [ ] Project structure created
- [ ] API client (client.ts) with all endpoints
- [ ] 5 store files initialized (Zustand or Redux)
- [ ] App.tsx with screen routing
- [ ] StepIndicator + Navigation components

---

### Phase 2: Screen Implementation (Days 2-3)

#### Screen 1: Tool Selection

```typescript
// src/screens/ToolSelection.tsx
import {useToolStore} from '../state/toolStore';
import {Card, Button} from '../components/common';
import {useApi} from '../api/useApi';

export const ToolSelection: React.FC<{onNext: () => void}> = ({onNext}) => {
  const {selectedToolIds, selectTool, deselectTool} = useToolStore();
  const {data: tools, loading} = useApi('/api/tools');

  if (loading) return <div>Loading tools...</div>;

  const handleNext = () => {
    if (selectedToolIds.length > 0) onNext();
    else alert('Select at least one tool');
  };

  return (
    <div className="screen tool-selection">
      <h2>Select Tools to Work With</h2>
      <p>Choose one or more cutting tools for your operations.</p>

      <div className="tool-grid">
        {tools?.map(tool => (
          <Card
            key={tool.id}
            clickable
            selected={selectedToolIds.includes(tool.id)}
            onClick={() => selectedToolIds.includes(tool.id)
              ? deselectTool(tool.id)
              : selectTool(tool.id)
            }
          >
            <h3>{tool.name}</h3>
            <p>DC: {tool.geometry.DC}mm, LCF: {tool.geometry.LCF}mm</p>
            <p>L/D Ratio: {tool.ld_ratio.toFixed(2)} ({tool.ld_classification})</p>
          </Card>
        ))}
      </div>

      <div className="sidebar-summary">
        Selected: {selectedToolIds.length} tools
      </div>

      <Button onClick={handleNext}>Next: Materials</Button>
    </div>
  );
};
```

#### Screen 2: Material Selection (PER TOOL)

**CRITICAL:** Show materials SEPARATELY for each selected tool!

```typescript
// src/screens/MaterialSelection.tsx
export const MaterialSelection: React.FC = () => {
  const {selectedToolIds} = useToolStore();
  const {materialsByTool, selectMaterialForTool} = useMaterialStore();
  const {data: materials} = useApi('/api/materials');
  const [currentToolIndex, setCurrentToolIndex] = useState(0);

  const currentToolId = selectedToolIds[currentToolIndex];
  const currentMaterials = materialsByTool[currentToolId] || [];

  return (
    <div className="screen material-selection">
      <h2>Material Selection</h2>

      {/* Tool Switcher (if multiple tools) */}
      {selectedToolIds.length > 1 && (
        <div className="tool-tabs">
          {selectedToolIds.map((id, i) => (
            <button
              key={id}
              className={i === currentToolIndex ? 'active' : ''}
              onClick={() => setCurrentToolIndex(i)}
            >
              Tool {id}
            </button>
          ))}
        </div>
      )}

      <p>For {currentToolId}: Select applicable materials</p>

      <div className="material-grid">
        {materials?.map(mat => (
          <Card
            key={mat.id}
            selected={currentMaterials.includes(mat.id)}
            onClick={() => selectMaterialForTool(currentToolId, mat.id)}
          >
            <h3>{mat.name}</h3>
            <p>Hardness: {mat.hardness_order} (1=soft, 7=hard)</p>
          </Card>
        ))}
      </div>

      {/* Summary Sidebar */}
      <div className="sidebar-summary">
        <h4>Selected Materials per Tool:</h4>
        {selectedToolIds.map(toolId => (
          <div key={toolId}>
            {toolId}: {materialsByTool[toolId]?.join(', ') || 'None'}
          </div>
        ))}
      </div>
    </div>
  );
};
```

#### Screen 3: Operation Selection

```typescript
// src/screens/OperationSelection.tsx
export const OperationSelection: React.FC = () => {
  const {selectedOperations, selectOperation} = useCalculationStore();
  const {data: operationGroups} = useApi('/api/operations');
  const [expandedGroups, setExpandedGroups] = useState(['FACE']);

  return (
    <div className="screen operation-selection">
      <h2>Select Operations (13 Total)</h2>

      {operationGroups?.map(group => (
        <OperationMatrix
          key={group.group}
          operations={group.operations}
          selectedOperations={selectedOperations}
          onSelectionChange={(opId) => selectOperation(opId)}
          expandedGroups={expandedGroups}
          onToggleGroup={(group) => {
            setExpandedGroups(prev =>
              prev.includes(group)
                ? prev.filter(g => g !== group)
                : [...prev, group]
            );
          }}
        />
      ))}

      <div className="sidebar-summary">
        Selected: {selectedOperations.length} operations
      </div>
    </div>
  );
};
```

#### Screen 4: Coating + Surface Quality

```typescript
// src/screens/ParameterConfiguration.tsx
export const ParameterConfiguration: React.FC = () => {
  const {coatingType, surfaceQuality, coolantType, setCoating, setSurfaceQuality, setCoolant}
    = useCalculationStore();

  return (
    <div className="screen parameter-config">
      <h2>Tool & Surface Settings</h2>

      <Card title="Coating Type" bordered>
        <div className="coating-buttons">
          {['NONE', 'TIN', 'TIALN', 'ALTIN', 'DIAMOND', 'CARBIDE'].map(ct => (
            <Button
              key={ct}
              variant={coatingType === ct ? 'primary' : 'secondary'}
              onClick={() => setCoating(ct as CoatingType)}
            >
              {ct} {ct !== 'NONE' && `+${getCoatingFactor(ct) * 100 - 100}%`}
            </Button>
          ))}
        </div>
      </Card>

      <Card title="Surface Quality" bordered>
        <div className="quality-buttons">
          {['ROUGHING', 'STANDARD', 'FINISHING', 'HIGH_FINISH'].map(sq => (
            <Button
              key={sq}
              variant={surfaceQuality === sq ? 'primary' : 'secondary'}
              onClick={() => setSurfaceQuality(sq as SurfaceQuality)}
            >
              {sq}
            </Button>
          ))}
        </div>
      </Card>

      <Card title="Coolant Type" bordered>
        <div className="coolant-buttons">
          {['WET', 'DRY', 'MQL'].map(ct => (
            <Button
              key={ct}
              variant={coolantType === ct ? 'primary' : 'secondary'}
              onClick={() => setCoolant(ct as CoolantType)}
            >
              {ct}
            </Button>
          ))}
        </div>
      </Card>
    </div>
  );
};
```

#### Screen 5: Results + Expert Mode

```typescript
// src/screens/Results.tsx
export const Results: React.FC = () => {
  const {selectedToolIds} = useToolStore();
  const {materialsByTool} = useMaterialStore();
  const {selectedOperations, calculationResults, calculate, isCalculating} = useCalculationStore();
  const {expertModeEnabled, toggleExpertMode, globalSlider, setGlobalSlider} = useExpertModeStore();

  useEffect(() => {
    // Auto-calculate when prerequisites are selected
    const calculateAll = async () => {
      for (const toolId of selectedToolIds) {
        const mats = materialsByTool[toolId] || [];
        for (const matId of mats) {
          for (const opId of selectedOperations) {
            await calculate(toolId, matId, opId);
          }
        }
      }
    };
    calculateAll();
  }, [selectedToolIds, materialsByTool, selectedOperations]);

  return (
    <div className="screen results">
      <h2>Calculation Results</h2>

      {isCalculating && <ProgressBar current={3} total={10} />}

      <div className="results-table">
        <Table
          data={Object.values(calculationResults)}
          columns={[
            {key: 'tool', header: 'Tool', accessor: r => r.tool.name},
            {key: 'material', header: 'Material', accessor: r => r.input.material},
            {key: 'operation', header: 'Operation', accessor: r => r.input.operation},
            {key: 'vc', header: 'vc (m/min)', accessor: r => r.results.vc_final, render: v => v.toFixed(1)},
            {key: 'n', header: 'n (RPM)', accessor: r => r.results.n_rpm},
            {key: 'vf', header: 'vf (mm/min)', accessor: r => r.results.vf_mm_min, render: v => v.toFixed(1)},
            {key: 'status', header: 'Status', accessor: r => r.validation.all_passed ? '✓' : '⚠'},
          ]}
        />
      </div>

      {/* Expert Mode Toggle */}
      <label>
        <input
          type="checkbox"
          checked={expertModeEnabled}
          onChange={toggleExpertMode}
        />
        Enable Expert Mode
      </label>

      {expertModeEnabled && (
        <ExpertModePanel />
      )}
    </div>
  );
};

const ExpertModePanel: React.FC = () => {
  const {globalSlider, setGlobalSlider, parameterOverrides, setParameterOverride, recalculateAdjusted}
    = useExpertModeStore();

  return (
    <Card title="Expert Mode: Global Adjustment" elevated>
      <Slider
        min={-50}
        max={50}
        value={globalSlider}
        onChange={(v) => {
          setGlobalSlider(v);
          recalculateAdjusted();
        }}
        markers={[
          {value: -50, label: 'Conservative'},
          {value: 0, label: 'Optimal'},
          {value: 50, label: 'Aggressive'},
        ]}
        showValue
      />

      <div className="parameter-overrides">
        <h4>Individual Parameter Overrides:</h4>
        <CompactSlider
          label="ae"
          min={-100}
          max={100}
          value={parameterOverrides.ae_mm || 0}
          onChange={(v) => {
            setParameterOverride('ae', v);
            recalculateAdjusted();
          }}
          unit="%"
          showValue
        />
        {/* Similar for ap, fz */}
      </div>
    </Card>
  );
};
```

#### Screen 6: Export

```typescript
// src/screens/Export.tsx
export const Export: React.FC = () => {
  const {calculationResults} = useCalculationStore();
  const {exportFormat, selectedResultsIds, toggleResultSelection, export: doExport}
    = useExportStore();

  const handleExport = async () => {
    const blob = await doExport();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cnc-toolcalc-${exportFormat}.${exportFormat === 'fusion' ? 'tools' : exportFormat}`;
    a.click();
  };

  return (
    <div className="screen export">
      <h2>Export Results</h2>

      <Card title="Export Format" bordered>
        <label>
          <input type="checkbox" onChange={() => {}} />
          Fusion 360 (.tools ZIP)
        </label>
        <label>
          <input type="checkbox" onChange={() => {}} />
          Underscott CSV
        </label>
      </Card>

      <Card title="Select Results to Export" bordered>
        <Table
          data={Object.values(calculationResults)}
          selectable
          selectedRows={selectedResultsIds}
          onSelectionChange={toggleResultSelection}
          columns={[...columns]}
        />
      </Card>

      <Button onClick={handleExport} variant="primary">
        Export
      </Button>
    </div>
  );
};
```

**Deliverables:**
- [ ] All 6 screen components implemented
- [ ] Navigation between screens working
- [ ] Material selection working (per-tool, not global!)
- [ ] API integration (calculate on results screen)
- [ ] Progressive disclosure (basic + expert mode)
- [ ] Export functionality

---

## WORKFLOW: CHANGE REQUESTS

### CR-2025-11-10-002: Frontend Workflow Implementation

```
Title: Phase 3 - Frontend Workflow (6 Screens + State Management)

Assigned To: frontend-workflow
Target Version: v0.3.0
Estimated Effort: 24h

Requirements:
1. 6-Screen workflow implementation
2. State management (5 stores)
3. Backend API integration
4. Material selection PER TOOL (critical!)
5. Expert mode UI
6. Progressive disclosure

Acceptance Criteria:
- All 6 screens navigate correctly
- Material selection is per-tool (not global)
- Calculation results display correctly
- Expert mode: global slider + overrides work
- API calls return expected data
- E2E tests for all user flows

Tests:
- Navigation tests (forward/backward)
- State management tests (Zustand/Redux)
- API integration tests
- E2E tests via Playwright
```

### Implementation Workflow

```bash
# Create CR
cp docs/change-requests/CR_TEMPLATE.md \
   docs/change-requests/active/CR-2025-11-10-002.md

# Start branch
git checkout -b agent/frontend-workflow

# Implement screens (Days 2-3)
npm install zustand react-router-dom
mkdir -p src/{screens,state,api,components/common}
# Create all screen files
# Create all store files
# Create API client

# Test
npm run test:frontend -- --coverage
npm run test:e2e

# Commit
git add src/
git commit -m "[FRONTEND-WORKFLOW] IMPL: All 6 screens + state management"

# Push for review
git push origin agent/frontend-workflow
```

---

## QUALITY CHECKLIST

Before pushing for review:

- [ ] All 6 screens navigate correctly
- [ ] Material selection is **per-tool** (verify by selecting tool T1, then materials for T1 separately)
- [ ] State persists when navigating back
- [ ] API calls successful (check network tab)
- [ ] Calculation results display on Screen 5
- [ ] Expert mode toggle works
- [ ] Global slider changes results
- [ ] Individual parameter overrides work
- [ ] Export screen shows results to export
- [ ] E2E tests >90% pass rate
- [ ] Coverage >85%
- [ ] No TypeScript errors
- [ ] Accessibility: keyboard navigation on all screens

---

## SUCCESS METRICS

**Phase 3 Complete When:**
- ✅ 6 screens fully functional
- ✅ Material selection per-tool (verified)
- ✅ Expert mode working (global + overrides)
- ✅ E2E tests >90% pass
- ✅ Coverage >85%
- ✅ API integration working
- ✅ Progressive disclosure logic correct

---

**Last Updated:** 2025-11-10
**Agent:** Frontend/Workflow
**Mode:** FULL EXECUTION
