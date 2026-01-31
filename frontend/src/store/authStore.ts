import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  username: string;
  role: string;
  daily_limit: number | null;
}

interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: () => boolean;
  isAdmin: () => boolean;
  setAuth: (token: string, user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,

      isAuthenticated: () => {
        const state = get();
        return state.token !== null && state.user !== null;
      },

      isAdmin: () => {
        const state = get();
        return state.user?.role === 'admin';
      },

      setAuth: (token: string, user: User) => {
        set({ token, user });
      },

      logout: () => {
        set({ token: null, user: null });
      },
    }),
    {
      name: 'langgraph-catalyst-auth',
    }
  )
);
