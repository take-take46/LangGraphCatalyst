import apiClient from './client';
import type { RAGQueryRequest, RAGQueryResponse } from '../types/index';

export const ragApi = {
  query: async (request: RAGQueryRequest): Promise<RAGQueryResponse> => {
    const response = await apiClient.post<RAGQueryResponse>('/rag/query', request);
    return response.data;
  },

  checkHealth: async (): Promise<{ status: string; vectorstore_connected: boolean; document_count: number }> => {
    const response = await apiClient.get('/rag/health');
    return response.data;
  },
};
