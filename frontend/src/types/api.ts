// API Type Definitions

// Tool Types
export interface Tool {
  id: string;
  name: string;
  type: string;
  geometry: {
    DC: number;     // Diameter
    LCF: number;    // Cutting Length
    NOF: number;    // Number of Flutes
  };
  ld_ratio: number;
  ld_classification: string;
  presets?: ToolPreset[];
}

export interface ToolPreset {
  id: string;
  name: string;
  material: string;
  parameters: {
    speed: number;
    feed: number;
  };
}

// Material Types
export interface Material {
  id: string;
  name: string;
  category: string;
  hardness_order: number;
  color: string;
}

// Operation Types
export type CoatingType = 'none' | 'TiN' | 'TiAlN' | 'AlTiN' | 'TiCN';
export type SurfaceQuality = 'rough' | 'standard' | 'finish';
export type CoolantType = 'dry' | 'wet' | 'mql' | 'coolant';

export interface Operation {
  id: string;
  name: string;
  type: string;
}

// Calculation Request/Response
export interface CalculationRequest {
  tool_id: string;
  material: string;
  operation: string;
  coating: CoatingType;
  surface_quality: SurfaceQuality;
  coolant: CoolantType;
}

export interface CalculationResponse {
  tool_id: string;
  material: string;
  operation: string;
  parameters: {
    vc: number;      // Cutting speed
    n: number;       // Spindle speed (RPM)
    fz: number;      // Feed per tooth
    vf: number;      // Feed rate
    ae: number;      // Radial depth of cut
    ap: number;      // Axial depth of cut
  };
  warnings?: string[];
  timestamp: string;
}

// API Response Wrappers
export interface ToolsResponse {
  tools: Tool[];
}

export interface MaterialsResponse {
  materials: Material[];
}

export interface OperationsResponse {
  operations: Operation[];
}
