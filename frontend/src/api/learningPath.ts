import apiClient from './client';
import type { LearningPathResponse, Topic, ProgressResponse } from '../types/index';

export const learningPathApi = {
  getAll: async (): Promise<LearningPathResponse> => {
    const response = await apiClient.get<LearningPathResponse>('/learning-path');
    return response.data;
  },

  getByLevel: async (level: string): Promise<{ level: string; topics: Topic[]; count: number }> => {
    const response = await apiClient.get(`/learning-path/level/${encodeURIComponent(level)}`);
    return response.data;
  },

  getTopic: async (topicId: string): Promise<Topic> => {
    const response = await apiClient.get<Topic>(`/learning-path/topic/${topicId}`);
    return response.data;
  },

  calculateProgress: async (completedIds: string[]): Promise<ProgressResponse> => {
    const response = await apiClient.post<ProgressResponse>('/learning-path/progress', {
      completed_topic_ids: completedIds,
    });
    return response.data;
  },
};
