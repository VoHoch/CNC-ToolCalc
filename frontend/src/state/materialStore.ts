// Material Selection Store (PER TOOL!)

import { create } from 'zustand';
import type { Material } from '@/types/api';

interface MaterialStore {
  // State: materials are per-tool!
  materialsByTool: Record<string, string[]>; // {T1: ["aluminium", "steel"], T2: ["aluminium"]}
  allMaterials: Material[];

  // Actions
  loadMaterials: (materials: Material[]) => void;
  selectMaterialForTool: (toolId: string, materialId: string) => void;
  deselectMaterialForTool: (toolId: string, materialId: string) => void;
  toggleMaterialForTool: (toolId: string, materialId: string) => void;
  getMaterialsForTool: (toolId: string) => Material[];
  getAllSelectedMaterials: () => Array<{ toolId: string; materialId: string }>;
  resetMaterialsForTool: (toolId: string) => void;
  resetAll: () => void;
}

export const useMaterialStore = create<MaterialStore>((set, get) => ({
  // Initial State
  materialsByTool: {},
  allMaterials: [],

  // Actions
  loadMaterials: (materials) => set({ allMaterials: materials }),

  selectMaterialForTool: (toolId, materialId) =>
    set((state) => {
      const currentMaterials = state.materialsByTool[toolId] || [];
      if (currentMaterials.includes(materialId)) {
        return state; // Already selected
      }
      return {
        materialsByTool: {
          ...state.materialsByTool,
          [toolId]: [...currentMaterials, materialId],
        },
      };
    }),

  deselectMaterialForTool: (toolId, materialId) =>
    set((state) => {
      const currentMaterials = state.materialsByTool[toolId] || [];
      return {
        materialsByTool: {
          ...state.materialsByTool,
          [toolId]: currentMaterials.filter((id) => id !== materialId),
        },
      };
    }),

  toggleMaterialForTool: (toolId, materialId) => {
    const { materialsByTool, selectMaterialForTool, deselectMaterialForTool } = get();
    const currentMaterials = materialsByTool[toolId] || [];
    if (currentMaterials.includes(materialId)) {
      deselectMaterialForTool(toolId, materialId);
    } else {
      selectMaterialForTool(toolId, materialId);
    }
  },

  getMaterialsForTool: (toolId) => {
    const { allMaterials, materialsByTool } = get();
    const materialIds = materialsByTool[toolId] || [];
    return allMaterials.filter((mat) => materialIds.includes(mat.id));
  },

  getAllSelectedMaterials: () => {
    const { materialsByTool } = get();
    const result: Array<{ toolId: string; materialId: string }> = [];

    Object.entries(materialsByTool).forEach(([toolId, materialIds]) => {
      materialIds.forEach((materialId) => {
        result.push({ toolId, materialId });
      });
    });

    return result;
  },

  resetMaterialsForTool: (toolId) =>
    set((state) => ({
      materialsByTool: {
        ...state.materialsByTool,
        [toolId]: [],
      },
    })),

  resetAll: () => set({ materialsByTool: {} }),
}));
