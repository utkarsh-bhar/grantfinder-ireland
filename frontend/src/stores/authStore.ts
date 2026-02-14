import { create } from 'zustand';
import type { User } from '@/types';
import { authAPI } from '@/lib/api';
import { setTokens, clearTokens } from '@/lib/auth';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: false,
  isAuthenticated: false,

  login: async (email, password) => {
    set({ isLoading: true });
    try {
      const { data } = await authAPI.login(email, password);
      setTokens(data.access_token, data.refresh_token);
      const { data: user } = await authAPI.me();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (err) {
      set({ isLoading: false });
      throw err;
    }
  },

  register: async (email, password) => {
    set({ isLoading: true });
    try {
      const { data } = await authAPI.register(email, password);
      setTokens(data.access_token, data.refresh_token);
      const { data: user } = await authAPI.me();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (err) {
      set({ isLoading: false });
      throw err;
    }
  },

  logout: () => {
    clearTokens();
    set({ user: null, isAuthenticated: false });
  },

  fetchUser: async () => {
    set({ isLoading: true });
    try {
      const { data } = await authAPI.me();
      set({ user: data, isAuthenticated: true, isLoading: false });
    } catch {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },
}));
