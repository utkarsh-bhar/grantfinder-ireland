'use client';

import { useRouter } from 'next/navigation';
import { useProfileStore } from '@/stores/profileStore';
import { useScanStore } from '@/stores/scanStore';
import ProgressBar from './ProgressBar';
import StepAboutYou from './StepAboutYou';
import StepYourHome from './StepYourHome';
import StepFamily from './StepFamily';
import StepWorkIncome from './StepWorkIncome';
import StepWelfareHealth from './StepWelfareHealth';
import StepEducationBusiness from './StepEducationBusiness';
import StepTransportOther from './StepTransportOther';

export default function QuestionnaireWizard() {
  const router = useRouter();
  const { currentStep, totalSteps, nextStep, prevStep, profile } = useProfileStore();
  const { runAnonymousScan, isScanning } = useScanStore();

  const handleSubmit = async () => {
    await runAnonymousScan(profile);
    router.push('/results');
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1: return <StepAboutYou />;
      case 2: return <StepYourHome />;
      case 3: return <StepFamily />;
      case 4: return <StepWorkIncome />;
      case 5: return <StepWelfareHealth />;
      case 6: return <StepEducationBusiness />;
      case 7: return <StepTransportOther />;
      default: return null;
    }
  };

  return (
    <div className="mx-auto max-w-2xl">
      <ProgressBar currentStep={currentStep} totalSteps={totalSteps} />

      <div className="card">
        {renderStep()}

        <div className="mt-8 flex items-center justify-between">
          {currentStep > 1 ? (
            <button onClick={prevStep} className="btn-secondary">
              &larr; Back
            </button>
          ) : (
            <div />
          )}

          {currentStep < totalSteps ? (
            <button onClick={nextStep} className="btn-primary">
              Next &rarr;
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={isScanning}
              className="btn-primary bg-brand-600 px-8"
            >
              {isScanning ? (
                <span className="flex items-center gap-2">
                  <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Finding your grants...
                </span>
              ) : (
                'See my grants! 🍀'
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
