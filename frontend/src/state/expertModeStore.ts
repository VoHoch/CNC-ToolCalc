// Expert Mode Store

import { create } from 'zustand';
import type { ExpertModeSettings, CalculationResponse } from '@/types/api';
import { apiClient } from '@/api/client';
import { useCalculationStore } from './calculationStore';

interface ExpertModeStore {
  // State
  expertModeEnabled: boolean;
  globalSlider: number; // -50 to +50
  parameterOverrides: {
    ae_mm?: number;
    ap_mm?: number;
    fz_mm?: number;
  };

  // Adjusted results based on expert mode settings
  adjustedResults: Record<string, CalculationResponse>;

  // Actions
  toggleExpertMode: () => void;
  setGlobalSlider: (value: number) => void;
  setParameterOverride: (param: 'ae' | 'ap' | 'fz', value: number | undefined) => void;
  recalculateAdjusted: () => Promise<void>;
  resetExpertMode: () => void;
  getExpertModeSettings: () => ExpertModeSettings;
}

export const useExpertModeStore = create<ExpertModeStore>((set, get) => ({
  // Initial State
  expertModeEnabled: false,
  globalSlider: 0,
  parameterOverrides: {},
  adjustedResults: {},

  // Actions
  toggleExpertMode: () =>
    set((state) => ({
      expertModeEnabled: !state.expertModeEnabled,
    })),

  setGlobalSlider: (value) => {
    // Clamp value between -50 and +50
    const clampedValue = Math.max(-50, Math.min(50, value));
    set({ globalSlider: clampedValue });
  },

  setParameterOverride: (param, value) =>
    set((state) => ({
      parameterOverrides: {
        ...state.parameterOverrides,
        [`${param}_mm`]: value,
      },
    })),

  recalculateAdjusted: async () => {
    const { globalSlider, parameterOverrides } = get();
    const calculationStore = useCalculationStore.getState();
    const { calculationResults, coatingType, surfaceQuality, coolantType } = calculationStore;

    // Recalculate all results with expert mode settings
    const expertSettings: ExpertModeSettings = {
      global_adjustment: globalSlider,
      overrides: parameterOverrides,
    };

    const newAdjustedResults: Record<string, CalculationResponse> = {};

    try {
      // Recalculate each result with expert mode settings
      for (const [key, result] of Object.entries(calculationResults)) {
        const request = {
          tool_id: result.tool.id,
          material: result.input.material,
          operation: result.input.operation,
          coating: coatingType,
          surface_quality: surfaceQuality,
          coolant: coolantType,
          expert_mode: expertSettings,
        };

        const adjustedResult = await apiClient.calculate(request);
        newAdjustedResults[key] = adjustedResult;
      }

      set({ adjustedResults: newAdjustedResults });
    } catch (error) {
      console.error('Failed to recalculate with expert mode:', error);
      throw error;
    }
  },

  resetExpertMode: () =>
    set({
      expertModeEnabled: false,
      globalSlider: 0,
      parameterOverrides: {},
      adjustedResults: {},
    }),

  getExpertModeSettings: () => {
    const { globalSlider, parameterOverrides } = get();
    return {
      global_adjustment: globalSlider,
      overrides: parameterOverrides,
    };
  },
}));
