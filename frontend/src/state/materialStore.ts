import { create } from 'zustand';
import type { Material } from '@/types/api';

// CRITICAL: Materials are PER-TOOL!
interface MaterialStore {
  materialsByTool: Record<string, string[]>; // {T1: ["aluminium"], T2: ["steel"]}
  allMaterials: Material[];
  loadMaterials: (materials: Material[]) => void;
  toggleMaterialForTool: (toolId: string, materialId: string) => void;
  getMaterialsForTool: (toolId: string) => Material[];
}

export const useMaterialStore = create<MaterialStore>((set, get) => ({
  materialsByTool: {},
  allMaterials: [],
  loadMaterials: (materials) => set({ allMaterials: materials }),
  toggleMaterialForTool: (toolId, materialId) =>
    set((state) => {
      const current = state.materialsByTool[toolId] || [];
      return {
        materialsByTool: {
          ...state.materialsByTool,
          [toolId]: current.includes(materialId)
            ? current.filter((id) => id !== materialId)
            : [...current, materialId],
        },
      };
    }),
  getMaterialsForTool: (toolId) => {
    const { allMaterials, materialsByTool } = get();
    const materialIds = materialsByTool[toolId] || [];
    return allMaterials.filter((mat) => materialIds.includes(mat.id));
  },
}));
