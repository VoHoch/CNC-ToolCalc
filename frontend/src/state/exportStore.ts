// Export Store

import { create } from 'zustand';
import { apiClient } from '@/api/client';

type ExportFormat = 'fusion' | 'underscott' | 'json' | 'pdf';

interface ExportStore {
  // State
  exportFormat: ExportFormat;
  selectedResultIds: string[]; // Which results to export
  presetName: string;
  isExporting: boolean;
  error: string | null;

  // Actions
  selectExportFormat: (format: ExportFormat) => void;
  toggleResultSelection: (resultId: string) => void;
  selectAllResults: (resultIds: string[]) => void;
  deselectAllResults: () => void;
  setPresetName: (name: string) => void;

  exportFusion: () => Promise<Blob>;
  exportUnderscott: () => Promise<Blob>;
  downloadExport: (blob: Blob, filename: string) => void;

  resetExport: () => void;
}

export const useExportStore = create<ExportStore>((set, get) => ({
  // Initial State
  exportFormat: 'fusion',
  selectedResultIds: [],
  presetName: '',
  isExporting: false,
  error: null,

  // Actions
  selectExportFormat: (format) => set({ exportFormat: format }),

  toggleResultSelection: (resultId) =>
    set((state) => ({
      selectedResultIds: state.selectedResultIds.includes(resultId)
        ? state.selectedResultIds.filter((id) => id !== resultId)
        : [...state.selectedResultIds, resultId],
    })),

  selectAllResults: (resultIds) => set({ selectedResultIds: resultIds }),

  deselectAllResults: () => set({ selectedResultIds: [] }),

  setPresetName: (name) => set({ presetName: name }),

  exportFusion: async () => {
    const { selectedResultIds, presetName } = get();

    set({ isExporting: true, error: null });

    try {
      const blob = await apiClient.exportFusion({
        calculation_ids: selectedResultIds,
        library_name: presetName || undefined,
      });

      set({ isExporting: false });
      return blob;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Export failed';
      set({ isExporting: false, error: errorMessage });
      throw error;
    }
  },

  exportUnderscott: async () => {
    const { selectedResultIds } = get();

    set({ isExporting: true, error: null });

    try {
      const blob = await apiClient.exportUnderscott({
        calculation_ids: selectedResultIds,
      });

      set({ isExporting: false });
      return blob;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Export failed';
      set({ isExporting: false, error: errorMessage });
      throw error;
    }
  },

  downloadExport: (blob, filename) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },

  resetExport: () =>
    set({
      selectedResultIds: [],
      presetName: '',
      error: null,
    }),
}));
