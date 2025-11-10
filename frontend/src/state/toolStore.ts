import { create } from 'zustand';
import type { Tool } from '@/types/api';

interface ToolStore {
  allTools: Tool[];
  selectedToolIds: string[];
  loadTools: (tools: Tool[]) => void;
  toggleTool: (toolId: string) => void;
  getSelectedTools: () => Tool[];
}

export const useToolStore = create<ToolStore>((set, get) => ({
  allTools: [],
  selectedToolIds: [],
  loadTools: (tools) => set({ allTools: tools }),
  toggleTool: (toolId) =>
    set((state) => ({
      selectedToolIds: state.selectedToolIds.includes(toolId)
        ? state.selectedToolIds.filter((id) => id !== toolId)
        : [...state.selectedToolIds, toolId],
    })),
  getSelectedTools: () => {
    const { allTools, selectedToolIds } = get();
    return allTools.filter((tool) => selectedToolIds.includes(tool.id));
  },
}));
