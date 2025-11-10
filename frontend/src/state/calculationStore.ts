// Calculation Store

import { create } from 'zustand';
import type {
  CoatingType,
  SurfaceQuality,
  CoolantType,
  CalculationRequest,
  CalculationResponse,
} from '@/types/api';
import { apiClient } from '@/api/client';

interface CalculationStore {
  // State
  selectedOperations: string[];
  coatingType: CoatingType;
  surfaceQuality: SurfaceQuality;
  coolantType: CoolantType;

  calculationResults: Record<string, CalculationResponse>; // keyed by "T1_aluminium_FACE_ROUGH"
  isCalculating: boolean;
  currentPhase: number; // 1-10 for progress display
  error: string | null;

  // Actions
  selectOperation: (opId: string) => void;
  deselectOperation: (opId: string) => void;
  toggleOperation: (opId: string) => void;
  setCoating: (coating: CoatingType) => void;
  setSurfaceQuality: (quality: SurfaceQuality) => void;
  setCoolant: (coolant: CoolantType) => void;

  calculate: (
    toolId: string,
    materialId: string,
    operationId: string
  ) => Promise<void>;

  getResultsForTool: (toolId: string) => CalculationResponse[];
  getResultKey: (toolId: string, materialId: string, operationId: string) => string;
  resetResults: () => void;
}

export const useCalculationStore = create<CalculationStore>((set, get) => ({
  // Initial State
  selectedOperations: [],
  coatingType: 'none' as CoatingType,
  surfaceQuality: 'standard' as SurfaceQuality,
  coolantType: 'wet' as CoolantType,
  calculationResults: {},
  isCalculating: false,
  currentPhase: 0,
  error: null,

  // Actions
  selectOperation: (opId) =>
    set((state) => ({
      selectedOperations: state.selectedOperations.includes(opId)
        ? state.selectedOperations
        : [...state.selectedOperations, opId],
    })),

  deselectOperation: (opId) =>
    set((state) => ({
      selectedOperations: state.selectedOperations.filter((id) => id !== opId),
    })),

  toggleOperation: (opId) => {
    const { selectedOperations, selectOperation, deselectOperation } = get();
    if (selectedOperations.includes(opId)) {
      deselectOperation(opId);
    } else {
      selectOperation(opId);
    }
  },

  setCoating: (coating) => set({ coatingType: coating }),

  setSurfaceQuality: (quality) => set({ surfaceQuality: quality }),

  setCoolant: (coolant) => set({ coolantType: coolant }),

  calculate: async (toolId, materialId, operationId) => {
    const { coatingType, surfaceQuality, coolantType } = get();

    set({ isCalculating: true, currentPhase: 1, error: null });

    try {
      const request: CalculationRequest = {
        tool_id: toolId,
        material: materialId,
        operation: operationId,
        coating: coatingType,
        surface_quality: surfaceQuality,
        coolant: coolantType,
      };

      // Simulate progress phases (could be enhanced with real progress tracking)
      for (let phase = 1; phase <= 10; phase++) {
        set({ currentPhase: phase });
        await new Promise((resolve) => setTimeout(resolve, 100));
      }

      const response = await apiClient.calculate(request);

      const resultKey = get().getResultKey(toolId, materialId, operationId);

      set((state) => ({
        calculationResults: {
          ...state.calculationResults,
          [resultKey]: response,
        },
        isCalculating: false,
        currentPhase: 10,
      }));
    } catch (error) {
      set({
        isCalculating: false,
        currentPhase: 0,
        error: error instanceof Error ? error.message : 'Calculation failed',
      });
      throw error;
    }
  },

  getResultsForTool: (toolId) => {
    const { calculationResults } = get();
    return Object.entries(calculationResults)
      .filter(([key]) => key.startsWith(`${toolId}_`))
      .map(([, result]) => result);
  },

  getResultKey: (toolId, materialId, operationId) => {
    return `${toolId}_${materialId}_${operationId}`;
  },

  resetResults: () => set({ calculationResults: {}, error: null }),
}));
