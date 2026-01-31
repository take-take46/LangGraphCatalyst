import apiClient from './client';
import type { ArchitectRequest, ArchitectResponse } from '../types/index';

export const architectApi = {
  generate: async (request: ArchitectRequest): Promise<ArchitectResponse> => {
    const response = await apiClient.post<ArchitectResponse>('/architect/generate', request);
    return response.data;
  },
};
