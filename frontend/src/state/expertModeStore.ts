import { create } from 'zustand';

interface ExpertModeStore {
  expertModeEnabled: boolean;
  globalSlider: number; // -50 to +50
  parameterOverrides: { ae_mm?: number; ap_mm?: number; fz_mm?: number };
  toggleExpertMode: () => void;
  setGlobalSlider: (value: number) => void;
  setParameterOverride: (param: 'ae' | 'ap' | 'fz', value: number | undefined) => void;
}

export const useExpertModeStore = create<ExpertModeStore>((set) => ({
  expertModeEnabled: false,
  globalSlider: 0,
  parameterOverrides: {},
  toggleExpertMode: () => set((state) => ({ expertModeEnabled: !state.expertModeEnabled })),
  setGlobalSlider: (value) => set({ globalSlider: Math.max(-50, Math.min(50, value)) }),
  setParameterOverride: (param, value) =>
    set((state) => ({
      parameterOverrides: { ...state.parameterOverrides, [`${param}_mm`]: value },
    })),
}));
