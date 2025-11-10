// API Types - Generated from API_CONTRACT.md

// ============================================================================
// Tool Types
// ============================================================================

export interface Tool {
  id: string;
  name: string;
  type: string;
  geometry: ToolGeometry;
  ld_ratio: number;
  ld_classification: string;
  presets?: Preset[];
}

export interface ToolGeometry {
  DC: number;    // Cutting diameter [mm]
  LCF: number;   // Cutting length [mm]
  DCON: number;  // Connection diameter [mm]
  OAL: number;   // Overall length [mm]
  NOF: number;   // Number of flutes
}

export interface Preset {
  name: string;
  material?: string;
  operation?: string;
  parameters: PresetParameters;
}

export interface PresetParameters {
  vc?: number;
  n?: number;
  fz?: number;
  vf?: number;
  ae?: number;
  ap?: number;
}

// ============================================================================
// Material Types
// ============================================================================

export interface Material {
  id: string;
  name: string;
  hardness_order: number;  // 1 (softest) to 7 (hardest)
  color: string;
  category: string;
}

// ============================================================================
// Operation Types
// ============================================================================

export interface OperationGroup {
  group: string;
  operations: Operation[];
}

export interface Operation {
  id: string;
  name: string;
  description: string;
  typical_ae_range: string;
  typical_ap_range: string;
}

// ============================================================================
// Calculation Types
// ============================================================================

export enum CoatingType {
  NONE = 'none',
  TIN = 'tin',
  TIALN = 'tialn',
  ALTIN = 'altin',
  DIAMOND = 'diamond',
  CARBIDE = 'carbide',
}

export enum SurfaceQuality {
  ROUGHING = 'roughing',
  STANDARD = 'standard',
  FINISHING = 'finishing',
  HIGH_FINISH = 'high_finish',
}

export enum CoolantType {
  WET = 'wet',
  DRY = 'dry',
  MQL = 'mql',
}

export enum ChipFormationType {
  CONTINUOUS = 'continuous',
  SEGMENTED = 'segmented',
  DISCONTINUOUS = 'discontinuous',
  DUST = 'dust',
}

export interface ExpertModeSettings {
  global_adjustment: number;  // -50 to +50
  overrides?: {
    ae_mm?: number;
    ap_mm?: number;
    fz_mm?: number;
  };
}

export interface CalculationRequest {
  tool_id: string;
  material: string;
  operation: string;
  coating?: CoatingType;
  surface_quality?: SurfaceQuality;
  coolant?: CoolantType;
  expert_mode?: ExpertModeSettings;
}

export interface CalculationResponse {
  calculation_id: string;
  timestamp: string;
  tool: Tool;
  input: CalculationRequest;
  results: CalculationResults;
  validation: ValidationChecks;
  warnings: string[];
  mathematical_workbook?: FormulaBreakdown;
}

export interface CalculationResults {
  // Phase 1-2: Cutting Speed
  vc_base: number;
  coating_factor: number;
  vc_final: number;

  // Phase 3: Spindle Speed
  n_rpm: number;

  // Phase 4-5: Feed
  fz_base: number;
  coolant_factor: number;
  fz_final: number;
  vf_mm_min: number;
  vf_entry: number;
  vf_ramp: number;
  vf_plunge: number;

  // Phase 6-8: Engagement
  ae_mm: number;
  ap_mm: number;
  ap_reference: string;
  surface_quality_factor: number;

  // Phase 9-10: Power & Thermal
  mrr_cm3_min: number;
  power_kw: number;
  torque_nm: number;
  chip_temperature_c: number;
  chip_formation: ChipFormationType;

  // L/D Stability
  ld_ratio: number;
  ld_classification: string;
  ld_reduction_factor: number;
}

export interface ValidationChecks {
  all_passed: boolean;
  checks: ValidationCheck[];
}

export interface ValidationCheck {
  name: string;
  passed: boolean;
  message: string;
  severity: 'info' | 'warning' | 'error';
  value?: any;
  limit?: any;
}

export interface FormulaBreakdown {
  vc: FormulaStep;
  [key: string]: FormulaStep;
}

export interface FormulaStep {
  formula: string;
  steps: string[];
  reference?: number;
  deviation?: number;
}

// ============================================================================
// Import Types
// ============================================================================

export interface ImportRequest {
  file: File;
}

export interface ImportResponse {
  tools: Tool[];
  materials_detected: DetectedMaterial[];
  operations_detected: DetectedOperation[];
  message: string;
}

export interface DetectedMaterial {
  tool_id: string;
  material: string;
  source: string;
  count: number;
}

export interface DetectedOperation {
  tool_id: string;
  operation: string;
  source: string;
  count: number;
}

// ============================================================================
// Export Types
// ============================================================================

export interface ExportRequest {
  calculation_ids: string[];
  library_name?: string;
}

export interface UndersottExportRequest {
  calculation_ids: string[];
}

// ============================================================================
// API Response Types
// ============================================================================

export interface HealthResponse {
  status: 'ok' | 'error';
  version: string;
  timestamp: string;
}

export interface MaterialsResponse {
  materials: Material[];
}

export interface OperationsResponse {
  operations: OperationGroup[];
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}
