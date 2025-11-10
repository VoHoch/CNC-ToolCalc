// API Client for Backend Communication
import type {
  MaterialsResponse,
  OperationsResponse,
  CalculationRequest,
  CalculationResponse,
  ExportRequest,
} from '@/types/api';

const API_BASE_URL = 'http://localhost:8000';

class ApiClient {
  async getMaterials(): Promise<MaterialsResponse> {
    const res = await fetch(`${API_BASE_URL}/api/materials`);
    if (!res.ok) throw new Error('Failed to fetch materials');
    return res.json();
  }

  async getOperations(): Promise<OperationsResponse> {
    const res = await fetch(`${API_BASE_URL}/api/operations`);
    if (!res.ok) throw new Error('Failed to fetch operations');
    return res.json();
  }

  async calculate(req: CalculationRequest): Promise<CalculationResponse> {
    const res = await fetch(`${API_BASE_URL}/api/calculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req),
    });
    if (!res.ok) throw new Error('Calculation failed');
    return res.json();
  }

  async exportFusion(req: ExportRequest): Promise<Blob> {
    const res = await fetch(`${API_BASE_URL}/api/export/fusion`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req),
    });
    if (!res.ok) throw new Error('Export failed');
    return res.blob();
  }
}

export const apiClient = new ApiClient();
