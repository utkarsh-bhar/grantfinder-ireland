import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ProfileData } from '@/types';

interface ProfileState {
  currentStep: number;
  totalSteps: number;
  profile: ProfileData;
  setStep: (step: number) => void;
  nextStep: () => void;
  prevStep: () => void;
  updateProfile: (data: Partial<ProfileData>) => void;
  resetProfile: () => void;
}

const initialProfile: ProfileData = {};

export const useProfileStore = create<ProfileState>()(
  persist(
    (set) => ({
      currentStep: 1,
      totalSteps: 7,
      profile: initialProfile,

      setStep: (step) => set({ currentStep: step }),
      nextStep: () => set((state) => ({ currentStep: Math.min(state.currentStep + 1, state.totalSteps) })),
      prevStep: () => set((state) => ({ currentStep: Math.max(state.currentStep - 1, 1) })),
      updateProfile: (data) =>
        set((state) => ({ profile: { ...state.profile, ...data } })),
      resetProfile: () => set({ currentStep: 1, profile: initialProfile }),
    }),
    {
      name: 'grantfinder-profile',
    }
  )
);
