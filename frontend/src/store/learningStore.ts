import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface LearningStore {
  completedTopics: string[];
  markCompleted: (topicId: string) => void;
  markIncomplete: (topicId: string) => void;
  isTopicCompleted: (topicId: string) => boolean;
  clearProgress: () => void;
}

export const useLearningStore = create<LearningStore>()(
  persist(
    (set, get) => ({
      completedTopics: [],

      markCompleted: (topicId) =>
        set((state) => ({
          completedTopics: Array.from(new Set([...state.completedTopics, topicId])),
        })),

      markIncomplete: (topicId) =>
        set((state) => ({
          completedTopics: state.completedTopics.filter((id) => id !== topicId),
        })),

      isTopicCompleted: (topicId) => get().completedTopics.includes(topicId),

      clearProgress: () => set({ completedTopics: [] }),
    }),
    {
      name: 'langgraph-catalyst-progress',
    }
  )
);
