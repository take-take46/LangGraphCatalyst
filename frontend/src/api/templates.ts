import apiClient from './client';
import type { Template, TemplatesListResponse } from '../types/index';

export const templatesApi = {
  getAll: async (category?: string, difficulty?: string): Promise<TemplatesListResponse> => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (difficulty) params.append('difficulty', difficulty);

    const response = await apiClient.get<TemplatesListResponse>(`/templates?${params.toString()}`);
    return response.data;
  },

  getCategories: async (): Promise<Record<string, string>> => {
    const response = await apiClient.get<{ categories: Record<string, string> }>('/templates/categories');
    return response.data.categories;
  },

  getById: async (id: string): Promise<Template> => {
    const response = await apiClient.get<Template>(`/templates/${id}`);
    return response.data;
  },
};
