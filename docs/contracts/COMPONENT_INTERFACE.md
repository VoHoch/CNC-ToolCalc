# Component Interfaces: UI Components Specification

**Version:** v0.0.1-alpha
**Last Updated:** 2025-11-10
**Status:** DRAFT

---

## Design System Foundation

All components follow the **Dark Theme** design system with 3 contrast modes:
- `medium`: Lower contrast (borders: rgba(255,255,255,0.06))
- `balanced`: Standard (borders: rgba(255,255,255,0.12)) **← DEFAULT**
- `high`: High contrast (borders: rgba(255,255,255,0.16))

**Colors:**
```css
--bg-primary: #0b0f15
--bg-secondary: #12161d
--bg-tertiary: #1a1f27

--text-primary: #e2e8f0
--text-secondary: #aeb8c4
--text-muted: #7a8491

--accent-primary: #6366F1  /* Indigo */
--accent-hover: #818cf8
```

**Spacing Scale (Compact):**
```css
--space-1: 0.125rem  /* 2px */
--space-2: 0.25rem   /* 4px */
--space-3: 0.5rem    /* 8px */
--space-4: 0.75rem   /* 12px */
--space-5: 1rem      /* 16px */
--space-6: 1.25rem   /* 20px */
--space-8: 1.5rem    /* 24px */
--space-10: 2rem     /* 32px */
```

**Typography:**
```css
--font-primary: Inter, system-ui, sans-serif
--font-headline: Work Sans, Inter, sans-serif
--font-mono: Fira Code, monospace
```

---

## 1. Slider Component

**Purpose:** Marker-based slider with gradient background (Blue → Green → Red)

**Key Feature:** **NO visible thumb!** Uses markers instead.

### Props Interface

```typescript
interface SliderProps {
  // Value
  min: number;                          // Min value
  max: number;                          // Max value
  value: number;                        // Current value
  defaultValue?: number;                // Initial value (if uncontrolled)

  // Markers
  markers: MarkerDefinition[];          // Positions for Conservative, Optimal, Aggressive

  // Appearance
  gradient?: [string, string, string];  // [start, middle, end] colors
                                        // Default: ['#3b82f6', '#22c55e', '#ef4444']
  trackHeight?: number;                 // Track height in px (default: 8)

  // Labels
  showValue?: boolean;                  // Show current value above slider
  valueFormatter?: (value: number) => string; // Custom value display
  leftLabel?: string;                   // Label left of track
  rightLabel?: string;                  // Label right of track

  // Behavior
  onChange: (value: number) => void;    // Value change callback
  onChangeCommitted?: (value: number) => void; // Final value (mouse up)
  disabled?: boolean;
  step?: number;                        // Step size (default: 1)

  // Compact Mode
  compact?: boolean;                    // Use smaller version (height: 6px)
}

interface MarkerDefinition {
  value: number;                        // Position value
  label: string;                        // "Conservative", "Optimal", "Aggressive"
  color?: string;                       // Optional custom color
  active?: boolean;                     // Is this the current selection?
}
```

### CSS Requirements

```css
/* Slider thumb MUST be invisible */
.slider-input::-webkit-slider-thumb {
  width: 0;
  height: 0;
  opacity: 0;
  cursor: pointer;
}

.slider-input::-moz-range-thumb {
  width: 0;
  height: 0;
  opacity: 0;
  cursor: pointer;
}

/* Track with gradient */
.slider-track {
  background: linear-gradient(
    to right,
    var(--gradient-start),    /* Blue */
    var(--gradient-middle),   /* Green */
    var(--gradient-end)       /* Red */
  );
}

/* Markers */
.slider-marker {
  position: absolute;
  width: 3px;
  height: 16px;
  background: var(--text-secondary);
  border-radius: 2px;
}

.slider-marker--active {
  background: var(--accent-primary);
  box-shadow: 0 0 8px var(--accent-primary);
}
```

### Usage Example

```tsx
<Slider
  min={-50}
  max={50}
  value={expertSliderValue}
  markers={[
    { value: -50, label: "Conservative", active: expertSliderValue === -50 },
    { value: 0, label: "Optimal", active: expertSliderValue === 0 },
    { value: 50, label: "Aggressive", active: expertSliderValue === 50 }
  ]}
  gradient={['#3b82f6', '#22c55e', '#ef4444']}
  showValue={true}
  valueFormatter={(v) => `${v > 0 ? '+' : ''}${v}%`}
  leftLabel="Conservative"
  rightLabel="Aggressive"
  onChange={setExpertSliderValue}
/>
```

---

## 2. CompactSlider Component

**Purpose:** Bidirectional slider for Expert Mode (-100% to +100%)

**Key Feature:** Center at 0%, visual distinction for negative/positive

### Props Interface

```typescript
interface CompactSliderProps {
  // Value
  min: number;                          // Typically -100
  max: number;                          // Typically +100
  value: number;                        // Current value
  centerValue?: number;                 // Center point (default: 0)

  // Appearance
  height?: number;                      // Track height (default: 6px)
  negativeColor?: string;               // Color for negative range
  positiveColor?: string;               // Color for positive range
  centerColor?: string;                 // Color at center

  // Labels
  label?: string;                       // Parameter label (e.g., "ae")
  unit?: string;                        // Unit (e.g., "mm", "%")
  showValue?: boolean;                  // Show numeric value

  // Behavior
  onChange: (value: number) => void;
  disabled?: boolean;
  step?: number;                        // Default: 1
}
```

### Visual Behavior

```
Negative Range      Center       Positive Range
    (Blue)         (White)          (Orange)
◄─────────────────────●─────────────────────►
-100%               0%                  +100%
```

### Usage Example

```tsx
<CompactSlider
  label="ae"
  min={-100}
  max={100}
  value={aeOverride}
  unit="%"
  showValue={true}
  negativeColor="#3b82f6"
  positiveColor="#f97316"
  centerColor="#ffffff"
  onChange={setAeOverride}
/>
```

---

## 3. Table Component

**Purpose:** Sortable, filterable data table with dark theme

### Props Interface

```typescript
interface TableProps<T> {
  // Data
  data: T[];                            // Array of row objects
  columns: ColumnDefinition<T>[];       // Column definitions

  // Sorting
  sortable?: boolean;                   // Enable sorting (default: true)
  defaultSortColumn?: string;           // Initial sort column key
  defaultSortOrder?: 'asc' | 'desc';    // Initial sort order

  // Selection
  selectable?: boolean;                 // Enable row selection
  selectedRows?: string[];              // Array of selected row IDs
  onSelectionChange?: (selectedIds: string[]) => void;

  // Styling
  compact?: boolean;                    // Smaller padding
  striped?: boolean;                    // Alternating row colors
  hoverable?: boolean;                  // Hover effect (default: true)

  // Behavior
  onRowClick?: (row: T) => void;
  emptyMessage?: string;                // Message when no data
}

interface ColumnDefinition<T> {
  key: string;                          // Unique column key
  header: string;                       // Column header text
  accessor: (row: T) => any;            // Get value from row
  sortable?: boolean;                   // Override global sortable
  width?: string;                       // Column width (e.g., "100px", "20%")
  align?: 'left' | 'center' | 'right'; // Text alignment
  render?: (value: any, row: T) => React.ReactNode; // Custom cell renderer
}
```

### CSS Requirements

```css
.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  color: var(--text-primary);
}

.table thead {
  background: var(--bg-secondary);
  border-bottom: 2px solid var(--border-default);
}

.table th {
  padding: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.table tbody tr {
  border-bottom: 1px solid var(--border-default);
}

.table tbody tr:hover {
  background: var(--bg-secondary);
}

.table td {
  padding: 0.5rem 0.75rem;
  color: var(--text-primary);
}

/* Sortable header */
.table th.sortable {
  cursor: pointer;
  user-select: none;
}

.table th.sortable:hover {
  color: var(--text-primary);
}
```

### Usage Example

```tsx
<Table
  data={calculationResults}
  columns={[
    {
      key: 'name',
      header: 'Preset Name',
      accessor: (row) => row.name,
      width: '200px'
    },
    {
      key: 'vc',
      header: 'vc (m/min)',
      accessor: (row) => row.vc_final,
      align: 'right',
      render: (value) => value.toFixed(1)
    },
    {
      key: 'status',
      header: 'Status',
      accessor: (row) => row.status,
      render: (value) => (
        <StatusBadge status={value} />
      )
    }
  ]}
  sortable={true}
  hoverable={true}
  onRowClick={(row) => selectPreset(row.id)}
/>
```

---

## 4. Button Component

**Purpose:** Consistent button styling across app

### Props Interface

```typescript
interface ButtonProps {
  // Content
  children: React.ReactNode;

  // Appearance
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'small' | 'medium' | 'large';
  fullWidth?: boolean;

  // State
  disabled?: boolean;
  loading?: boolean;                    // Show spinner

  // Behavior
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';

  // Icon
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}
```

### Variants

```css
/* Primary */
.button--primary {
  background: var(--accent-primary);
  color: white;
}

.button--primary:hover {
  background: var(--accent-hover);
}

/* Secondary */
.button--secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
}

/* Ghost */
.button--ghost {
  background: transparent;
  color: var(--text-secondary);
}

.button--ghost:hover {
  background: var(--bg-secondary);
}

/* Danger */
.button--danger {
  background: #ef4444;
  color: white;
}
```

---

## 5. Card Component

**Purpose:** Container for tool/material/operation cards

### Props Interface

```typescript
interface CardProps {
  // Content
  title?: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;

  // Appearance
  variant?: 'default' | 'bordered' | 'elevated';
  padding?: 'none' | 'small' | 'medium' | 'large';

  // Interaction
  hoverable?: boolean;
  clickable?: boolean;
  onClick?: () => void;
  selected?: boolean;                   // For selectable cards

  // Icon/Badge
  icon?: React.ReactNode;
  badge?: string | number;
}
```

### CSS Requirements

```css
.card {
  background: var(--bg-primary);
  border-radius: 0.5rem;
  padding: var(--space-5);
}

.card--bordered {
  border: 1px solid var(--border-default);
}

.card--elevated {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.card--hoverable:hover {
  background: var(--bg-secondary);
  border-color: var(--accent-primary);
}

.card--selected {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3);
}
```

---

## 6. OperationMatrix Component

**Purpose:** 4-group operation selector with collapse/expand

### Props Interface

```typescript
interface OperationMatrixProps {
  // Data
  operations: OperationGroup[];         // 4 groups (FACE, SLOT, GEOMETRY, SPECIAL)
  selectedOperations: string[];         // Array of selected operation IDs

  // Behavior
  onSelectionChange: (selectedIds: string[]) => void;
  multiSelect?: boolean;                // Allow multiple selections

  // Appearance
  expandedGroups?: string[];            // Initially expanded group names
  showDescriptions?: boolean;           // Show operation descriptions
}

interface OperationGroup {
  name: string;                         // "FACE", "SLOT", etc.
  displayName: string;                  // "Face Milling"
  operations: OperationItem[];
}

interface OperationItem {
  id: string;                           // "FACE_ROUGH", "SLOT_TROCHOIDAL", etc.
  name: string;                         // Display name
  description?: string;
  icon?: string;                        // Optional icon
}
```

### Visual Layout

```
┌─────────────────────────────────────────────────────┐
│ ▼ FACE (Planfräsen)                         [2/2]   │
├─────────────────────────────────────────────────────┤
│   [☑] Face Roughing (Schruppen)                    │
│       High MRR, coarse surface                      │
│   [☑] Face Finishing (Schlichten)                  │
│       Low MRR, fine surface                         │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ ► SLOT (Nuten/Taschen)                      [0/4]   │
└─────────────────────────────────────────────────────┘
```

---

## 7. ProgressBar Component

**Purpose:** Real-time calculation progress indicator

### Props Interface

```typescript
interface ProgressBarProps {
  // Progress
  current: number;                      // Current step (1-10)
  total: number;                        // Total steps (typically 10)

  // Labels
  currentStepLabel?: string;            // "Phase 3: Spindle Speed"
  showPercentage?: boolean;

  // Appearance
  height?: number;                      // Bar height (default: 8px)
  color?: string;                       // Progress color
  animated?: boolean;                   // Animate progress
}
```

### Usage Example

```tsx
<ProgressBar
  current={currentPhase}
  total={10}
  currentStepLabel={`Phase ${currentPhase}: ${phaseNames[currentPhase]}`}
  showPercentage={true}
  animated={true}
/>
```

---

## Component Hierarchy

```
App
├── ImportScreen
│   └── FileUpload
│       └── ProgressBar
├── ToolSelectionScreen
│   └── Card (tool cards)
├── MaterialSelectionScreen
│   └── Card (material cards)
├── OperationScreen
│   └── OperationMatrix
├── ParameterScreen
│   ├── Card (coating selector)
│   ├── Card (surface quality)
│   └── Slider (surface quality slider)
├── ResultsScreen
│   ├── Table (results table)
│   └── ExpertModePanel
│       ├── Slider (global adjustment)
│       └── CompactSlider[] (parameter overrides)
└── ExportScreen
    └── Button (export actions)
```

---

## Accessibility Requirements

All components MUST meet **WCAG 2.1 Level AA**:

- ✅ Keyboard navigation (Tab, Enter, Arrow keys)
- ✅ ARIA labels and roles
- ✅ Focus indicators (visible outline)
- ✅ Color contrast ≥ 4.5:1 for text
- ✅ Screen reader support

---

**Status:** ✅ READY FOR IMPLEMENTATION
**Last Updated:** 2025-11-10
**Approved by:** Governance Agent
