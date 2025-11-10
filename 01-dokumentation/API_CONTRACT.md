# API Contract: Frontend ↔ Backend

**Version:** v0.0.1-alpha
**Last Updated:** 2025-11-10
**Status:** DRAFT

---

## Base URL

**Development:** `http://localhost:8000`
**Production:** TBD

---

## Authentication

None (internal tool, local deployment)

---

## Common Headers

```
Content-Type: application/json
Accept: application/json
```

---

## Error Response Format

All errors follow this schema:

```typescript
interface ErrorResponse {
  error: {
    code: string;           // "VALIDATION_ERROR", "CALCULATION_ERROR", etc.
    message: string;        // Human-readable error message
    details?: any;          // Optional detailed error info
  }
}
```

**Example:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Tool diameter must be greater than 0",
    "details": {
      "field": "tool_diameter",
      "value": -5,
      "constraint": "must be > 0"
    }
  }
}
```

---

## Endpoints

### 1. Health Check

**GET** `/health`

**Description:** Check if API is running

**Response:**
```typescript
interface HealthResponse {
  status: "ok" | "error";
  version: string;
  timestamp: string;
}
```

**Example:**
```json
{
  "status": "ok",
  "version": "0.0.1-alpha",
  "timestamp": "2025-11-10T12:00:00Z"
}
```

---

### 2. Import Tool Library

**POST** `/api/import`

**Description:** Import Fusion 360 .tools file (ZIP) or .json library

**Request:** `multipart/form-data`
```typescript
interface ImportRequest {
  file: File;  // .tools (ZIP) or .json
}
```

**Response:**
```typescript
interface ImportResponse {
  tools: Tool[];
  materials_detected: DetectedMaterial[];
  operations_detected: DetectedOperation[];
  message: string;
}

interface Tool {
  id: string;                    // "T1", "T2", etc.
  name: string;                  // "Planfräser Ø30mm"
  type: string;                  // "flat end mill", "ball mill", etc.
  geometry: {
    DC: number;                  // Cutting diameter [mm]
    LCF: number;                 // Cutting length [mm]
    DCON: number;                // Connection diameter [mm]
    OAL: number;                 // Overall length [mm]
    NOF: number;                 // Number of flutes
  };
  ld_ratio: number;              // L/D ratio (calculated)
  ld_classification: string;     // "short" | "normal" | "long" | "very_long"
  presets?: Preset[];            // Existing presets from Fusion (if any)
}

interface DetectedMaterial {
  tool_id: string;               // Which tool has this material
  material: string;              // "Aluminium", "Softwood", etc.
  source: string;                // "Alu_Face_Finish" (preset name)
  count: number;                 // How many presets with this material
}

interface DetectedOperation {
  tool_id: string;
  operation: string;             // "FACE_FINISH", "SLOT_ROUGH", etc.
  source: string;
  count: number;
}

interface Preset {
  name: string;                  // "Alu_Face_Finish"
  material?: string;             // Parsed material (if detectable)
  operation?: string;            // Parsed operation (if detectable)
  parameters: {
    vc?: number;                 // Reference vc from Fusion
    n?: number;                  // Reference RPM
    fz?: number;                 // Reference chip load
    vf?: number;                 // Reference feed rate
    ae?: number;                 // Reference radial engagement
    ap?: number;                 // Reference axial depth
  };
}
```

**Example Response:**
```json
{
  "tools": [
    {
      "id": "T1",
      "name": "Planfräser Ø30mm",
      "type": "flat end mill",
      "geometry": {
        "DC": 30.0,
        "LCF": 8.0,
        "DCON": 25.0,
        "OAL": 80.0,
        "NOF": 3
      },
      "ld_ratio": 0.27,
      "ld_classification": "short",
      "presets": [
        {
          "name": "Alu_Face_Finish",
          "material": "Aluminium",
          "operation": "FACE_FINISH",
          "parameters": {
            "vc": 150.0,
            "n": 20000,
            "fz": 0.05,
            "vf": 3000,
            "ae": 15.0,
            "ap": 2.4
          }
        }
      ]
    }
  ],
  "materials_detected": [
    {
      "tool_id": "T1",
      "material": "Aluminium",
      "source": "Alu_Face_Finish",
      "count": 2
    }
  ],
  "operations_detected": [
    {
      "tool_id": "T1",
      "operation": "FACE_FINISH",
      "source": "Alu_Face_Finish",
      "count": 1
    }
  ],
  "message": "Imported 13 tools successfully. 6 presets detected."
}
```

---

### 3. Get Available Materials

**GET** `/api/materials`

**Description:** Get all available materials (sorted by hardness)

**Response:**
```typescript
interface MaterialsResponse {
  materials: Material[];
}

interface Material {
  id: string;                    // "softwood", "aluminium", etc.
  name: string;                  // "Softwood (Weichholz)"
  hardness_order: number;        // 1 (softest) to 7 (hardest)
  color: string;                 // UI color code
  category: string;              // "wood", "metal", "plastic"
}
```

**Example:**
```json
{
  "materials": [
    {
      "id": "softwood",
      "name": "Softwood (Weichholz)",
      "hardness_order": 1,
      "color": "#d4a574",
      "category": "wood"
    },
    {
      "id": "aluminium",
      "name": "Aluminium (6061, 7075)",
      "hardness_order": 3,
      "color": "#c0c0c0",
      "category": "metal"
    }
  ]
}
```

---

### 4. Get Available Operations

**GET** `/api/operations`

**Description:** Get all 13 operations grouped by category

**Response:**
```typescript
interface OperationsResponse {
  operations: OperationGroup[];
}

interface OperationGroup {
  group: string;                 // "FACE", "SLOT", "GEOMETRY", "SPECIAL"
  operations: Operation[];
}

interface Operation {
  id: string;                    // "FACE_ROUGH", "SLOT_TROCHOIDAL", etc.
  name: string;                  // "Face Roughing (Schruppen)"
  description: string;
  typical_ae_range: string;      // "50-100% DC"
  typical_ap_range: string;      // "DC/2 to DC"
}
```

**Example:**
```json
{
  "operations": [
    {
      "group": "FACE",
      "operations": [
        {
          "id": "FACE_ROUGH",
          "name": "Face Roughing (Schruppen)",
          "description": "High MRR, coarse surface finish",
          "typical_ae_range": "70-100% DC",
          "typical_ap_range": "DC/2 to DC"
        },
        {
          "id": "FACE_FINISH",
          "name": "Face Finishing (Schlichten)",
          "description": "Low MRR, fine surface finish",
          "typical_ae_range": "30-60% DC",
          "typical_ap_range": "LCF/2 to LCF"
        }
      ]
    },
    {
      "group": "SLOT",
      "operations": [
        {
          "id": "SLOT_TROCHOIDAL",
          "name": "Slot Trochoidal (Progressive)",
          "description": "Small circular paths, low radial load",
          "typical_ae_range": "10-20% DC",
          "typical_ap_range": "Full depth (LCF)"
        }
      ]
    }
  ]
}
```

---

### 5. Calculate Parameters (MAIN ENDPOINT)

**POST** `/api/calculate`

**Description:** Calculate cutting parameters for given tool/material/operation

**Request:**
```typescript
interface CalculationRequest {
  tool_id: string;                      // "T1"
  material: string;                     // "aluminium", "softwood", etc.
  operation: string;                    // "FACE_ROUGH", "SLOT_TROCHOIDAL", etc.
  coating?: CoatingType;                // Optional coating
  surface_quality?: SurfaceQuality;     // Optional quality level
  coolant?: CoolantType;                // Optional coolant type
  expert_mode?: ExpertModeSettings;     // Optional expert overrides
}

enum CoatingType {
  NONE = "none",
  TIN = "tin",          // +40% vc
  TIALN = "tialn",      // +60% vc
  ALTIN = "altin",      // +80% vc
  DIAMOND = "diamond",  // +120% vc (non-ferrous only!)
  CARBIDE = "carbide"   // +50% vc
}

enum SurfaceQuality {
  ROUGHING = "roughing",       // 100% ae/ap
  STANDARD = "standard",       // 80/90% ae/ap
  FINISHING = "finishing",     // 60/70% ae/ap
  HIGH_FINISH = "high_finish"  // 40/50% ae/ap
}

enum CoolantType {
  WET = "wet",         // Normal
  DRY = "dry",         // -30% fz
  MQL = "mql"          // -15% fz
}

interface ExpertModeSettings {
  global_adjustment: number;    // -50 to +50 (percentage)
  overrides?: {
    ae_mm?: number;             // Direct override
    ap_mm?: number;
    fz_mm?: number;
  };
}
```

**Response:**
```typescript
interface CalculationResponse {
  calculation_id: string;                   // Unique ID for this calculation
  timestamp: string;
  tool: Tool;                               // Echo back tool info
  input: CalculationRequest;                // Echo back input
  results: CalculationResults;
  validation: ValidationChecks;
  warnings: string[];
  mathematical_workbook?: FormulaBreakdown; // If requested
}

interface CalculationResults {
  // Phase 1-2: Cutting Speed
  vc_base: number;                          // Base vc [m/min]
  coating_factor: number;                   // 1.0 - 2.2
  vc_final: number;                         // vc after coating [m/min]

  // Phase 3: Spindle Speed
  n_rpm: number;                            // Spindle speed [RPM]

  // Phase 4-5: Feed
  fz_base: number;                          // Base chip load [mm/tooth]
  coolant_factor: number;                   // 0.7 - 1.0
  fz_final: number;                         // fz after coolant [mm/tooth]
  vf_mm_min: number;                        // Feed rate [mm/min]
  vf_entry: number;                         // Entry feed [mm/min]
  vf_ramp: number;                          // Ramp feed [mm/min]
  vf_plunge: number;                        // Plunge feed [mm/min]

  // Phase 6-8: Engagement
  ae_mm: number;                            // Radial engagement [mm]
  ap_mm: number;                            // Axial depth [mm]
  ap_reference: string;                     // "DC" or "LCF" (dynamic logic!)
  surface_quality_factor: number;           // 0.4 - 1.0

  // Phase 9-10: Power & Thermal
  mrr_cm3_min: number;                      // Material removal rate
  power_kw: number;                         // Cutting power [kW]
  torque_nm: number;                        // Torque [Nm]
  chip_temperature_c: number;               // Chip temperature [°C]
  chip_formation: ChipFormationType;        // Chip type prediction

  // L/D Stability
  ld_ratio: number;
  ld_classification: string;
  ld_reduction_factor: number;              // 1.0 (no reduction) to 0.5
}

enum ChipFormationType {
  CONTINUOUS = "continuous",        // Long, stringy chips
  SEGMENTED = "segmented",          // Medium chips
  DISCONTINUOUS = "discontinuous",  // Short chips
  DUST = "dust"                     // Wood dust/powder
}

interface ValidationChecks {
  all_passed: boolean;
  checks: ValidationCheck[];
}

interface ValidationCheck {
  name: string;                     // "rpm_within_limit", "power_available", etc.
  passed: boolean;
  message: string;
  severity: "info" | "warning" | "error";
  value?: any;                      // Actual value
  limit?: any;                      // Limit value
}

interface FormulaBreakdown {
  vc: {
    formula: string;                // "vc_base × coating_factor"
    steps: string[];                // ["120 m/min × 1.4", "= 168 m/min"]
    reference?: number;             // Fusion preset value (if available)
    deviation?: number;             // % deviation from reference
  };
  // ... similar for n, fz, vf, ae, ap, power, etc.
}
```

**Example Request:**
```json
{
  "tool_id": "T1",
  "material": "aluminium",
  "operation": "FACE_FINISH",
  "coating": "tin",
  "surface_quality": "finishing",
  "coolant": "wet",
  "expert_mode": {
    "global_adjustment": 15,
    "overrides": {
      "ae_mm": 10.5
    }
  }
}
```

**Example Response:**
```json
{
  "calculation_id": "calc_20251110_120034_t1",
  "timestamp": "2025-11-10T12:00:34Z",
  "tool": { ... },
  "input": { ... },
  "results": {
    "vc_base": 120.0,
    "coating_factor": 1.4,
    "vc_final": 168.0,
    "n_rpm": 18000,
    "fz_base": 0.05,
    "coolant_factor": 1.0,
    "fz_final": 0.05,
    "vf_mm_min": 2700,
    "vf_entry": 1350,
    "vf_ramp": 900,
    "vf_plunge": 450,
    "ae_mm": 10.5,
    "ap_mm": 2.4,
    "ap_reference": "DC",
    "surface_quality_factor": 0.6,
    "mrr_cm3_min": 45.5,
    "power_kw": 0.65,
    "torque_nm": 0.35,
    "chip_temperature_c": 285,
    "chip_formation": "segmented",
    "ld_ratio": 0.27,
    "ld_classification": "short",
    "ld_reduction_factor": 1.0
  },
  "validation": {
    "all_passed": true,
    "checks": [
      {
        "name": "rpm_within_limit",
        "passed": true,
        "message": "RPM 18000 within spindle limit 30000",
        "severity": "info",
        "value": 18000,
        "limit": 30000
      },
      {
        "name": "power_available",
        "passed": true,
        "message": "Power 0.65 kW available (max 0.71 kW)",
        "severity": "info",
        "value": 0.65,
        "limit": 0.71
      }
    ]
  },
  "warnings": [
    "Expert mode active: ae manually overridden to 10.5mm"
  ]
}
```

---

### 6. Export to Fusion 360

**POST** `/api/export/fusion`

**Description:** Export calculation results as Fusion 360 .tools ZIP

**Request:**
```typescript
interface ExportRequest {
  calculation_ids: string[];        // Array of calculation IDs to export
  library_name?: string;            // Optional library name
}
```

**Response:** Binary `.tools` file (ZIP)
```
Content-Type: application/zip
Content-Disposition: attachment; filename="cnc-toolcalc-export.tools"
```

**ZIP Contents:**
```
export.tools (ZIP)
└── tools.json                      // Fusion 360 tool library format
    ├── version
    ├── tools[]
    │   ├── guid
    │   ├── description
    │   ├── geometry { ... }
    │   └── presets[]
    │       ├── name: "Alu_Face_Finish"
    │       ├── description
    │       └── expressions[13]     // 13 mandatory expressions!
    │           ├── tool_diameter
    │           ├── tool_fluteLength
    │           ├── ... (11 more)
```

---

### 7. Export to Underscott CSV

**POST** `/api/export/underscott`

**Description:** Export calculation results as Underscott Disco CSV

**Request:**
```typescript
interface UndersottExportRequest {
  calculation_ids: string[];
}
```

**Response:** CSV file
```
Content-Type: text/csv
Content-Disposition: attachment; filename="cnc-toolcalc-underscott.csv"
```

**CSV Format:**
```csv
Tool,Material,Operation,DC,LCF,vc,n,fz,vf,ae,ap
T1,Aluminium,FACE_FINISH,30,8,168,18000,0.05,2700,10.5,2.4
...
```

---

## Validation Rules

### Tool Validation
- DC > 0
- LCF > 0
- OAL > LCF
- NOF >= 1

### Material Validation
- Must be one of 7 supported materials
- Diamond coating ONLY for non-ferrous (Aluminium, Brass, Acrylic, Copper)

### Operation Validation
- Must be one of 13 supported operations
- Tool must be suitable for operation (e.g., no ball mill for face milling)

### Expert Mode Validation
- global_adjustment: -50 to +50
- Overrides must be positive
- Overrides cannot exceed safety limits (e.g., ae <= DC, ap <= LCF)

---

## Rate Limiting

None (local deployment, internal tool)

---

## Versioning

API version follows project version: `v0.0.1-alpha`

Breaking changes will increment major version.

---

**Status:** ✅ READY FOR IMPLEMENTATION
**Last Updated:** 2025-11-10
**Approved by:** Governance Agent
