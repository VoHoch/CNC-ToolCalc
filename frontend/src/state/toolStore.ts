// Tool Selection Store

import { create } from 'zustand';
import type { Tool } from '@/types/api';

interface ToolStore {
  // State
  allTools: Tool[];
  selectedToolIds: string[];

  // Actions
  loadTools: (tools: Tool[]) => void;
  selectTool: (toolId: string) => void;
  deselectTool: (toolId: string) => void;
  toggleTool: (toolId: string) => void;
  getSelectedTools: () => Tool[];
  resetSelection: () => void;
}

export const useToolStore = create<ToolStore>((set, get) => ({
  // Initial State
  allTools: [],
  selectedToolIds: [],

  // Actions
  loadTools: (tools) => set({ allTools: tools }),

  selectTool: (toolId) =>
    set((state) => ({
      selectedToolIds: state.selectedToolIds.includes(toolId)
        ? state.selectedToolIds
        : [...state.selectedToolIds, toolId],
    })),

  deselectTool: (toolId) =>
    set((state) => ({
      selectedToolIds: state.selectedToolIds.filter((id) => id !== toolId),
    })),

  toggleTool: (toolId) => {
    const { selectedToolIds, selectTool, deselectTool } = get();
    if (selectedToolIds.includes(toolId)) {
      deselectTool(toolId);
    } else {
      selectTool(toolId);
    }
  },

  getSelectedTools: () => {
    const { allTools, selectedToolIds } = get();
    return allTools.filter((tool) => selectedToolIds.includes(tool.id));
  },

  resetSelection: () => set({ selectedToolIds: [] }),
}));
