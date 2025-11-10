// API Types (kompakte Version)

export interface Tool {
  id: string;
  name: string;
  type: string;
  geometry: { DC: number; LCF: number; DCON: number; OAL: number; NOF: number };
  ld_ratio: number;
  ld_classification: string;
  presets?: Preset[];
}

export interface Preset {
  name: string;
  material?: string;
  operation?: string;
  parameters: { vc?: number; n?: number; fz?: number; vf?: number; ae?: number; ap?: number };
}

export interface Material {
  id: string;
  name: string;
  hardness_order: number;
  color: string;
  category: string;
}

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

export type CoatingType = 'none' | 'tin' | 'tialn' | 'altin' | 'diamond' | 'carbide';
export type SurfaceQuality = 'roughing' | 'standard' | 'finishing' | 'high_finish';
export type CoolantType = 'wet' | 'dry' | 'mql';

export interface CalculationRequest {
  tool_id: string;
  material: string;
  operation: string;
  coating?: CoatingType;
  surface_quality?: SurfaceQuality;
  coolant?: CoolantType;
  expert_mode?: { global_adjustment: number; overrides?: Record<string, number> };
}

export interface CalculationResponse {
  calculation_id: string;
  timestamp: string;
  tool: Tool;
  input: CalculationRequest;
  results: CalculationResults;
  validation: { all_passed: boolean; checks: ValidationCheck[] };
  warnings: string[];
}

export interface CalculationResults {
  vc_base: number;
  coating_factor: number;
  vc_final: number;
  n_rpm: number;
  fz_base: number;
  coolant_factor: number;
  fz_final: number;
  vf_mm_min: number;
  vf_entry: number;
  vf_ramp: number;
  vf_plunge: number;
  ae_mm: number;
  ap_mm: number;
  ap_reference: string;
  surface_quality_factor: number;
  mrr_cm3_min: number;
  power_kw: number;
  torque_nm: number;
  chip_temperature_c: number;
  chip_formation: string;
  ld_ratio: number;
  ld_classification: string;
  ld_reduction_factor: number;
}

export interface ValidationCheck {
  name: string;
  passed: boolean;
  message: string;
  severity: 'info' | 'warning' | 'error';
  value?: any;
  limit?: any;
}

export interface MaterialsResponse {
  materials: Material[];
}

export interface OperationsResponse {
  operations: OperationGroup[];
}

export interface ExportRequest {
  calculation_ids: string[];
  library_name?: string;
}

export interface ErrorResponse {
  error: { code: string; message: string; details?: any };
}
