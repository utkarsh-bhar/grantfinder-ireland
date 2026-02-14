import QuestionnaireWizard from '@/components/questionnaire/QuestionnaireWizard';

export const metadata = {
  title: 'Find Your Grants — GrantFinder Ireland',
  description: 'Answer a few questions to discover every grant, scheme, and entitlement you qualify for in Ireland.',
};

export default function ScanPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 sm:py-16">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">Find your grants</h1>
        <p className="mt-2 text-gray-500">Answer a few quick questions — it takes under 3 minutes.</p>
      </div>
      <QuestionnaireWizard />
    </div>
  );
}
