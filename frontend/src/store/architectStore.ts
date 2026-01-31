import { create } from 'zustand';
import type { ArchitectResponse } from '../types/index';

interface ArchitectStore {
  result: ArchitectResponse | null;
  isLoading: boolean;
  error: string | null;
  setResult: (result: ArchitectResponse | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clear: () => void;
}

export const useArchitectStore = create<ArchitectStore>((set) => ({
  result: null,
  isLoading: false,
  error: null,

  setResult: (result) => set({ result }),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  clear: () => set({ result: null, error: null }),
}));
