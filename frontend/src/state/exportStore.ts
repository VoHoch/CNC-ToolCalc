import { create } from 'zustand';
import { apiClient } from '@/api/client';

type ExportFormat = 'fusion' | 'underscott' | 'json' | 'pdf';

interface ExportStore {
  exportFormat: ExportFormat;
  selectedResultIds: string[];
  isExporting: boolean;
  selectExportFormat: (format: ExportFormat) => void;
  toggleResultSelection: (resultId: string) => void;
  exportFusion: () => Promise<Blob>;
  downloadExport: (blob: Blob, filename: string) => void;
}

export const useExportStore = create<ExportStore>((set, get) => ({
  exportFormat: 'fusion',
  selectedResultIds: [],
  isExporting: false,

  selectExportFormat: (format) => set({ exportFormat: format }),

  toggleResultSelection: (resultId) =>
    set((state) => ({
      selectedResultIds: state.selectedResultIds.includes(resultId)
        ? state.selectedResultIds.filter((id) => id !== resultId)
        : [...state.selectedResultIds, resultId],
    })),

  exportFusion: async () => {
    const { selectedResultIds } = get();
    set({ isExporting: true });
    try {
      const blob = await apiClient.exportFusion({ calculation_ids: selectedResultIds });
      set({ isExporting: false });
      return blob;
    } catch (error) {
      set({ isExporting: false });
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
}));
