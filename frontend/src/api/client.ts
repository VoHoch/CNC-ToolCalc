// API Client for Backend Communication

import type {
  HealthResponse,
  ImportResponse,
  MaterialsResponse,
  OperationsResponse,
  CalculationRequest,
  CalculationResponse,
  ExportRequest,
  UndersottExportRequest,
  ErrorResponse,
} from '@/types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

class CalculationApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  // ============================================================================
  // Health Check
  // ============================================================================

  async health(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  }

  // ============================================================================
  // Import Tool Library
  // ============================================================================

  async import(file: File): Promise<ImportResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/api/import`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData: ErrorResponse = await response.json();
      throw new ApiError(
        errorData.error.code,
        errorData.error.message,
        errorData.error.details
      );
    }

    return response.json();
  }

  // ============================================================================
  // Get Available Materials
  // ============================================================================

  async getMaterials(): Promise<MaterialsResponse> {
    const response = await fetch(`${this.baseUrl}/api/materials`);

    if (!response.ok) {
      const errorData: ErrorResponse = await response.json();
      throw new ApiError(
        errorData.error.code,
        errorData.error.message,
        errorData.error.details
      );
    }

    return response.json();
  }

  // ============================================================================
  // Get Available Operations
  // ============================================================================

  async getOperations(): Promise<OperationsResponse> {
    const response = await fetch(`${this.baseUrl}/api/operations`);

    if (!response.ok) {
      const errorData: ErrorResponse = await response.json();
      throw new ApiError(
        errorData.error.code,
        errorData.error.message,
        errorData.error.details
      );
    }

    return response.json();
  }

  // ============================================================================
  // Calculate Parameters (MAIN ENDPOINT)
  // ============================================================================

  async calculate(request: CalculationRequest): Promise<CalculationResponse> {
    const response = await fetch(`${this.baseUrl}/api/calculate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData: ErrorResponse = await response.json();
      throw new ApiError(
        errorData.error.code,
        errorData.error.message,
        errorData.error.details
      );
    }

    return response.json();
  }

  // ============================================================================
  // Export to Fusion 360
  // ============================================================================

  async exportFusion(request: ExportRequest): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/api/export/fusion`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData: ErrorResponse = await response.json();
      throw new ApiError(
        errorData.error.code,
        errorData.error.message,
        errorData.error.details
      );
    }

    return response.blob();
  }

  // ============================================================================
  // Export to Underscott CSV
  // ============================================================================

  async exportUnderscott(request: UndersottExportRequest): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/api/export/underscott`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData: ErrorResponse = await response.json();
      throw new ApiError(
        errorData.error.code,
        errorData.error.message,
        errorData.error.details
      );
    }

    return response.blob();
  }
}

// Export singleton instance
export const apiClient = new CalculationApiClient();
export { ApiError };
export type { CalculationApiClient };
