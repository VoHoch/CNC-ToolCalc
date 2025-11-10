import { create } from 'zustand';
import type { CoatingType, SurfaceQuality, CoolantType, CalculationResponse } from '@/types/api';
import { apiClient } from '@/api/client';

interface CalculationStore {
  selectedOperations: string[];
  coatingType: CoatingType;
  surfaceQuality: SurfaceQuality;
  coolantType: CoolantType;
  calculationResults: Record<string, CalculationResponse>;
  isCalculating: boolean;
  toggleOperation: (opId: string) => void;
  setCoating: (coating: CoatingType) => void;
  setSurfaceQuality: (quality: SurfaceQuality) => void;
  setCoolant: (coolant: CoolantType) => void;
  calculate: (toolId: string, materialId: string, operationId: string) => Promise<void>;
}

export const useCalculationStore = create<CalculationStore>((set, get) => ({
  selectedOperations: [],
  coatingType: 'none' as CoatingType,
  surfaceQuality: 'standard' as SurfaceQuality,
  coolantType: 'wet' as CoolantType,
  calculationResults: {},
  isCalculating: false,

  toggleOperation: (opId) =>
    set((state) => ({
      selectedOperations: state.selectedOperations.includes(opId)
        ? state.selectedOperations.filter((id) => id !== opId)
        : [...state.selectedOperations, opId],
    })),

  setCoating: (coating) => set({ coatingType: coating }),
  setSurfaceQuality: (quality) => set({ surfaceQuality: quality }),
  setCoolant: (coolant) => set({ coolantType: coolant }),

  calculate: async (toolId, materialId, operationId) => {
    const { coatingType, surfaceQuality, coolantType } = get();
    set({ isCalculating: true });
    try {
      const response = await apiClient.calculate({
        tool_id: toolId,
        material: materialId,
        operation: operationId,
        coating: coatingType,
        surface_quality: surfaceQuality,
        coolant: coolantType,
      });
      const key = `${toolId}_${materialId}_${operationId}`;
      set((state) => ({
        calculationResults: { ...state.calculationResults, [key]: response },
        isCalculating: false,
      }));
    } catch (error) {
      console.error('Calculation failed:', error);
      set({ isCalculating: false });
    }
  },
}));
