import { create } from 'zustand';
import type { ScanResponse } from '@/types';
import { scanAPI } from '@/lib/api';
import type { ProfileData } from '@/types';

interface ScanState {
  results: ScanResponse | null;
  isScanning: boolean;
  error: string | null;
  runAnonymousScan: (profile: ProfileData) => Promise<void>;
  runAuthenticatedScan: () => Promise<void>;
  clearResults: () => void;
}

export const useScanStore = create<ScanState>((set) => ({
  results: null,
  isScanning: false,
  error: null,

  runAnonymousScan: async (profile) => {
    set({ isScanning: true, error: null });
    try {
      const { data } = await scanAPI.anonymous(profile);
      set({ results: data, isScanning: false });
    } catch (err: any) {
      set({
        isScanning: false,
        error: err.response?.data?.detail || 'An error occurred while scanning.',
      });
    }
  },

  runAuthenticatedScan: async () => {
    set({ isScanning: true, error: null });
    try {
      const { data } = await scanAPI.run();
      set({ results: data, isScanning: false });
    } catch (err: any) {
      set({
        isScanning: false,
        error: err.response?.data?.detail || 'An error occurred while scanning.',
      });
    }
  },

  clearResults: () => set({ results: null, error: null }),
}));
