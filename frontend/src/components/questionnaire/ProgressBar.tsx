'use client';

interface ProgressBarProps {
  currentStep: number;
  totalSteps: number;
}

const STEP_LABELS = [
  'About You',
  'Your Home',
  'Family',
  'Work & Income',
  'Welfare & Health',
  'Education & Business',
  'Transport & Other',
];

export default function ProgressBar({ currentStep, totalSteps }: ProgressBarProps) {
  const progress = ((currentStep - 1) / (totalSteps - 1)) * 100;

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-brand-600">
          Step {currentStep} of {totalSteps}
        </span>
        <span className="text-sm text-gray-500">
          {STEP_LABELS[currentStep - 1]}
        </span>
      </div>
      <div className="h-2 w-full rounded-full bg-gray-200">
        <div
          className="h-2 rounded-full bg-brand-500 transition-all duration-500 ease-out"
          style={{ width: `${Math.max(progress, 5)}%` }}
        />
      </div>
    </div>
  );
}
